"""
Fleet-Ryan Backend — FastAPI Application
Autonomous Fleet Management System for Orbital Installation Technologies
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import structlog
import time

from app.core.config import settings
from app.api import fleet, compliance, maintenance, escalation, webhooks, health
from app.core.database import init_db, close_db
from app.core.redis import init_redis, close_redis

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    # Startup
    logger.info("Starting Fleet-Ryan Backend", version=settings.APP_VERSION)
    try:
        await init_db()
    except Exception as e:
        logger.warning("DB init failed (will retry on first request)", error=str(e))
    try:
        await init_redis()
    except Exception as e:
        logger.warning("Redis init failed (running without cache)", error=str(e))
    logger.info("Fleet-Ryan Backend started successfully")

    yield

    # Shutdown
    logger.info("Shutting down Fleet-Ryan Backend")
    await close_db()
    await close_redis()
    logger.info("Fleet-Ryan Backend shut down")


app = FastAPI(
    title="Fleet-Ryan API",
    description="Autonomous Fleet Management System — Orbital Installation Technologies",
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = f"{duration:.4f}"
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        exc_info=True,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


# Include routers
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(fleet.router, prefix="/api/v1/fleet", tags=["Fleet"])
app.include_router(compliance.router, prefix="/api/v1/compliance", tags=["Compliance"])
app.include_router(maintenance.router, prefix="/api/v1/maintenance", tags=["Maintenance"])
app.include_router(escalation.router, prefix="/api/v1/escalation", tags=["Escalation"])
app.include_router(webhooks.router, prefix="/api/v1/webhooks", tags=["Webhooks"])


@app.get("/")
async def root():
    return {
        "name": "Fleet-Ryan API",
        "version": settings.APP_VERSION,
        "description": "Autonomous Fleet Management System",
        "company": "Orbital Installation Technologies, LLC",
        "docs": "/docs",
    }
