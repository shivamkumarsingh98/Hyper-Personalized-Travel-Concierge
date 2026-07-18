from pydantic import BaseModel
from typing import Any, Dict, Optional
from uuid import UUID

class ItineraryBase(BaseModel):
    trip_request_id: UUID
    flight_data: Dict[str, Any]
    hotel_data: Dict[str, Any]
    personalized_content: Dict[str, Any]
    total_cost: float

class ItineraryCreate(ItineraryBase):
    pass

class ItineraryResponse(ItineraryBase):
    id: UUID

    class Config:
        from_attributes = True
