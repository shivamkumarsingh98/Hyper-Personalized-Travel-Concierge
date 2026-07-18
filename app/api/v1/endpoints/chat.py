from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.chat import ChatRequest, ChatResponse
from app.agents.orchestrator import OrchestratorAgent

router = APIRouter()
router_prefix = "/chat"

orchestrator = OrchestratorAgent()

@router.post("/converse", response_model=ChatResponse)
async def converse(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    result = await orchestrator.execute(db, {
        "user_id": request.user_id,
        "message": request.message
    })
    
    return ChatResponse(
        session_id=request.user_id,
        trip_request_id=result["trip_request_id"],
        message=result["message"],
        itinerary=result["recommended_itinerary"],
        all_itineraries=result["all_itineraries"],
        status=result["status"]
    )
