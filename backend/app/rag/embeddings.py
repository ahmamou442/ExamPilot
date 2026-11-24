import hashlib, re
import numpy as np
from app.core.config import API_KEY, EMBED_MODEL

def local_embed(text, dim=384):
    # Lightweight deterministic demo embedding; not semantic-grade.
    vec=np.zeros(dim,dtype="float32")
    for token in re.findall(r"[a-zA-Z0-9_]+",text.lower()):
        h=hashlib.blake2b(token.encode(),digest_size=8).digest(); n=int.from_bytes(h,"little")
        vec[n%dim]+=1 if (n>>8)&1 else -1
    norm=np.linalg.norm(vec)
    return vec/norm if norm else vec
def embed_texts(texts):
    if API_KEY:
        from openai import OpenAI
        client=OpenAI(api_key=API_KEY)
        res=client.embeddings.create(model=EMBED_MODEL,input=texts)
        return np.asarray([d.embedding for d in res.data],dtype="float32")
    return np.asarray([local_embed(t) for t in texts],dtype="float32")
def embed_query(text): return embed_texts([text])[0]
