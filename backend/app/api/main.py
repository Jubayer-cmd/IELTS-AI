"""
API Router aggregation.

Following FastAPI full-stack template pattern:
All route modules are imported and included here,
then this router is mounted in the main app.
"""
from fastapi import APIRouter

from app.api.routes import auth, users, writing

api_router = APIRouter()

# Auth routes (login, register)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# User management routes
api_router.include_router(users.router, prefix="/users", tags=["users"])

# IELTS writing/evaluation routes
api_router.include_router(writing.router, prefix="/writing", tags=["writing"])
