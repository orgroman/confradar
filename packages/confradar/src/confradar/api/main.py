"""Entry point for running the FastAPI server.

Usage:
    python -m confradar.api.main
    
Or with uvicorn directly:
    uvicorn confradar.api.main:app --reload --host 0.0.0.0 --port 8000
"""

from .app import create_app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "confradar.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
