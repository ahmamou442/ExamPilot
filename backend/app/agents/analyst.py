import json
from app.agents.prompts import ANALYST_PROMPT
from app.agents.runner import structured_agent
from app.schemas.schemas import CourseAnalysis
async def analyze_course(title,chunks):
    context="\n\n".join(f"[{c['document_name']} p.{c['page_start']}] {c['text']}" for c in chunks[:60])
    output=await structured_agent("Course Analyst",ANALYST_PROMPT,CourseAnalysis,f"Course title: {title}\n\nCourse context:\n{context}")
    if output: return output.model_dump()
    # Demo mode fallback: meaningful but explicitly approximate structure from text
    sample=chunks[:12]; concepts=[]
    for i,c in enumerate(sample[:8]):
        txt=c['text'][:240].replace("\n"," ")
        if len(txt)<35: continue
        name=(txt.split(".")[0][:90] or f"Course concept {i+1}")
        concepts.append({"name":name,"definition":txt,"learning_objective":f"Explain and apply: {name}","prerequisites":[],"misconceptions":[],"source_refs":[f"{c['document_name']} page {c['page_start']}" ]})
    return {"title":title,"description":"Demo-mode analysis generated from extracted text; configure OPENAI_API_KEY for full AI analysis.","chapters":[{"title":"Extracted course concepts","description":"Approximate structure in demo mode","concepts":concepts}]}
