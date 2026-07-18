from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.services.contentstack import ContentstackService
from app.db.models import AgentLog, User

class PersonalizerAgent(BaseAgent):
    def __init__(self):
        super().__init__("personalizer")

    async def execute(self, db: AsyncSession, payload: Dict[str, Any]) -> Dict[str, Any]:
        trip_request_id = payload.get("trip_request_id")
        user_id = payload.get("user_id")
        flights = payload.get("flights", [])
        hotels = payload.get("hotels", [])
        constraints = payload.get("extracted_constraints", {})
        
        user = await db.get(User, user_id)
        loyalty_tier = user.loyalty_tier if user else "Standard"
        
        cms_content = ContentstackService.get_personalized_content(loyalty_tier, constraints.get("destination", "London"))
        
        scored_itineraries = []
        for flight in flights:
            for hotel in hotels:
                score = 100
                if constraints.get("hotel_preference", "").lower() in hotel.get("hotel_name", "").lower():
                    score += 20
                if loyalty_tier == "VIP":
                    score += 10
                    
                total_cost = flight.get("price", 0) + hotel.get("total_price", 0)
                if total_cost > constraints.get("budget", 1500):
                    score -= 50
                    
                scored_itineraries.append({
                    "flight": flight,
                    "hotel": hotel,
                    "total_cost": total_cost,
                    "score": score,
                    "personalized_content": cms_content
                })
                
        scored_itineraries.sort(key=lambda x: x["score"], reverse=True)
        
        result = {
            "scored_itineraries": scored_itineraries,
            "loyalty_tier": loyalty_tier
        }
        
        log = AgentLog(
            trip_request_id=trip_request_id,
            agent_name=self.name,
            input_payload={"user_id": str(user_id)},
            output_payload=result
        )
        db.add(log)
        await db.commit()
        
        return result
