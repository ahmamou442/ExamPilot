import json, uuid
from pathlib import Path
from app.core.config import DATA_DIR
from app.rag.pdf_extractor import extract_pdf
from app.rag.text_cleaner import clean_text
from app.rag.chunker import chunk_pages
from app.rag.vector_store import CourseVectorStore
from app.agents.analyst import analyze_course
async def process_course(db,course,uploads):
    folder=DATA_DIR/"courses"/course.id; (folder/"documents").mkdir(parents=True,exist_ok=True); (folder/"extracted").mkdir(parents=True,exist_ok=True)
    all_pages=[]
    for filename,data in uploads:
        pages=extract_pdf(data,filename)
        for p in pages: p["text"]=clean_text(p["text"])
        all_pages.extend(pages)
        (folder/"documents"/filename.replace("/","_")).write_bytes(data)
        from app.models.models import Document
        db.add(Document(id=str(uuid.uuid4()),course_id=course.id,filename=filename,file_path=str(folder/"documents"/filename.replace("/","_"))))
        (folder/"extracted"/(filename.replace("/","_")+".json")).write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding="utf-8")
    chunks=chunk_pages(all_pages)
    (folder/"corpus.json").write_text(json.dumps(chunks,ensure_ascii=False,indent=2),encoding="utf-8")
    CourseVectorStore(folder/"vectors").build(chunks)
    course.title=course.title or uploads[0][0].rsplit(".",1)[0]
    analysis=await analyze_course(course.title,chunks)
    course.knowledge_json=json.dumps(analysis,ensure_ascii=False)
    course.description=analysis.get("description","")
    course.status="ready"
    db.commit()
    return analysis
