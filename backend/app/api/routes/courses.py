import uuid, json, shutil
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Course
from app.core.config import MAX_UPLOAD_MB, DATA_DIR
from app.services.course_service import process_course
router=APIRouter(prefix="/courses",tags=["courses"])
@router.post("/upload")
async def upload(files:list[UploadFile]=File(...),title:str=Form(default=""),db:Session=Depends(get_db)):
    if not files: raise HTTPException(400,"Upload at least one PDF")
    cid=str(uuid.uuid4()); course=Course(id=cid,title=title or files[0].filename.rsplit(".",1)[0],status="processing"); db.add(course); db.commit()
    upload_data=[]
    for f in files:
        if not f.filename.lower().endswith(".pdf"): course.status="failed"; db.commit(); raise HTTPException(400,f"Unsupported file: {f.filename}. Upload PDFs.")
        data=await f.read()
        if len(data)>MAX_UPLOAD_MB*1024*1024: course.status="failed"; db.commit(); raise HTTPException(413,f"{f.filename} exceeds {MAX_UPLOAD_MB} MB")
        upload_data.append((f.filename,data))
    try: knowledge=await process_course(db,course,upload_data)
    except Exception as e: course.status="failed"; db.commit(); raise HTTPException(422,str(e))
    return {"id":cid,"title":course.title,"status":course.status,"knowledge_map":knowledge}
@router.get("")
def list_courses(db:Session=Depends(get_db)):
    return [{"id":c.id,"title":c.title,"description":c.description,"status":c.status,"created_at":c.created_at.isoformat()} for c in db.query(Course).order_by(Course.created_at.desc()).all()]
@router.get("/{cid}")
def get_course(cid:str,db:Session=Depends(get_db)):
    c=db.get(Course,cid)
    if not c: raise HTTPException(404,"Course not found")
    return {"id":c.id,"title":c.title,"description":c.description,"status":c.status,"knowledge_map":json.loads(c.knowledge_json or "{}"),"created_at":c.created_at.isoformat()}
@router.get("/{cid}/knowledge-map")
def map_course(cid:str,db:Session=Depends(get_db)):
    c=db.get(Course,cid)
    if not c: raise HTTPException(404,"Course not found")
    return json.loads(c.knowledge_json or "{}")
@router.delete("/{cid}")
def delete_course(cid:str,db:Session=Depends(get_db)):
    c=db.get(Course,cid)
    if not c: raise HTTPException(404,"Course not found")
    db.delete(c); db.commit(); shutil.rmtree(DATA_DIR/"courses"/cid,ignore_errors=True); return {"deleted":True}
