import json
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Course, Diagnostic
from app.services.diagnostic_service import start, submit

router = APIRouter(tags=["diagnostics"])


class DiagnosticAnswer(BaseModel):
    question_id: str
    answer: str


@router.post("/courses/{cid}/diagnostic")
async def start_diagnostic(cid: str, db: Session = Depends(get_db)):
    course = db.get(Course, cid)
    if not course or course.status != "ready":
        raise HTTPException(status_code=404, detail="Course unavailable.")
    obj, questions = await start(db, course)
    public = [{key: value for key, value in question.items() if key not in {"correct_answer", "explanation"}} for question in questions]
    return {"id": obj.id, "questions": public, "status": obj.status}


@router.get("/diagnostics/{did}")
def get_diagnostic(did: str, db: Session = Depends(get_db)):
    obj = db.get(Diagnostic, did)
    if not obj:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    questions = json.loads(obj.questions_json or "[]")
    public = [{key: value for key, value in question.items() if key not in {"correct_answer", "explanation"}} for question in questions]
    return {"id": obj.id, "status": obj.status, "questions": public, "answers": json.loads(obj.answers_json or "{}")}


@router.post("/diagnostics/{did}/answer")
def answer_diagnostic(did: str, payload: DiagnosticAnswer, db: Session = Depends(get_db)):
    obj = db.get(Diagnostic, did)
    if not obj:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    if obj.status != "active":
        raise HTTPException(status_code=400, detail="Assessment already completed.")
    questions = json.loads(obj.questions_json or "[]")
    question = next((item for item in questions if item.get("id") == payload.question_id), None)
    if question is None or payload.answer not in question.get("options", {}):
        raise HTTPException(status_code=400, detail="Invalid question or answer option.")
    answers, result = submit(db, obj, {payload.question_id: payload.answer})
    return {"saved": True, "completed": result is not None, "results": result}


@router.get("/diagnostics/{did}/results")
def diagnostic_results(did: str, db: Session = Depends(get_db)):
    obj = db.get(Diagnostic, did)
    if not obj:
        raise HTTPException(status_code=404, detail="Diagnostic not found.")
    if obj.status != "completed":
        raise HTTPException(status_code=400, detail="Assessment incomplete.")
    return json.loads(obj.results_json or "{}")
