from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class BookingBase(BaseModel):
    itinerary_id: UUID
    pnr: str
    status: str

class BookingCreate(BookingBase):
    pass

class BookingResponse(BookingBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
