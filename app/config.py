print("CONFIG LOADED")
print(__file__)
from functools import lru_cache
from pydantic_settings import BaseSettings
from supabase import create_client, Client



class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GEMINI_API_KEY: str
    DATABASE_URL: str   # For PostgresSaver checkpointer

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_supabase_client() -> Client:
    settings = get_settings()
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

