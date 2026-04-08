"""Playlist API endpoints - user-scoped."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete
from typing import List
from app.core.database import get_db
from app.models.models import Playlist, PlaylistTrack, Track, User
from app.schemas.schemas import PlaylistCreate, PlaylistResponse, PlaylistWithTracks, TrackResponse
from app.core.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[PlaylistResponse])
async def get_playlists(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all playlists for the current user."""
    result = await db.execute(
        select(Playlist).where(Playlist.user_id == current_user.id).offset(skip).limit(limit).order_by(Playlist.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{playlist_id}", response_model=PlaylistWithTracks)
async def get_playlist(playlist_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a playlist with its tracks, owned by the current user."""
    result = await db.execute(select(Playlist).where(Playlist.id == playlist_id, Playlist.user_id == current_user.id))
    playlist = result.scalar_one_or_none()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    pt_result = await db.execute(
        select(PlaylistTrack, Track)
        .join(Track, PlaylistTrack.track_id == Track.id)
        .where(PlaylistTrack.playlist_id == playlist_id)
        .order_by(PlaylistTrack.position)
    )
    tracks = [TrackResponse.model_validate(track) for _, track in pt_result.all()]

    response = PlaylistWithTracks.model_validate(playlist)
    response.tracks = tracks
    return response


@router.post("/", response_model=PlaylistResponse, status_code=201)
async def create_playlist(playlist_data: PlaylistCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new playlist for the current user."""
    playlist = Playlist(user_id=current_user.id, **playlist_data.model_dump())
    db.add(playlist)
    await db.flush()
    await db.refresh(playlist)
    return playlist


@router.post("/{playlist_id}/tracks/{track_id}", status_code=201)
async def add_track_to_playlist(
    playlist_id: str,
    track_id: str,
    position: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Add a track to a playlist owned by the current user."""
    result = await db.execute(select(Playlist).where(Playlist.id == playlist_id, Playlist.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Playlist not found")

    result = await db.execute(select(Track).where(Track.id == track_id, Track.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Track not found")

    if position is None:
        pos_result = await db.execute(
            select(PlaylistTrack.position).where(PlaylistTrack.playlist_id == playlist_id).order_by(PlaylistTrack.position.desc()).limit(1)
        )
        position = (pos_result.scalar_one_or_none() or -1) + 1

    playlist_track = PlaylistTrack(playlist_id=playlist_id, track_id=track_id, position=position)
    db.add(playlist_track)
    await db.flush()
    return {"message": "Track added to playlist"}


@router.delete("/{playlist_id}/tracks/{track_id}", status_code=204)
async def remove_track_from_playlist(
    playlist_id: str,
    track_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a track from a playlist."""
    result = await db.execute(select(Playlist).where(Playlist.id == playlist_id, Playlist.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Playlist not found")

    await db.execute(
        sql_delete(PlaylistTrack).where(
            PlaylistTrack.playlist_id == playlist_id,
            PlaylistTrack.track_id == track_id
        )
    )
    await db.flush()


@router.delete("/{playlist_id}", status_code=204)
async def delete_playlist(playlist_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a playlist owned by the current user."""
    result = await db.execute(select(Playlist).where(Playlist.id == playlist_id, Playlist.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Playlist not found")

    await db.execute(sql_delete(Playlist).where(Playlist.id == playlist_id))
    await db.flush()
