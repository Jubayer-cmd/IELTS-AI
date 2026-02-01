from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings
from app.core.db import init_db
from app.core.memory import (
    close_async_memory,
    close_memory,
    init_async_memory,
    init_memory,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    init_db()  # SQLModel tables
    init_memory()  # LangGraph sync checkpointer + store tables
    await init_async_memory()  # LangGraph async checkpointer + store
    yield
    # Shutdown
    await close_async_memory()  # Close async connection pool
    close_memory()  # Close sync connection pool


app = FastAPI(
    title="IELTS Writing AI",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router with version prefix
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
