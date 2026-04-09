"""Track API endpoints - user-scoped + shared default tracks."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, delete as sql_delete
from typing import List
from app.core.database import get_db
from app.models.models import Track, User
from app.schemas.schemas import TrackCreate, TrackUpdate, TrackResponse
from app.core.auth import get_current_user

# System user owns all seeded tracks
SYSTEM_USER_ID = "00000000-0000-0000-0000-000000000000"

router = APIRouter()


@router.get("/", response_model=List[TrackResponse])
async def get_tracks(skip: int = 0, limit: int = 200, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all tracks: user's own + shared default tracks."""
    result = await db.execute(
        select(Track)
        .where(or_(Track.user_id == current_user.id, Track.user_id == SYSTEM_USER_ID))
        .offset(skip)
        .limit(limit)
        .order_by(Track.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{track_id}", response_model=TrackResponse)
async def get_track(track_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific track."""
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.post("/", response_model=TrackResponse, status_code=201)
async def create_track(track_data: TrackCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new track for the current user."""
    track = Track(user_id=current_user.id, **track_data.model_dump())
    db.add(track)
    await db.flush()
    await db.refresh(track)
    return track


@router.put("/{track_id}", response_model=TrackResponse)
async def update_track(track_id: str, track_data: TrackUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update a track owned by the current user."""
    result = await db.execute(select(Track).where(Track.id == track_id, Track.user_id == current_user.id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found or not yours")

    update_data = track_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(track, key, value)

    await db.flush()
    await db.refresh(track)
    return track


@router.delete("/{track_id}", status_code=204)
async def delete_track(track_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a track owned by the current user (cannot delete shared tracks)."""
    result = await db.execute(select(Track).where(Track.id == track_id, Track.user_id == current_user.id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found or cannot delete shared tracks")

    await db.execute(sql_delete(Track).where(Track.id == track_id))
    await db.flush()
