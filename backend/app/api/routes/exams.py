import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.models import Course, Exam
from app.services.exam_service import start, submit

router = APIRouter(prefix="/exams", tags=["exams"])


class ExamRequest(BaseModel):
    count: int = Field(default=8, ge=5, le=10)


class ExamSubmission(BaseModel):
    answers: dict[str, str] = Field(default_factory=dict)


def public_questions(raw: str):
    questions = json.loads(raw or "[]")
    return [{key: value for key, value in question.items() if key not in {"correct_answer", "explanation"}} for question in questions]


@router.post("/course/{cid}")
async def create_exam(cid: str, payload: ExamRequest = ExamRequest(), db: Session = Depends(get_db)):
    course = db.get(Course, cid)
    if not course or course.status != "ready":
        raise HTTPException(status_code=404, detail="Ready course not found.")
    exam, questions = await start(db, course, payload.count)
    return {"id": exam.id, "questions": [{key: value for key, value in question.items() if key not in {"correct_answer", "explanation"}} for question in questions]}


@router.get("/{eid}")
def get_exam(eid: str, db: Session = Depends(get_db)):
    exam = db.get(Exam, eid)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")
    return {"id": exam.id, "status": exam.status, "questions": public_questions(exam.questions_json)}


@router.post("/{eid}/submit")
def submit_exam(eid: str, payload: ExamSubmission, db: Session = Depends(get_db)):
    exam = db.get(Exam, eid)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")
    questions = json.loads(exam.questions_json or "[]")
    valid_ids = {question.get("id") for question in questions}
    if set(payload.answers) - valid_ids:
        raise HTTPException(status_code=400, detail="Submission contains an unknown question.")
    for question in questions:
        answer = payload.answers.get(question.get("id"))
        if answer is not None and answer not in question.get("options", {}):
            raise HTTPException(status_code=400, detail="Submission contains an invalid answer option.")
    return submit(db, exam, payload.answers)


@router.get("/{eid}/results")
def exam_results(eid: str, db: Session = Depends(get_db)):
    exam = db.get(Exam, eid)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found.")
    if exam.status != "graded":
        raise HTTPException(status_code=400, detail="Exam not graded yet.")
    return json.loads(exam.results_json or "{}")
