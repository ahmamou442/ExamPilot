import json, uuid
from app.models.models import Diagnostic
from app.rag.retriever import retrieve
from app.agents.tutor import generate_questions
from app.services.grading_service import grade
from app.services.mastery_service import update_mastery
def flatten_concepts(knowledge):
    return [c for ch in knowledge.get("chapters",[]) for c in ch.get("concepts",[])]
async def start(db,course):
    knowledge=json.loads(course.knowledge_json or "{}")
    concepts=flatten_concepts(knowledge); ctx=retrieve(course.id,"course fundamentals and learning objectives",5)
    text="\n\n".join(x["text"] for x in ctx)
    questions=await generate_questions(text,concepts,5,"diagnostic")
    for q in questions: q["id"]=str(uuid.uuid4())
    obj=Diagnostic(id=str(uuid.uuid4()),course_id=course.id,questions_json=json.dumps(questions),answers_json="{}",status="active")
    db.add(obj); db.commit(); return obj,questions
def submit(db,obj,answer):
    questions=json.loads(obj.questions_json); answers=json.loads(obj.answers_json); answers.update(answer)
    if len(answers)>=len(questions):
        obj.status="completed"; result=grade(questions,answers); obj.results_json=json.dumps(result); update_mastery(db,obj.course_id,result["concept_performance"])
    obj.answers_json=json.dumps(answers); db.commit(); return answers, (json.loads(obj.results_json) if obj.status=="completed" else None)
