"""
Emergency Response AI System - Main Application
Consolidated FastAPI application with all endpoints
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router as api_router
from .config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create FastAPI application with all configurations"""
    app = FastAPI(
        title="Emergency Response AI System",
        description="AI-powered emergency response and hospital finder",
        version="1.0.0"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(api_router)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("Emergency Response AI System starting up...")
        logger.info("All systems operational")
    
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Emergency Response AI System shutting down...")
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)