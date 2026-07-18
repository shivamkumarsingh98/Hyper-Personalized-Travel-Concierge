from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.services.amadeus import AmadeusService
from app.db.models import AgentLog

class PlannerAgent(BaseAgent):
    def __init__(self):
        super().__init__("planner")

    async def execute(self, db: AsyncSession, payload: Dict[str, Any]) -> Dict[str, Any]:
        raw_message = payload.get("raw_message", "")
        trip_request_id = payload.get("trip_request_id")
        
        destination = "London"
        budget = 1500.0
        hotel_preference = "Marriott"
        
        if "london" in raw_message.lower():
            destination = "London"
        if "marriott" in raw_message.lower():
            hotel_preference = "Marriott"
            
        extracted_constraints = {
            "destination": destination,
            "budget": budget,
            "hotel_preference": hotel_preference,
            "parsed_date": "2026-08-15"
        }
        
        flights = AmadeusService.search_flights("DEL", destination, "2026-08-15")
        hotels = AmadeusService.search_hotels(destination, "2026-08-15", "2026-08-18")
        
        result = {
            "extracted_constraints": extracted_constraints,
            "flights": flights,
            "hotels": hotels
        }
        
        log = AgentLog(
            trip_request_id=trip_request_id,
            agent_name=self.name,
            input_payload={"raw_message": raw_message},
            output_payload=result
        )
        db.add(log)
        await db.commit()
        
        return result
