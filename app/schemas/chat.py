from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    user_id: UUID
    message: str

class ChatResponse(BaseModel):
    session_id: UUID
    trip_request_id: Optional[UUID] = None
    message: str
    itinerary: Optional[Dict[str, Any]] = None
    all_itineraries: Optional[List[Dict[str, Any]]] = None
    status: str
