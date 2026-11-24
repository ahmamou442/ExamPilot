import json
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Course,Mastery,Exam,Diagnostic,TeachingSession
router=APIRouter(tags=["dashboard"])
@router.get("/dashboard")
def dashboard(db:Session=Depends(get_db)):
    courses=db.query(Course).order_by(Course.created_at.desc()).all(); rows=[]
    for c in courses:
        mastery=db.query(Mastery).filter_by(course_id=c.id).all(); exams=db.query(Exam).filter_by(course_id=c.id,status="graded").all()
        rows.append({"id":c.id,"title":c.title,"status":c.status,"concepts_count":sum(len(ch.get("concepts",[])) for ch in json.loads(c.knowledge_json or "{}").get("chapters",[])),"mastery":[{"concept_id":m.concept_id,"status":m.status} for m in mastery],"exam_count":len(exams)})
    return {"courses":rows,"demo_mode":__import__("app.core.config",fromlist=["DEMO_MODE"]).DEMO_MODE}
