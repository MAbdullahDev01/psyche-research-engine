from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PUBLIC_SUPABASE_URL: str
    PUBLIC_SUPABASE_PUBLISHABLE_KEY: str

    # Config for settings
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings() # type: ignore