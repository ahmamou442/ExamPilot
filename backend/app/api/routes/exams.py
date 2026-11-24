import json
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Course,Exam
from app.services.exam_service import start,submit
router=APIRouter(prefix="/exams",tags=["exams"])
@router.post("/course/{cid}")
async def create_exam(cid:str,payload:dict={},db:Session=Depends(get_db)):
    course=db.get(Course,cid)
    if not course: raise HTTPException(404,"Course not found")
    count=max(5,min(10,int(payload.get("count",8))))
    e,qs=await start(db,course,count); return {"id":e.id,"questions":[{k:v for k,v in q.items() if k not in ["correct_answer","explanation"]} for q in qs]}
@router.get("/{eid}")
def get_exam(eid:str,db:Session=Depends(get_db)):
    e=db.get(Exam,eid)
    if not e: raise HTTPException(404,"Exam not found")
    qs=json.loads(e.questions_json); return {"id":e.id,"status":e.status,"questions":[{k:v for k,v in q.items() if k not in ["correct_answer","explanation"]} for q in qs]}
@router.post("/{eid}/submit")
def submit_exam(eid:str,payload:dict,db:Session=Depends(get_db)):
    e=db.get(Exam,eid)
    if not e: raise HTTPException(404,"Exam not found")
    result=submit(db,e,payload.get("answers",{})); return result
@router.get("/{eid}/results")
def exam_results(eid:str,db:Session=Depends(get_db)):
    e=db.get(Exam,eid)
    if not e: raise HTTPException(404,"Exam not found")
    if e.status!="graded": raise HTTPException(400,"Exam not graded yet")
    return json.loads(e.results_json)
