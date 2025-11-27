# Career Platform Backend API

FastAPI backend for the MVP Career Platform.

Environment handling and build process have been updated to remove build-time reliance on `.env` files.

## Key changes

- No `cat '*.env'` or any build-time concatenation of `.env` files.
- Environment variables are loaded at runtime via Pydantic settings (`src/api/settings.py`).
- A `.env` file is optional for local development only. If absent, the app still starts (unless critical vars are missing).
- Clear, actionable error messages are produced if critical env vars are missing (`JWT_SECRET`, and `DATABASE_URL` outside of development).

## Required/Optional environment variables

See `.env.example` for a full list. Important ones include:

- APP_ENV (default: development)
- PORT (default: 8000)
- JWT_SECRET (required)
- DATABASE_URL (required in non-development APP_ENV)
- INTERNAL_TOKEN (optional; required if calling internal services)

## Local development

1. Copy `.env.example` to `.env` and customize as needed (optional).
2. Install dependencies:
   pip install -r requirements.txt
3. Run the server:
   python -m src.api.entrypoint

Alternatively, with Uvicorn directly:
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000

Note: The application reads environment variables from the process environment and, if present, from a `.env` file. Absence of `.env` does not cause build/startup failure.

## Docker/Container notes

- Do not bake `.env` into images.
- Provide environment variables at container runtime via your orchestrator (Docker, Compose, Kubernetes, etc.).
- The app fails gracefully with a clear message if critical variables are not supplied; the health endpoint will show `status=degraded`.

Example (Docker):
  docker run --rm -e APP_ENV=production -e JWT_SECRET=secret -e DATABASE_URL=postgresql://... -p 8000:8000 backend-image

## Diagnostics

A non-sensitive diagnostics endpoint is available:
  GET /_env

This returns boolean flags for critical variables without exposing secrets.
