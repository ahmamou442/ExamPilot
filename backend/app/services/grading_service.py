def grade(questions,answers):
    total=len(questions); correct=0; details=[]; by_concept={}
    for q in questions:
        qid=q.get("id"); answer=answers.get(qid); is_correct=answer==q.get("correct_answer")
        correct+=int(is_correct); concept=q.get("concept_id","unknown")
        bucket=by_concept.setdefault(concept,{"total":0,"correct":0}); bucket["total"]+=1; bucket["correct"]+=int(is_correct)
        details.append({"question_id":qid,"answer":answer,"correct_answer":q.get("correct_answer"),"correct":is_correct,"explanation":q.get("explanation"),"concept_id":concept})
    return {"score":correct,"total":total,"percentage":round(correct/total*100) if total else 0,"details":details,"concept_performance":by_concept}
