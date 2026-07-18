from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class PaymentCreate(BaseModel):
    booking_id: UUID
    amount: float
    currency: str = "INR"

class PaymentResponse(BaseModel):
    id: UUID
    booking_id: UUID
    razorpay_order_id: str
    razorpay_payment_id: Optional[str] = None
    amount: float
    currency: str
    status: str

    class Config:
        from_attributes = True

class RazorpayVerifyRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
