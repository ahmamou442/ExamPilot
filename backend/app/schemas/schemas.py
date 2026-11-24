from pydantic import BaseModel, Field
from typing import Optional
class Concept(BaseModel):
    name:str
    definition:str
    learning_objective:str
    prerequisites:list[str]=[]
    misconceptions:list[str]=[]
    source_refs:list[str]=[]
class Chapter(BaseModel):
    title:str
    description:str=""
    concepts:list[Concept]=[]
class CourseAnalysis(BaseModel):
    title:str
    description:str=""
    chapters:list[Chapter]=[]
class Question(BaseModel):
    question:str
    options:dict[str,str]
    correct_answer:str
    explanation:str
    concept_id:str
    difficulty:str="medium"
    source_refs:list[str]=[]
class QuestionsOutput(BaseModel):
    questions:list[Question]
class TeachStageOutput(BaseModel):
    content:str
    check_question:Optional[Question]=None
class PlanTask(BaseModel):
    title:str
    description:str
    concept_id:str|None=None
    priority:str="medium"
class StudyPlanOutput(BaseModel):
    summary:str
    tasks:list[PlanTask]=Field(default_factory=list)
