"""FastAPI application factory."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from confradar.settings import get_settings

from .routes_conferences import router as conferences_router
from .routes_deadlines import router as deadlines_router
from .routes_health import router as health_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    # Startup
    settings = get_settings()
    logger.info("ConfRadar API starting up")
    logger.info(f"Database URL: {settings.database_url}")
    yield
    # Shutdown
    logger.info("ConfRadar API shutting down")


def create_app() -> FastAPI:
    """Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    app = FastAPI(
        title="ConfRadar API",
        description="REST API for conference deadline tracking",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    
    # Configure CORS
    # TODO: Configure CORS_ORIGINS via settings for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure this for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Register routers
    app.include_router(health_router)
    app.include_router(conferences_router)
    app.include_router(deadlines_router)
    
    return app
