from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.agents.planner import PlannerAgent
from app.agents.personalizer import PersonalizerAgent
from app.db.models import TripRequest, TripStatus, AgentLog

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("orchestrator")
        self.planner = PlannerAgent()
        self.personalizer = PersonalizerAgent()

    async def execute(self, db: AsyncSession, payload: Dict[str, Any]) -> Dict[str, Any]:
        user_id = payload.get("user_id")
        message = payload.get("message", "")
        
        trip_request = TripRequest(
            user_id=user_id,
            raw_message=message,
            status=TripStatus.received
        )
        db.add(trip_request)
        await db.flush()
        
        trip_request.status = TripStatus.planning
        await db.commit()
        
        planner_res = await self.planner.execute(db, {
            "trip_request_id": trip_request.id,
            "raw_message": message
        })
        
        trip_request.extracted_constraints = planner_res.get("extracted_constraints", {})
        await db.commit()
        
        trip_request.status = TripStatus.personalized
        await db.commit()
        
        personalizer_res = await self.personalizer.execute(db, {
            "trip_request_id": trip_request.id,
            "user_id": user_id,
            "flights": planner_res.get("flights", []),
            "hotels": planner_res.get("hotels", []),
            "extracted_constraints": planner_res.get("extracted_constraints", {})
        })
        
        itineraries = personalizer_res.get("scored_itineraries", [])
        recommended_itinerary = itineraries[0] if itineraries else None
        
        result = {
            "trip_request_id": str(trip_request.id),
            "status": trip_request.status,
            "recommended_itinerary": recommended_itinerary,
            "all_itineraries": itineraries,
            "message": f"I have processed your request. Based on your preferences (Loyalty Tier: {personalizer_res.get('loyalty_tier')}), I recommend the {recommended_itinerary['hotel']['hotel_name'] if recommended_itinerary else 'best'} package."
        }
        
        log = AgentLog(
            trip_request_id=trip_request.id,
            agent_name=self.name,
            input_payload={"message": message},
            output_payload=result
        )
        db.add(log)
        await db.commit()
        
        return result
