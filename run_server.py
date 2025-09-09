#!/usr/bin/env python3
"""
Emergency Accident Response System Server
"""

import uvicorn
import sys
import os
from pathlib import Path

# Add the backend directory to Python path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from backend.app.core.config import settings

def main():
    """Run the FastAPI server"""
    try:
        uvicorn.run(
            "backend.app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            reload_dirs=["backend"] if settings.DEBUG else None,
        )
    except Exception as e:
        print(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()