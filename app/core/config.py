from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="postgresql+asyncpg://postgres:postgres@localhost:5432/travel_concierge")
    RAZORPAY_KEY_ID: str = Field(default="rzp_test_xxxxxxxxxxxx")
    RAZORPAY_KEY_SECRET: str = Field(default="xxxxxxxxxxxxxxxxxxxx")
    
    @property
    def async_database_url(self) -> str:
        url = self.DATABASE_URL
        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        if "sslmode=" in url:
            url = url.replace("sslmode=require", "ssl=require")
            url = url.replace("sslmode=", "ssl=")
        return url
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
