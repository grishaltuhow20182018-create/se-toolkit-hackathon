"""Setlist API endpoints - user-scoped."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete as sql_delete
from typing import List
from app.core.database import get_db
from app.models.models import Setlist, User
from app.schemas.schemas import SetlistCreate, SetlistResponse
from app.core.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=List[SetlistResponse])
async def get_setlists(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get all setlists for the current user."""
    result = await db.execute(
        select(Setlist).where(Setlist.user_id == current_user.id).offset(skip).limit(limit).order_by(Setlist.created_at.desc())
    )
    return result.scalars().all()


@router.get("/{setlist_id}", response_model=SetlistResponse)
async def get_setlist(setlist_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Get a specific setlist owned by the current user."""
    result = await db.execute(select(Setlist).where(Setlist.id == setlist_id, Setlist.user_id == current_user.id))
    setlist = result.scalar_one_or_none()
    if not setlist:
        raise HTTPException(status_code=404, detail="Setlist not found")
    return setlist


@router.post("/", response_model=SetlistResponse, status_code=201)
async def create_setlist(setlist_data: SetlistCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Create a new setlist for the current user."""
    setlist = Setlist(user_id=current_user.id, **setlist_data.model_dump(exclude={"playlist_id"}))
    db.add(setlist)
    await db.flush()
    await db.refresh(setlist)
    return setlist


@router.delete("/{setlist_id}", status_code=204)
async def delete_setlist(setlist_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Delete a setlist owned by the current user."""
    result = await db.execute(select(Setlist).where(Setlist.id == setlist_id, Setlist.user_id == current_user.id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Setlist not found")

    await db.execute(sql_delete(Setlist).where(Setlist.id == setlist_id))
    await db.flush()
