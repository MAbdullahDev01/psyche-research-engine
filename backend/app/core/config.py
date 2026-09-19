from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PUBLIC_SUPABASE_URL: str
    PUBLIC_SUPABASE_PUBLISHABLE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    PUBLIC_CLERK_PUBLISHABLE_KEY: str
    CLERK_SECRET_KEY: str
    CLERK_WEBHOOK_SIGNING_SECRET: str

    # Config for settings
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore