
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Course, Diagnostic
from app.services.diagnostic_service import start, submit

router = APIRouter(tags=["diagnostics"])


@router.post("/courses/{cid}/diagnostic")
async def start_diag(cid: str, db: Session = Depends(get_db)):
    course = db.get(Course, cid)

    if not course or course.status != "ready":
        raise HTTPException(404, "Course unavailable")

    obj, questions = await start(db, course)

    public_questions = [
        {
            key: value
            for key, value in question.items()
            if key not in ["correct_answer", "explanation"]
        }
        for question in questions
    ]

    return {
        "id": obj.id,
        "questions": public_questions,
        "status": obj.status
    }


@router.get("/diagnostics/{did}")
def get_diag(did: str, db: Session = Depends(get_db)):
    obj = db.get(Diagnostic, did)

    if not obj:
        raise HTTPException(404, "Diagnostic not found")

    questions = json.loads(obj.questions_json)
    answers = json.loads(obj.answers_json)

    public_questions = [
        {
            key: value
            for key, value in question.items()
            if key not in ["correct_answer", "explanation"]
        }
        for question in questions
    ]

    return {
        "id": obj.id,
        "status": obj.status,
        "questions": public_questions,
        "answers": answers
    }


@router.post("/diagnostics/{did}/answer")
def answer(
    did: str,
    payload: dict,
    db: Session = Depends(get_db)
):
    obj = db.get(Diagnostic, did)

    if not obj:
        raise HTTPException(404, "Diagnostic not found")

    if obj.status != "active":
        raise HTTPException(400, "Assessment already completed")

    question_id = payload.get("question_id")
    selected_answer = payload.get("answer")

    questions = json.loads(obj.questions_json)

    if not any(q["id"] == question_id for q in questions):
        raise HTTPException(400, "Invalid question ID")

    answers, result = submit(
        db,
        obj,
        {question_id: selected_answer}
    )

    return {
        "saved": True,
        "completed": result is not None,
        "results": result
    }


@router.get("/diagnostics/{did}/results")
def results(did: str, db: Session = Depends(get_db)):
    obj = db.get(Diagnostic, did)

    if not obj:
        raise HTTPException(404, "Diagnostic not found")

    if obj.status != "completed":
        raise HTTPException(400, "Assessment incomplete")

    return json.loads(obj.results_json)
