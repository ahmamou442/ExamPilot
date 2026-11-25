from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.config import DATA_DIR, MAX_UPLOAD_MB
from app.db.session import get_db
from app.models.models import Course
from app.services.course_service import process_course

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/upload")
async def upload_course(files: list[UploadFile] = File(...), title: str = Form(default=""), db: Session = Depends(get_db)):
    if not files:
        raise HTTPException(status_code=400, detail="Upload at least one PDF.")
    upload_data: list[tuple[str, bytes]] = []
    limit = MAX_UPLOAD_MB * 1024 * 1024
    for file in files:
        filename = Path(file.filename or "").name
        if not filename or not filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files are supported.")
        data = await file.read(limit + 1)
        await file.close()
        if not data:
            raise HTTPException(status_code=400, detail=f"{filename} is empty.")
        if len(data) > limit:
            raise HTTPException(status_code=413, detail=f"{filename} exceeds the {MAX_UPLOAD_MB} MB limit.")
        upload_data.append((filename, data))
    course_id = str(uuid.uuid4())
    default_title = Path(upload_data[0][0]).stem or "Untitled course"
    course = Course(id=course_id, title=title.strip() or default_title, status="processing")
    db.add(course)
    db.commit()
    try:
        knowledge = await process_course(db, course, upload_data)
    except (ValueError, RuntimeError) as exc:
        db.rollback()
        course.status = "failed"
        db.add(course)
        db.commit()
        shutil.rmtree(DATA_DIR / "courses" / course_id, ignore_errors=True)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        db.rollback()
        course.status = "failed"
        db.add(course)
        db.commit()
        shutil.rmtree(DATA_DIR / "courses" / course_id, ignore_errors=True)
        raise HTTPException(status_code=422, detail="Could not process these course files. Check that the PDFs are readable and try again.") from exc
    return {"id": course_id, "title": course.title, "status": course.status, "knowledge_map": knowledge}


@router.get("")
def list_courses(db: Session = Depends(get_db)):
    return [{"id": course.id, "title": course.title, "description": course.description, "status": course.status, "created_at": course.created_at.isoformat()} for course in db.query(Course).order_by(Course.created_at.desc()).all()]


@router.get("/{cid}")
def get_course(cid: str, db: Session = Depends(get_db)):
    course = db.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return {"id": course.id, "title": course.title, "description": course.description, "status": course.status, "knowledge_map": json.loads(course.knowledge_json or "{}"), "created_at": course.created_at.isoformat()}


@router.get("/{cid}/knowledge-map")
def get_knowledge_map(cid: str, db: Session = Depends(get_db)):
    course = db.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    return json.loads(course.knowledge_json or "{}")


@router.delete("/{cid}")
def delete_course(cid: str, db: Session = Depends(get_db)):
    course = db.get(Course, cid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found.")
    db.delete(course)
    db.commit()
    shutil.rmtree(DATA_DIR / "courses" / cid, ignore_errors=True)
    return {"deleted": True}
