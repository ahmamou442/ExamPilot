from fastapi import APIRouter
from app.api.routes import courses,diagnostics,teaching,exams,dashboard
router=APIRouter(prefix="/api")
router.include_router(courses.router); router.include_router(diagnostics.router); router.include_router(teaching.router); router.include_router(exams.router); router.include_router(dashboard.router)
