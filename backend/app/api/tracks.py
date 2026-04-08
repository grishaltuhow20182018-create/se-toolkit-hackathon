"""Track API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import List
from app.core.database import get_db
from app.models.models import Track
from app.schemas.schemas import TrackCreate, TrackUpdate, TrackResponse

router = APIRouter()


@router.get("/", response_model=List[TrackResponse])
async def get_tracks(
    skip: int = 0,
    limit: int = 100,
    genre: str | None = None,
    energy_min: int | None = None,
    energy_max: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Get all tracks with optional filters."""
    query = select(Track)
    
    if genre:
        query = query.where(Track.genre == genre)
    if energy_min:
        query = query.where(Track.energy_level >= energy_min)
    if energy_max:
        query = query.where(Track.energy_level <= energy_max)
    
    query = query.offset(skip).limit(limit).order_by(Track.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{track_id}", response_model=TrackResponse)
async def get_track(track_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific track by ID."""
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    return track


@router.post("/", response_model=TrackResponse, status_code=201)
async def create_track(track_data: TrackCreate, db: AsyncSession = Depends(get_db)):
    """Add a new track to the library."""
    track = Track(**track_data.model_dump())
    db.add(track)
    await db.flush()
    await db.refresh(track)
    return track


@router.put("/{track_id}", response_model=TrackResponse)
async def update_track(
    track_id: str,
    track_data: TrackUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update track metadata."""
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    update_data = track_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(track, field, value)
    
    await db.flush()
    await db.refresh(track)
    return track


@router.delete("/{track_id}", status_code=204)
async def delete_track(track_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a track from the library."""
    result = await db.execute(select(Track).where(Track.id == track_id))
    track = result.scalar_one_or_none()
    if not track:
        raise HTTPException(status_code=404, detail="Track not found")
    
    await db.execute(delete(Track).where(Track.id == track_id))
    await db.flush()
