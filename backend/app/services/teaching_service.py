import json, uuid
from app.models.models import TeachingSession
from app.rag.retriever import retrieve
from app.agents.tutor import teach_stage
STAGES=["motivate","establish","connect","verify"]
def context_for(course_id,concept):
    chunks=retrieve(course_id,concept,5); return "\n\n".join(c["text"] for c in chunks),chunks
async def create(db,course_id,concept):
    context,chunks=context_for(course_id,concept); stage="motivate"; content=await teach_stage(concept,stage,context)
    data={"history":[{"stage":stage,"content":content["content"]}],"context_refs":[{"document_name":c["document_name"],"page":c["page_start"]} for c in chunks]}
    s=TeachingSession(id=str(uuid.uuid4()),course_id=course_id,concept_id=concept,current_stage=stage,data_json=json.dumps(data)); db.add(s); db.commit(); return s,content
async def advance(db,s):
    data=json.loads(s.data_json); idx=STAGES.index(s.current_stage)
    if idx>=len(STAGES)-1: s.status="completed"; db.commit(); return {"content":"Session complete. Start a fresh verification or examination to continue."}
    stage=STAGES[idx+1]; context,_=context_for(s.course_id,s.concept_id); previous=json.dumps(data["history"][-2:])
    content=await teach_stage(s.concept_id,stage,context,previous); s.current_stage=stage; data["history"].append({"stage":stage,"content":content["content"]}); s.data_json=json.dumps(data); db.commit(); return content
async def check(db,s,answer):
    data=json.loads(s.data_json); data.setdefault("checks",[]).append(answer); s.data_json=json.dumps(data); db.commit()
    # MVP verification is evidence collection; do not claim AI evaluated short answer.
    return {"received":True,"feedback":"Answer recorded. Continue the session or use an exam for scored evidence."}
