import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
BASE_DIR=Path(__file__).resolve().parents[2]
DATA_DIR=Path(os.getenv("DATA_DIR", str(BASE_DIR / "data"))).resolve()
API_KEY=os.getenv("OPENAI_API_KEY", "").strip()
MODEL=os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
EMBED_MODEL=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
MAX_UPLOAD_MB=int(os.getenv("MAX_UPLOAD_MB", "30"))
DEMO_MODE=not bool(API_KEY)
DATA_DIR.mkdir(parents=True, exist_ok=True)
