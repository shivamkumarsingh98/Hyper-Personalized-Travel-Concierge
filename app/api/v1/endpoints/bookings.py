from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.api.deps import get_db
from app.agents.executor import ExecutorAgent
from app.services.payment import verify_payment, create_order
from app.db.models import Booking, BookingStatus, Payment, PaymentStatus
from app.schemas.payment import RazorpayVerifyRequest
from app.core.config import settings

router = APIRouter()
router_prefix = "/bookings"

executor = ExecutorAgent()

@router.post("/execute")
async def execute_booking(payload: dict, db: AsyncSession = Depends(get_db)):
    try:
        res = await executor.execute(db, payload)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{booking_id}/pay")
async def pay_booking(booking_id: UUID, db: AsyncSession = Depends(get_db)):
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    # Load itinerary
    await db.refresh(booking, ["itinerary"])
    amount = float(booking.itinerary.total_cost)
    
    stmt = select(Payment).where(Payment.booking_id == booking_id).order_by(Payment.created_at.desc())
    res = await db.execute(stmt)
    payment = res.scalars().first()
    
    if payment and payment.status == PaymentStatus.created:
        order_id = payment.razorpay_order_id
    else:
        order_id = create_order(amount=amount)
        payment = Payment(
            booking_id=booking_id,
            razorpay_order_id=order_id,
            amount=amount,
            currency="INR",
            status=PaymentStatus.created
        )
        db.add(payment)
        await db.commit()
        
    return {
        "booking_id": str(booking_id),
        "razorpay_order_id": order_id,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": amount
    }

@router.post("/{booking_id}/verify")
async def verify_booking_payment(booking_id: UUID, verify_in: RazorpayVerifyRequest, db: AsyncSession = Depends(get_db)):
    booking = await db.get(Booking, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    stmt = select(Payment).where(Payment.booking_id == booking_id, Payment.razorpay_order_id == verify_in.razorpay_order_id)
    res = await db.execute(stmt)
    payment = res.scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment record for order not found")
        
    try:
        verify_payment(
            razorpay_order_id=verify_in.razorpay_order_id,
            razorpay_payment_id=verify_in.razorpay_payment_id,
            razorpay_signature=verify_in.razorpay_signature
        )
        payment.status = PaymentStatus.captured
        payment.razorpay_payment_id = verify_in.razorpay_payment_id
        booking.status = BookingStatus.confirmed
        await db.commit()
        return {"status": "success", "message": "Payment verified and booking confirmed"}
    except Exception as e:
        payment.status = PaymentStatus.failed
        await db.commit()
        raise HTTPException(status_code=400, detail=f"Payment verification failed: {str(e)}")
