# mvp-career-platform-db-1-214773-214793

This workspace contains the Career Platform containers.

For backend environment handling updates and runtime configuration instructions, see:
- CareerPlatformBackendAPI/README.md
- CareerPlatformBackendAPI/.env.example

Container build hygiene:
- A Dockerfile is provided that does not copy or read .env at build time.
- A .dockerignore excludes .env files from the build context.