from __future__ import annotations


def grade(questions: list[dict], answers: dict[str, str]) -> dict:
    """Grade an assessment deterministically and report per-concept evidence."""
    total = len(questions)
    correct = 0
    details = []
    by_concept: dict[str, dict[str, int]] = {}
    for question in questions:
        question_id = question.get("id")
        answer = answers.get(question_id)
        is_correct = answer is not None and answer == question.get("correct_answer")
        correct += int(is_correct)
        concept = str(question.get("concept_id") or "unknown")
        bucket = by_concept.setdefault(concept, {"total": 0, "correct": 0})
        bucket["total"] += 1
        bucket["correct"] += int(is_correct)
        details.append({"question_id": question_id, "answer": answer, "correct_answer": question.get("correct_answer"), "correct": is_correct, "explanation": question.get("explanation"), "concept_id": concept})
    return {"score": correct, "total": total, "percentage": round(correct / total * 100) if total else 0, "details": details, "concept_performance": by_concept}
