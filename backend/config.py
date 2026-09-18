from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PUBLIC_SUPABASE_URL: str
    PUBLIC_SUPABASE_PUBLISHABLE_KEY: str

    # Config for settings
    class Config:
        env_file = ".env"

settings = Settings() # type: ignore