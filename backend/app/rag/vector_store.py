import json
from pathlib import Path
import faiss, numpy as np
from app.rag.embeddings import embed_texts, embed_query
class CourseVectorStore:
    def __init__(self,folder:Path): self.folder=folder; self.folder.mkdir(parents=True,exist_ok=True); self.index_path=folder/"index.faiss"; self.chunks_path=folder/"chunks.json"
    def build(self,chunks):
        vectors=embed_texts([c["text"] for c in chunks]); vectors=np.ascontiguousarray(vectors,dtype="float32")
        faiss.normalize_L2(vectors); self.index=faiss.IndexFlatIP(vectors.shape[1]); self.index.add(vectors); self.chunks=chunks
        faiss.write_index(self.index,str(self.index_path)); self.chunks_path.write_text(json.dumps(chunks,ensure_ascii=False,indent=2),encoding="utf-8")
    def load(self):
        if not self.index_path.exists() or not self.chunks_path.exists(): raise FileNotFoundError("Vector index not found")
        self.index=faiss.read_index(str(self.index_path)); self.chunks=json.loads(self.chunks_path.read_text(encoding="utf-8"))
    def search(self,query,k=5):
        if not hasattr(self,"index"): self.load()
        q=np.asarray([embed_query(query)],dtype="float32"); faiss.normalize_L2(q); scores,idx=self.index.search(q,min(k,len(self.chunks)))
        return [{**self.chunks[int(i)],"score":float(s)} for s,i in zip(scores[0],idx[0]) if i>=0]
