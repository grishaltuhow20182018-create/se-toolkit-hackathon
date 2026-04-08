"""Setlist API endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.core.database import get_db
from app.models.models import Setlist
from app.schemas.schemas import SetlistCreate, SetlistResponse

router = APIRouter()


@router.get("/", response_model=List[SetlistResponse])
async def get_setlists(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    """Get all setlists."""
    result = await db.execute(select(Setlist).offset(skip).limit(limit).order_by(Setlist.created_at.desc()))
    return result.scalars().all()


@router.get("/{setlist_id}", response_model=SetlistResponse)
async def get_setlist(setlist_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific setlist."""
    result = await db.execute(select(Setlist).where(Setlist.id == setlist_id))
    setlist = result.scalar_one_or_none()
    if not setlist:
        raise HTTPException(status_code=404, detail="Setlist not found")
    return setlist


@router.post("/", response_model=SetlistResponse, status_code=201)
async def create_setlist(setlist_data: SetlistCreate, db: AsyncSession = Depends(get_db)):
    """Create a new manual setlist."""
    setlist = Setlist(**setlist_data.model_dump(exclude={"playlist_id"}))
    db.add(setlist)
    await db.flush()
    await db.refresh(setlist)
    return setlist


@router.delete("/{setlist_id}", status_code=204)
async def delete_setlist(setlist_id: str, db: AsyncSession = Depends(get_db)):
    """Delete a setlist."""
    result = await db.execute(select(Setlist).where(Setlist.id == setlist_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Setlist not found")
    
    from sqlalchemy import delete as sql_delete
    await db.execute(sql_delete(Setlist).where(Setlist.id == setlist_id))
    await db.flush()
