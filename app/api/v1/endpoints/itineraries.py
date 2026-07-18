from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.api.deps import get_db
from app.db.models import Itinerary
from app.schemas.itinerary import ItineraryResponse

router = APIRouter()
router_prefix = "/itineraries"

@router.get("/{itinerary_id}", response_model=ItineraryResponse)
async def get_itinerary(itinerary_id: UUID, db: AsyncSession = Depends(get_db)):
    itinerary = await db.get(Itinerary, itinerary_id)
    if not itinerary:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return itinerary

@router.get("", response_model=list[ItineraryResponse])
async def list_itineraries(db: AsyncSession = Depends(get_db)):
    stmt = select(Itinerary)
    res = await db.execute(stmt)
    return res.scalars().all()
