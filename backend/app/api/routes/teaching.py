import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Course, TeachingSession
from app.services.teaching_service import advance, check, create

router = APIRouter(prefix="/teaching-sessions", tags=["teaching"])


class CreateTeachingSession(BaseModel):
    course_id: str
    concept_id: str


class TeachingCheck(BaseModel):
    answer: dict = Field(default_factory=dict)


def serialize(session: TeachingSession):
    data = json.loads(session.data_json or "{}")
    history = data.get("history", [])
    return {"id": session.id, "course_id": session.course_id, "concept_id": session.concept_id, "stage": session.current_stage, "status": session.status, "history": history, "content": history[-1].get("content", "") if history else ""}


@router.post("")
async def create_session(payload: CreateTeachingSession, db: Session = Depends(get_db)):
    course = db.get(Course, payload.course_id)
    if not course or course.status != "ready":
        raise HTTPException(status_code=404, detail="Ready course not found.")
    concepts = [concept for chapter in json.loads(course.knowledge_json or "{}").get("chapters", []) for concept in chapter.get("concepts", [])]
    if concepts and payload.concept_id not in {concept.get("id", concept.get("name")) for concept in concepts} and payload.concept_id not in {concept.get("name") for concept in concepts}:
        # Knowledge maps may use names as IDs; accept those while rejecting arbitrary course IDs.
        if payload.concept_id not in {concept.get("name") for concept in concepts}:
            raise HTTPException(status_code=404, detail="Concept not found in this course.")
    session, content = await create(db, payload.course_id, payload.concept_id)
    return {"id": session.id, "course_id": session.course_id, "concept_id": session.concept_id, "stage": session.current_stage, "content": content.get("content", ""), "status": session.status}


@router.get("/{sid}")
def get_session(sid: str, db: Session = Depends(get_db)):
    session = db.get(TeachingSession, sid)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return serialize(session)


@router.post("/{sid}/advance")
async def advance_session(sid: str, db: Session = Depends(get_db)):
    session = db.get(TeachingSession, sid)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status == "completed":
        return {**serialize(session), "content": "Session complete"}
    content = await advance(db, session)
    return {"id": session.id, "stage": session.current_stage, "content": content.get("content", ""), "check_question": content.get("check_question"), "status": session.status}


@router.post("/{sid}/check")
async def check_answer(sid: str, payload: TeachingCheck, db: Session = Depends(get_db)):
    session = db.get(TeachingSession, sid)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if session.status == "completed":
        raise HTTPException(status_code=400, detail="Learning session is already complete.")
    return await check(db, session, payload.answer)
