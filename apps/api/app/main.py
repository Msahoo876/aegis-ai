"""
Application Entry Point
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.logging import logger
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logger import RequestLoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    """

    logger.info("Starting Aegis AI API...")

    yield

    logger.info("Shutting down Aegis AI API...")


def create_application() -> FastAPI:
    """
    Application Factory
    """

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )
    
    # ----------------------------
    # Built-in Middleware
    # ----------------------------

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        GZipMiddleware,
        minimum_size=1024,
    )

    # ----------------------------
    # Custom Middleware
    # ----------------------------

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # ----------------------------
    # API Routes
    # ----------------------------

    app.include_router(api_router)

    logger.info("Application initialized successfully.")

    return app


app = create_application()