import sys
import uvicorn

from .main import app
from .settings import get_settings

def _get_port() -> int:
    try:
        settings = get_settings()
        return int(settings.PORT)
    except Exception as e:
        # Fall back to default port and print a clear message
        print(f"[startup] Warning: using default port 8000 due to configuration issue: {e}", file=sys.stderr)
        return 8000

if __name__ == "__main__":
    port = _get_port()
    # PUBLIC_INTERFACE
    # Start Uvicorn server; configuration comes from runtime env only
    uvicorn.run(app, host="0.0.0.0", port=port, proxy_headers=True)
