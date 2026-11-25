import json
import uuid

from app.models.models import Diagnostic
from app.rag.retriever import retrieve
from app.agents.tutor import generate_questions
from app.services.grading_service import grade
from app.services.mastery_service import update_mastery


def flatten_concepts(knowledge):
    return [concept for chapter in knowledge.get("chapters", []) for concept in chapter.get("concepts", [])]


async def start(db, course):
    knowledge = json.loads(course.knowledge_json or "{}")
    concepts = flatten_concepts(knowledge)
    context = retrieve(course.id, "course fundamentals and learning objectives", 5)
    text = "\n\n".join(chunk["text"] for chunk in context)
    questions = await generate_questions(text, concepts, 5, "diagnostic")
    for question in questions:
        question["id"] = str(uuid.uuid4())
    obj = Diagnostic(id=str(uuid.uuid4()), course_id=course.id, questions_json=json.dumps(questions), answers_json="{}", status="active")
    db.add(obj)
    db.commit()
    return obj, questions


def submit(db, obj, answer):
    questions = json.loads(obj.questions_json or "[]")
    answers = json.loads(obj.answers_json or "{}")
    answers.update(answer)
    # Count only known question IDs; duplicate requests cannot complete an assessment early.
    expected_ids = {question.get("id") for question in questions}
    if expected_ids and expected_ids.issubset(answers):
        obj.status = "completed"
        result = grade(questions, answers)
        obj.results_json = json.dumps(result)
        update_mastery(db, obj.course_id, result["concept_performance"])
    obj.answers_json = json.dumps(answers)
    db.commit()
    return answers, json.loads(obj.results_json or "{}") if obj.status == "completed" else None
