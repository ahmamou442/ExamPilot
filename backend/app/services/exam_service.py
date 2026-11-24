import json, uuid
from app.models.models import Exam
from app.services.diagnostic_service import flatten_concepts
from app.rag.retriever import retrieve
from app.agents.tutor import generate_questions
from app.services.grading_service import grade
from app.services.mastery_service import update_mastery
async def start(db,course,count=8):
    concepts=flatten_concepts(json.loads(course.knowledge_json or "{}")); chunks=retrieve(course.id,"exam concepts and applications",6); ctx="\n\n".join(c["text"] for c in chunks)
    qs=await generate_questions(ctx,concepts,count,"exam")
    for q in qs: q["id"]=str(uuid.uuid4())
    e=Exam(id=str(uuid.uuid4()),course_id=course.id,questions_json=json.dumps(qs),status="active"); db.add(e); db.commit(); return e,qs
def submit(db,e,answers):
    if e.status=="graded": return json.loads(e.results_json)
    qs=json.loads(e.questions_json); result=grade(qs,answers); e.answers_json=json.dumps(answers); e.results_json=json.dumps(result); e.status="graded"; update_mastery(db,e.course_id,result["concept_performance"]); db.commit(); return result
