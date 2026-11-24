import json,uuid
from app.models.models import StudyPlan
from app.agents.coach import create_plan
from app.rag.retriever import retrieve
async def generate(db,course,performance):
    chunks=retrieve(course.id,"course learning objectives and weak concepts",5); context="\n\n".join(c["text"] for c in chunks)
    plan=await create_plan(context,performance); obj=StudyPlan(id=str(uuid.uuid4()),course_id=course.id,plan_json=json.dumps(plan)); db.add(obj); db.commit(); return plan
