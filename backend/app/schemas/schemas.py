"""Pydantic schemas for API requests/responses."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Track schemas
class TrackBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    artist: str = Field(..., min_length=1, max_length=255)
    album: Optional[str] = None
    bpm: float = Field(..., gt=0, description="Beats per minute")
    key: str = Field(..., pattern=r"^\d{1,2}[AB]$", description="Camelot key notation (e.g., 8A, 12B)")
    energy_level: int = Field(..., ge=1, le=10, description="Energy level 1-10")
    genre: Optional[str] = None
    duration_seconds: Optional[float] = None
    file_path: Optional[str] = None
    tags: list[str] = []
    notes: Optional[str] = None


class TrackCreate(TrackBase):
    pass


class TrackUpdate(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    bpm: Optional[float] = None
    key: Optional[str] = None
    energy_level: Optional[int] = None
    genre: Optional[str] = None
    duration_seconds: Optional[float] = None
    file_path: Optional[str] = None
    tags: Optional[list[str]] = None
    notes: Optional[str] = None


class TrackResponse(TrackBase):
    id: str
    file_size_bytes: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# Playlist schemas
class PlaylistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class PlaylistResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class PlaylistWithTracks(PlaylistResponse):
    tracks: list[TrackResponse] = []


# Setlist schemas
class SetlistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    target_duration_minutes: Optional[int] = None
    vibe: Optional[str] = None
    playlist_id: Optional[str] = None


class SetlistResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    target_duration_minutes: Optional[int] = None
    vibe: Optional[str] = None
    track_order: list = []
    ai_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# AI schemas
class SetlistGenerationRequest(BaseModel):
    playlist_id: Optional[str] = None
    track_ids: Optional[list[str]] = None
    target_duration_minutes: Optional[int] = None
    vibe: Optional[str] = Field(None, description="e.g., warmup, peak, cooldown, journey")
    starting_track_id: Optional[str] = None
    max_tracks: Optional[int] = Field(None, ge=1, le=50)


class SetlistGenerationResponse(BaseModel):
    setlist: SetlistResponse
    suggestions: list[str] = []
    compatibility_scores: dict[str, float] = {}


class NextTrackRequest(BaseModel):
    current_track_id: str
    available_track_ids: Optional[list[str]] = None
    playlist_id: Optional[str] = None


class NextTrackResponse(BaseModel):
    recommended_track: TrackResponse
    reasoning: str
    compatibility_score: float
    transition_tips: str
