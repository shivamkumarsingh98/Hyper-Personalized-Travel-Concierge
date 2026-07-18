from pydantic import BaseModel
from typing import Any, Dict, List, Optional
from uuid import UUID

class ChatRequest(BaseModel):
    user_id: UUID
    message: str

class ChatResponse(BaseModel):
    session_id: UUID
    message: str
    itinerary: Optional[Dict[str, Any]] = None
    status: str
