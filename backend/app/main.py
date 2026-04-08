"""DJ Setlist AI - Main Application Entry Point."""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import tracks, playlists, setlists, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan event handler."""
    # Startup: Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Cleanup resources
    await engine.dispose()

app = FastAPI(
    title="DJ Setlist AI",
    description="AI-powered DJ setlist generator with seamless track matching",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tracks.router, prefix="/api/tracks", tags=["tracks"])
app.include_router(playlists.router, prefix="/api/playlists", tags=["playlists"])
app.include_router(setlists.router, prefix="/api/setlists", tags=["setlists"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "DJ Setlist AI"}
