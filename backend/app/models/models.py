from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from app.db.base import Base
def now(): return datetime.now(timezone.utc)
class Course(Base):
    __tablename__="courses"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    title: Mapped[str]=mapped_column(String, default="Untitled course")
    description: Mapped[str]=mapped_column(Text, default="")
    status: Mapped[str]=mapped_column(String, default="processing")
    knowledge_json: Mapped[str]=mapped_column(Text, default="{}")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Document(Base):
    __tablename__="documents"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    filename: Mapped[str]=mapped_column(String)
    file_path: Mapped[str]=mapped_column(String)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Diagnostic(Base):
    __tablename__="diagnostics"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id"))
    questions_json: Mapped[str]=mapped_column(Text)
    answers_json: Mapped[str]=mapped_column(Text, default="{}")
    results_json: Mapped[str]=mapped_column(Text, default="{}")
    status: Mapped[str]=mapped_column(String, default="active")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class TeachingSession(Base):
    __tablename__="teaching_sessions"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id"))
    concept_id: Mapped[str]=mapped_column(String)
    current_stage: Mapped[str]=mapped_column(String, default="motivate")
    data_json: Mapped[str]=mapped_column(Text, default="{}")
    status: Mapped[str]=mapped_column(String, default="active")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Exam(Base):
    __tablename__="exams"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id"))
    questions_json: Mapped[str]=mapped_column(Text)
    answers_json: Mapped[str]=mapped_column(Text, default="{}")
    results_json: Mapped[str]=mapped_column(Text, default="{}")
    status: Mapped[str]=mapped_column(String, default="active")
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class StudyPlan(Base):
    __tablename__="study_plans"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id"))
    plan_json: Mapped[str]=mapped_column(Text)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=now)
class Mastery(Base):
    __tablename__="mastery"
    id: Mapped[str]=mapped_column(String, primary_key=True)
    course_id: Mapped[str]=mapped_column(ForeignKey("courses.id"))
    concept_id: Mapped[str]=mapped_column(String)
    status: Mapped[str]=mapped_column(String, default="not_assessed")
    evidence_json: Mapped[str]=mapped_column(Text, default="[]")
