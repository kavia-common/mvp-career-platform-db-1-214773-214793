from typing import Optional

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

# PUBLIC_INTERFACE
class AppSettings(BaseSettings):
    """Application settings loaded from environment variables at runtime.

    The loader does NOT require a .env file to exist. If a .env file is present in the
    working directory, it will be used as an additional source. Absence of a .env file
    must not cause build or runtime failure; environment variables should be injected by
    the runtime orchestrator (Docker/Kubernetes/etc.).

    Critical variables:
    - APP_ENV: Environment name (development, staging, production)
    - PORT: Port to bind the HTTP server
    - JWT_SECRET: Secret key for signing JWT tokens
    - DATABASE_URL: Database connection string
    - INTERNAL_TOKEN: Internal service-to-service auth token
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_ENV: str = Field(default="development", description="Application environment")
    PORT: int = Field(default=8000, description="Port for HTTP server")
    JWT_SECRET: str = Field(default="", description="JWT signing secret")
    DATABASE_URL: Optional[str] = Field(default=None, description="Database connection string")
    INTERNAL_TOKEN: Optional[str] = Field(default=None, description="Internal service token")

# PUBLIC_INTERFACE
def get_settings() -> AppSettings:
    """Return AppSettings instance.

    This function attempts to load from process environment, and optionally from a .env
    file if present. It does not fail if .env is missing; instead, it validates critical
    fields and raises clear messages if values are missing.
    """
    try:
        settings = AppSettings()
    except ValidationError as ve:
        # This will catch type errors, but we also provide custom checks below
        raise RuntimeError(f"Invalid environment configuration: {ve}") from ve

    critical_errors = []

    if not settings.JWT_SECRET:
        critical_errors.append("JWT_SECRET is required for authentication.")
    # DATABASE_URL may be optional depending on feature flags; mark as warning rather than error
    # but if APP_ENV is not development, we consider it required.
    if settings.APP_ENV.lower() != "development" and not settings.DATABASE_URL:
        critical_errors.append("DATABASE_URL is required outside of development.")

    if critical_errors:
        joined = " ".join(critical_errors)
        raise RuntimeError(
            f"Missing critical environment configuration. {joined} "
            "Set them via environment variables at runtime. "
            "See .env.example for details."
        )

    return settings
