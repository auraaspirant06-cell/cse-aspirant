"""
CSE Aspirant - NextGen FastAPI Server
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.constants import APP_NAME, APP_VERSION
from core.config import config
from api.routes import health, keys, music, education, payments, analytics

def create_app() -> FastAPI:
    app = FastAPI(
        title=f"{APP_NAME} NextGen API",
        version=APP_VERSION,
        description="High-performance unified API for CSE Aspirant Bot, Music Engine, and Education Academy.",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.services.cors_origins or ["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(keys.router)
    app.include_router(music.router)
    app.include_router(education.router)
    app.include_router(payments.router)
    app.include_router(analytics.router)

    return app

app = create_app()

