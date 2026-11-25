from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import DEMO_MODE
from app.db.session import get_db
from app.models.models import Course, Exam, Mastery

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)):
    """Return course progress summaries used by the home workspace."""
    courses = db.query(Course).order_by(Course.created_at.desc()).all()
    rows = []
    for course in courses:
        try:
            knowledge = json.loads(course.knowledge_json or "{}")
        except (TypeError, ValueError):
            knowledge = {}
        mastery = db.query(Mastery).filter_by(course_id=course.id).all()
        exams_count = db.query(Exam).filter_by(course_id=course.id, status="graded").count()
        rows.append({
            "id": course.id,
            "title": course.title,
            "status": course.status,
            "concepts_count": sum(len(chapter.get("concepts", [])) for chapter in knowledge.get("chapters", []) if isinstance(chapter, dict)),
            "mastery": [{"concept_id": row.concept_id, "status": row.status} for row in mastery],
            "exams_count": exams_count,
        })
    return {"courses": rows, "demo_mode": DEMO_MODE}
