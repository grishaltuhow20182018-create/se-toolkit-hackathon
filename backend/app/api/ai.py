"""AI-powered setlist generation endpoints - user-scoped."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import Track, Playlist, Setlist, User, PlaylistTrack
from app.schemas.schemas import (
    SetlistGenerationRequest,
    SetlistGenerationResponse,
    SetlistResponse,
    NextTrackRequest,
    NextTrackResponse,
    TrackResponse,
)
from app.agents.setlist_agent import generate_setlist_with_ai, recommend_next_track
from app.core.auth import get_current_user

router = APIRouter()


@router.post("/generate-setlist", response_model=SetlistGenerationResponse)
async def generate_setlist(
    request: SetlistGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate an AI-optimized DJ setlist for the current user."""
    tracks = []
    if request.playlist_id:
        pt_result = await db.execute(
            select(Track)
            .join(PlaylistTrack, Track.id == PlaylistTrack.track_id)
            .join(Playlist, Playlist.id == PlaylistTrack.playlist_id)
            .where(PlaylistTrack.playlist_id == request.playlist_id, Playlist.user_id == current_user.id)
            .order_by(PlaylistTrack.position)
        )
        tracks = pt_result.scalars().all()
    elif request.track_ids:
        result = await db.execute(select(Track).where(Track.id.in_(request.track_ids), Track.user_id == current_user.id))
        tracks = result.scalars().all()
    else:
        result = await db.execute(select(Track).where(Track.user_id == current_user.id).limit(100))
        tracks = result.scalars().all()

    if not tracks:
        raise HTTPException(status_code=400, detail="No tracks available for setlist generation")

    setlist_data = await generate_setlist_with_ai(
        tracks=tracks,
        target_duration_minutes=request.target_duration_minutes,
        vibe=request.vibe,
        starting_track_id=request.starting_track_id,
        max_tracks=request.max_tracks,
    )

    setlist = Setlist(
        user_id=current_user.id,
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
    current_user: User = Depends(get_current_user),
):
    """Get AI recommendation for the next track to play."""
    current_result = await db.execute(select(Track).where(Track.id == request.current_track_id, Track.user_id == current_user.id))
    current_track = current_result.scalar_one_or_none()
    if not current_track:
        raise HTTPException(status_code=404, detail="Current track not found")

    available_tracks = []
    if request.playlist_id:
        pt_result = await db.execute(
            select(Track)
            .join(PlaylistTrack, Track.id == PlaylistTrack.track_id)
            .join(Playlist, Playlist.id == PlaylistTrack.playlist_id)
            .where(PlaylistTrack.playlist_id == request.playlist_id, Playlist.user_id == current_user.id)
        )
        available_tracks = pt_result.scalars().all()
    elif request.available_track_ids:
        result = await db.execute(select(Track).where(Track.id.in_(request.available_track_ids), Track.user_id == current_user.id))
        available_tracks = result.scalars().all()
    else:
        result = await db.execute(select(Track).where(Track.user_id == current_user.id).limit(100))
        available_tracks = result.scalars().all()

    available_tracks = [t for t in available_tracks if t.id != request.current_track_id]

    if not available_tracks:
        raise HTTPException(status_code=400, detail="No available tracks for recommendation")

    recommendation = await recommend_next_track(current_track, available_tracks)

    return NextTrackResponse(**recommendation)
