import uuid
import random
from typing import Any, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.base import BaseAgent
from app.services.payment import create_order
from app.db.models import AgentLog, Itinerary, Booking, Payment, BookingStatus, PaymentStatus

class ExecutorAgent(BaseAgent):
    def __init__(self):
        super().__init__("executor")

    async def execute(self, db: AsyncSession, payload: Dict[str, Any]) -> Dict[str, Any]:
        trip_request_id = payload.get("trip_request_id")
        selected = payload.get("selected_itinerary", {})
        
        itinerary = Itinerary(
            trip_request_id=trip_request_id,
            flight_data=selected.get("flight", {}),
            hotel_data=selected.get("hotel", {}),
            personalized_content=selected.get("personalized_content", {}),
            total_cost=selected.get("total_cost", 0.0)
        )
        db.add(itinerary)
        await db.flush()
        
        pnr = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=6))
        booking = Booking(
            itinerary_id=itinerary.id,
            pnr=pnr,
            status=BookingStatus.pending
        )
        db.add(booking)
        await db.flush()
        
        order_id = create_order(amount=float(itinerary.total_cost), currency="INR")
        
        payment = Payment(
            booking_id=booking.id,
            razorpay_order_id=order_id,
            amount=itinerary.total_cost,
            currency="INR",
            status=PaymentStatus.created
        )
        db.add(payment)
        await db.commit()
        
        result = {
            "itinerary_id": str(itinerary.id),
            "booking_id": str(booking.id),
            "pnr": pnr,
            "booking_status": booking.status,
            "razorpay_order_id": order_id,
            "amount": float(itinerary.total_cost)
        }
        
        log = AgentLog(
            trip_request_id=trip_request_id,
            agent_name=self.name,
            input_payload={"selected_itinerary": selected},
            output_payload=result
        )
        db.add(log)
        await db.commit()
        
        return result
