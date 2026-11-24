# Architecture

Frontend → FastAPI routes → services → (Agents / RAG / SQLite).

- SQLite holds course/document metadata, diagnostic/exam/session JSON and mastery.
- PDFs and extracted chunks are stored in per-course folders.
- FAISS per course stores embeddings; index can be regenerated from chunk data.
- Three AI agents: Analyst, Tutor, Coach. Python orchestrates the workflow.
- Deterministic grading is server-side.
