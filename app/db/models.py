import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, ForeignKey, DateTime, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base

class TripStatus(str, PyEnum):
    received = "received"
    planning = "planning"
    personalized = "personalized"
    booked = "booked"
    failed = "failed"

class BookingStatus(str, PyEnum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"

class PaymentStatus(str, PyEnum):
    created = "created"
    authorized = "authorized"
    captured = "captured"
    failed = "failed"

class User(Base):
    __tablename__ = "users"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    loyalty_tier: Mapped[str] = mapped_column(String, default="Standard")
    preferences: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    trip_requests: Mapped[list["TripRequest"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class TripRequest(Base):
    __tablename__ = "trip_requests"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    raw_message: Mapped[str] = mapped_column(String, nullable=False)
    extracted_constraints: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[TripStatus] = mapped_column(Enum(TripStatus), default=TripStatus.received)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    user: Mapped["User"] = relationship(back_populates="trip_requests")
    itineraries: Mapped[list["Itinerary"]] = relationship(back_populates="trip_request", cascade="all, delete-orphan")
    agent_logs: Mapped[list["AgentLog"]] = relationship(back_populates="trip_request", cascade="all, delete-orphan")

class Itinerary(Base):
    __tablename__ = "itineraries"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id", ondelete="CASCADE"), nullable=False)
    flight_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    hotel_data: Mapped[dict] = mapped_column(JSONB, default=dict)
    personalized_content: Mapped[dict] = mapped_column(JSONB, default=dict)
    total_cost: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    trip_request: Mapped["TripRequest"] = relationship(back_populates="itineraries")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="itinerary", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    itinerary_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    pnr: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    itinerary: Mapped["Itinerary"] = relationship(back_populates="bookings")
    payments: Mapped[list["Payment"]] = relationship(back_populates="booking", cascade="all, delete-orphan")

class Payment(Base):
    __tablename__ = "payments"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    booking_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    razorpay_order_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    razorpay_payment_id: Mapped[str | None] = mapped_column(String, nullable=True)
    amount: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String, default="INR")
    status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.created)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    booking: Mapped["Booking"] = relationship(back_populates="payments")

class AgentLog(Base):
    __tablename__ = "agent_logs"
    
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    trip_request_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("trip_requests.id", ondelete="CASCADE"), nullable=False)
    agent_name: Mapped[str] = mapped_column(String, nullable=False)
    input_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    output_payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    trip_request: Mapped["TripRequest"] = relationship(back_populates="agent_logs")
