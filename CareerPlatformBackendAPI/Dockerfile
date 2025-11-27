# syntax=docker/dockerfile:1

# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set environment to avoid Python writing .pyc and buffering issues
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=on

# Create app directory
WORKDIR /app

# System deps (if needed for building wheels)
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Install Python dependencies first to leverage layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source (do NOT copy .env or local files)
COPY src ./src
COPY interfaces ./interfaces
COPY README.md ./

# Expose default FastAPI port
EXPOSE 8000

# Runtime envs are expected to be provided by orchestrator at container run time.
# Start the application using the module entrypoint.
CMD ["python", "-m", "src.api.entrypoint"]
