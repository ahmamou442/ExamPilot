from app.agents.prompts import COACH_PROMPT
from app.agents.runner import structured_agent
from app.schemas.schemas import StudyPlanOutput
async def create_plan(context,performance):
    out=await structured_agent("Study Coach",COACH_PROMPT,StudyPlanOutput,f"Course context: {context}\nPerformance: {performance}")
    if out: return out.model_dump()
    return {"summary":"Demo plan based on available results; API key enables tailored AI planning.","tasks":[{"title":"Review your lowest-scoring concept","description":"Revisit course material and attempt a fresh example.","concept_id":None,"priority":"high"},{"title":"Practice application","description":"Solve two problems without looking at the solution.","concept_id":None,"priority":"medium"},{"title":"Retest","description":"Take a short quiz to check retention.","concept_id":None,"priority":"medium"}]}
