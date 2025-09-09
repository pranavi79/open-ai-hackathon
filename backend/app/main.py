from fastapi import FastAPI
from backend.app.core.config import settings
from .routes import router as api_router
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    return app

app = create_app()