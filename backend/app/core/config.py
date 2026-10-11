from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PUBLIC_SUPABASE_URL: str
    PUBLIC_SUPABASE_PUBLISHABLE_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    PUBLIC_CLERK_PUBLISHABLE_KEY: str
    CLERK_SECRET_KEY: str
    CLERK_WEBHOOK_SIGNING_SECRET: str
    OPENALEX_API_KEY: str

    # Comma-separated origins/parties support local development and deployment.
    CORS_ALLOWED_ORIGINS: str = "http://localhost:3000"
    CLERK_AUTHORIZED_PARTIES: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @staticmethod
    def _parse_csv(value: str) -> list[str]:
        return [item.strip().rstrip("/") for item in value.split(",") if item.strip()]

    @property
    def cors_origins(self) -> list[str]:
        return self._parse_csv(self.CORS_ALLOWED_ORIGINS)

    @property
    def clerk_authorized_parties(self) -> list[str]:
        return self._parse_csv(self.CLERK_AUTHORIZED_PARTIES)


settings = Settings()  # type: ignore
