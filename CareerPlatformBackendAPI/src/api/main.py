from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .settings import get_settings

# Initialize settings at import time to fail-fast with clear error if critical env missing
try:
    settings = get_settings()
except Exception as exc:
    # Capture error message to avoid unused variable and make it available to route
    startup_error_message = str(exc)

    # Create a minimal app that returns a clear startup error instead of crashing the process
    app = FastAPI(
        title="Career Platform Backend API",
        description="Backend service for the MVP Career Platform. Startup error due to configuration.",
        version="1.0.0",
    )

    @app.get("/", tags=["health"], summary="Health Check (degraded)")
    def health_check_degraded():
        # Use the captured message so linting sees usage
        return {"status": "degraded", "error": startup_error_message}

else:
    app = FastAPI(
        title="Career Platform Backend API",
        description="Backend service for the MVP Career Platform",
        version="1.0.0",
    )

    # CORS configuration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", tags=["health"], summary="Health Check")
    def health_check():
        return {"message": "Healthy", "env": settings.APP_ENV}

    @app.get(
        "/_env",
        tags=["diagnostics"],
        summary="Environment diagnostics (non-sensitive)",
        description="Returns non-sensitive runtime configuration. Useful to verify that environment variables were loaded at runtime.",
    )
    def env_diagnostics():
        return {
            "APP_ENV": settings.APP_ENV,
            "PORT": settings.PORT,
            "has_JWT_SECRET": bool(settings.JWT_SECRET),
            "has_DATABASE_URL": bool(settings.DATABASE_URL),
            "has_INTERNAL_TOKEN": bool(settings.INTERNAL_TOKEN),
        }
