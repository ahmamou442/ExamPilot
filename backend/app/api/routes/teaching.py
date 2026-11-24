import json
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Course,TeachingSession
from app.services.teaching_service import create,advance,check
router=APIRouter(prefix="/teaching-sessions",tags=["teaching"])
@router.post("")
async def create_session(payload:dict,db:Session=Depends(get_db)):
    cid=payload.get("course_id"); concept=payload.get("concept_id")
    course=db.get(Course,cid)
    if not course or not concept: raise HTTPException(400,"course_id and concept_id required")
    s,content=await create(db,cid,concept); return {"id":s.id,"stage":s.current_stage,"content":content["content"],"status":s.status}
@router.get("/{sid}")
def get_session(sid:str,db:Session=Depends(get_db)):
    s=db.get(TeachingSession,sid)
    if not s: raise HTTPException(404,"Session not found")
    return {"id":s.id,"course_id":s.course_id,"concept_id":s.concept_id,"stage":s.current_stage,"status":s.status,"history":json.loads(s.data_json).get("history",[])}
@router.post("/{sid}/advance")
async def advance_session(sid:str,db:Session=Depends(get_db)):
    s=db.get(TeachingSession,sid)
    if not s: raise HTTPException(404,"Session not found")
    if s.status=="completed": return {"content":"Session complete","status":"completed"}
    content=await advance(db,s); return {"stage":s.current_stage,"content":content.get("content"),"check_question":content.get("check_question"),"status":s.status}
@router.post("/{sid}/check")
async def check_answer(sid:str,payload:dict,db:Session=Depends(get_db)):
    s=db.get(TeachingSession,sid)
    if not s: raise HTTPException(404,"Session not found")
    return await check(db,s,payload.get("answer",{}))
