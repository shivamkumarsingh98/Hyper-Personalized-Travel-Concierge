import ssl
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings

connect_args = {}
if "postgresql" in settings.DATABASE_URL:
    connect_args = {"timeout": 60}
    if "localhost" not in settings.DATABASE_URL and "127.0.0.1" not in settings.DATABASE_URL:
        connect_args["ssl"] = True

engine = create_async_engine(
    settings.async_database_url,
    echo=True,
    future=True,
    connect_args=connect_args
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with SessionLocal() as session:
        yield session
