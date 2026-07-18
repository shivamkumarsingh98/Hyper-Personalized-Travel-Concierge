from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID
from app.api.deps import get_db
from app.schemas.user import UserCreate, UserResponse
from app.db.models import User

router = APIRouter()
router_prefix = "/users"

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_in.email)
    res = await db.execute(stmt)
    existing = res.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(
        name=user_in.name,
        email=user_in.email,
        loyalty_tier=user_in.loyalty_tier,
        preferences=user_in.preferences
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

@router.get("/{user_id}/profile", response_model=UserResponse)
async def get_user_profile(user_id: UUID, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login", response_model=UserResponse)
async def login_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    stmt = select(User).where(User.email == user_in.email)
    res = await db.execute(stmt)
    user = res.scalars().first()
    if not user:
        user = User(
            name=user_in.name,
            email=user_in.email,
            loyalty_tier=user_in.loyalty_tier or "Standard",
            preferences=user_in.preferences or {}
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    return user

@router.put("/{user_id}/profile", response_model=UserResponse)
async def update_user_profile(user_id: UUID, user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.name = user_in.name
    user.email = user_in.email
    user.loyalty_tier = user_in.loyalty_tier
    user.preferences = user_in.preferences
    await db.commit()
    await db.refresh(user)
    return user
