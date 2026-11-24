from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATA_DIR
DB_URL=f"sqlite:///{DATA_DIR / 'app.db'}"
engine=create_engine(DB_URL, connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(bind=engine, autoflush=False, autocommit=False)
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
