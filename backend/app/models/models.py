"""Database models for DJ Setlist AI."""

import uuid
from datetime import datetime
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Track(Base):
    """Music track with metadata for DJ mixing."""

    __tablename__ = "tracks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    artist: Mapped[str] = mapped_column(String(255), nullable=False)
    album: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # DJ-specific metadata
    bpm: Mapped[float] = mapped_column(Float, nullable=False)
    # Musical key using Camelot notation (e.g., "8A", "12B")
    key: Mapped[str] = mapped_column(String(10), nullable=False)
    # Energy level from 1-10
    energy_level: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    
    # File information
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    file_size_bytes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    
    # Additional metadata
    tags: Mapped[list] = mapped_column(JSON, default=list)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    playlist_tracks = relationship("PlaylistTrack", back_populates="track", cascade="all, delete-orphan")


class Playlist(Base):
    """Collection of tracks."""

    __tablename__ = "playlists"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    playlist_tracks = relationship("PlaylistTrack", back_populates="playlist", cascade="all, delete-orphan")


class PlaylistTrack(Base):
    """Association table for playlist-track many-to-many relationship."""

    __tablename__ = "playlist_tracks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    playlist_id: Mapped[str] = mapped_column(String, ForeignKey("playlists.id", ondelete="CASCADE"), nullable=False)
    track_id: Mapped[str] = mapped_column(String, ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relationships
    playlist = relationship("Playlist", back_populates="playlist_tracks")
    track = relationship("Track", back_populates="playlist_tracks")


class Setlist(Base):
    """AI-generated DJ setlist with track order."""

    __tablename__ = "setlists"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Setlist configuration
    target_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    vibe: Mapped[str | None] = mapped_column(String(100), nullable=True)  # e.g., "warmup", "peak", "cooldown"
    
    # AI-generated ordered track list
    track_order: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    # AI reasoning/suggestions
    ai_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
