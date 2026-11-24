from pathlib import Path
from app.core.config import DATA_DIR
from app.rag.vector_store import CourseVectorStore
def retrieve(course_id,query,k=5):
    folder=DATA_DIR/"courses"/course_id/"vectors"
    store=CourseVectorStore(folder)
    return store.search(query,k)
