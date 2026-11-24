from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.base import Base
from app.db.session import engine
from app.models import models
from app.api.router import router
from app.core.config import DEMO_MODE
Base.metadata.create_all(bind=engine)
app=FastAPI(title="ExamPilot API",version="0.1.0",description="ExamPilot hackathon MVP")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router)
@app.get("/health")
def health(): return {"status":"ok","demo_mode":DEMO_MODE}
