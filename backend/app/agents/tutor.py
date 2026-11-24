import json
from app.agents.prompts import TUTOR_PROMPT
from app.agents.runner import structured_agent
from app.schemas.schemas import QuestionsOutput, TeachStageOutput
async def generate_questions(context,concepts,count=5,kind="diagnostic"):
    prompt=f"Generate {count} {kind} MCQs. Map each to one concept ID/name from this list: {concepts}. Use A-D options, one correct answer, explanation and source refs. Course context:\n{context}"
    out=await structured_agent("Learning Tutor",TUTOR_PROMPT,QuestionsOutput,prompt)
    if out: return [q.model_dump() for q in out.questions]
    concepts_list=concepts if isinstance(concepts,list) else []
    questions=[]
    for i in range(count):
        c=concepts_list[i%len(concepts_list)] if concepts_list else {"name":"Course concepts"}
        cname=c.get("name","Course concepts")
        questions.append({"question":f"Which option best describes the concept: {cname}? (Demo question; replace with AI-generated question when API key is configured.)","options":{"A":f"A description related to {cname}","B":"An unrelated idea","C":"The opposite of the concept","D":"None of these"},"correct_answer":"A","explanation":f"This demo fallback is illustrative, not a genuine assessment of {cname}.","concept_id":cname,"difficulty":"easy","source_refs":[]})
    return questions
async def teach_stage(concept,stage,context,previous=""):
    prompt=f"Concept: {concept}\nStage: {stage}\nCourse context: {context}\nPrevious learner/session context: {previous}\nWrite concise stage content. For verify, include a new MCQ."
    out=await structured_agent("Learning Tutor",TUTOR_PROMPT,TeachStageOutput,prompt)
    if out: return out.model_dump()
    messages={"motivate":f"Imagine a problem where {concept} is needed. What would you need to understand to solve it?","establish":f"Let's establish the core idea of {concept} from the course.\n\n{context[:1200]}","connect":f"Connect {concept} to the ideas you already know. Consider how the concepts in the retrieved course material fit together.\n\n{context[:1000]}","verify":f"Demo-mode verification: explain or choose how {concept} works using the course material. Configure OPENAI_API_KEY for generated verification questions."}
    return {"content":messages.get(stage,"Review the concept."),"check_question":None}
