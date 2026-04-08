"""AI-powered setlist generation endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import Track, Playlist, Setlist
from app.schemas.schemas import (
    SetlistGenerationRequest,
    SetlistGenerationResponse,
    SetlistResponse,
    NextTrackRequest,
    NextTrackResponse,
    TrackResponse,
)
from app.agents.setlist_agent import generate_setlist_with_ai, recommend_next_track

router = APIRouter()


@router.post("/generate-setlist", response_model=SetlistGenerationResponse)
async def generate_setlist(
    request: SetlistGenerationRequest,
    db: AsyncSession = Depends(get_db),
):
    """Generate an AI-optimized DJ setlist."""
    # Get tracks from playlist or specific track IDs
    tracks = []
    if request.playlist_id:
        from app.models.models import PlaylistTrack
        pt_result = await db.execute(
            select(Track)
            .join(PlaylistTrack, Track.id == PlaylistTrack.track_id)
            .where(PlaylistTrack.playlist_id == request.playlist_id)
            .order_by(PlaylistTrack.position)
        )
        tracks = pt_result.scalars().all()
    elif request.track_ids:
        result = await db.execute(select(Track).where(Track.id.in_(request.track_ids)))
        tracks = result.scalars().all()
    else:
        # Get all tracks
        result = await db.execute(select(Track).limit(100))
        tracks = result.scalars().all()
    
    if not tracks:
        raise HTTPException(status_code=400, detail="No tracks available for setlist generation")
    
    # Call AI agent
    setlist_data = await generate_setlist_with_ai(
        tracks=tracks,
        target_duration_minutes=request.target_duration_minutes,
        vibe=request.vibe,
        starting_track_id=request.starting_track_id,
        max_tracks=request.max_tracks,
    )
    
    # Save to database
    setlist = Setlist(
        name=f"AI Setlist - {request.vibe or 'Mixed'}",
        description=f"AI-generated setlist with {len(setlist_data['track_order'])} tracks",
        target_duration_minutes=request.target_duration_minutes,
        vibe=request.vibe,
        track_order=setlist_data["track_order"],
        ai_notes=setlist_data.get("ai_notes"),
    )
    db.add(setlist)
    await db.flush()
    await db.refresh(setlist)
    
    return SetlistGenerationResponse(
        setlist=SetlistResponse.model_validate(setlist),
        suggestions=setlist_data.get("suggestions", []),
        compatibility_scores=setlist_data.get("compatibility_scores", {}),
    )


@router.post("/next-track", response_model=NextTrackResponse)
async def get_next_track_recommendation(
    request: NextTrackRequest,
    db: AsyncSession = Depends(get_db),
):
    """Get AI recommendation for the next track to play."""
    # Get current track
    current_result = await db.execute(select(Track).where(Track.id == request.current_track_id))
    current_track = current_result.scalar_one_or_none()
    if not current_track:
        raise HTTPException(status_code=404, detail="Current track not found")
    
    # Get available tracks
    available_tracks = []
    if request.playlist_id:
        from app.models.models import PlaylistTrack
        pt_result = await db.execute(
            select(Track)
            .join(PlaylistTrack, Track.id == PlaylistTrack.track_id)
            .where(PlaylistTrack.playlist_id == request.playlist_id)
        )
        available_tracks = pt_result.scalars().all()
    elif request.available_track_ids:
        result = await db.execute(select(Track).where(Track.id.in_(request.available_track_ids)))
        available_tracks = result.scalars().all()
    else:
        result = await db.execute(select(Track).limit(100))
        available_tracks = result.scalars().all()
    
    # Filter out current track
    available_tracks = [t for t in available_tracks if t.id != request.current_track_id]
    
    if not available_tracks:
        raise HTTPException(status_code=400, detail="No available tracks for recommendation")
    
    # Get AI recommendation
    recommendation = await recommend_next_track(current_track, available_tracks)
    
    return NextTrackResponse(**recommendation)
