from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Dict, Any
import os

from backend.app.models.accident_report import AccidentReport
from backend.app.models.user_request import UserRequest
from backend.app.service.run_accident_response_agent import handle_question

router = APIRouter()

@router.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint providing basic API information"""
    return {
        "message": "Emergency Accident Response System API",
        "version": "1.0.0",
        "status": "operational"
    }

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint to verify system status"""
    health_status = {
        "status": "healthy",
        "services": {
            "api": "operational",
            "openai": "configured" if os.getenv("OPENAI_API_KEY") else "not configured",
            "google_maps": "configured" if os.getenv("GOOGLE_MAPS_API_KEY") else "not configured",
            "twilio": "configured" if all([os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN")]) else "not configured"
        }
    }
    
    # Determine overall health
    missing_services = [service for service, status in health_status["services"].items() 
                       if status == "not configured" and service != "api"]
    
    if missing_services:
        health_status["status"] = "degraded"
        health_status["warnings"] = f"Missing configuration for: {', '.join(missing_services)}"
    
    status_code = status.HTTP_200_OK if health_status["status"] == "healthy" else status.HTTP_503_SERVICE_UNAVAILABLE
    return JSONResponse(content=health_status, status_code=status_code)

@router.post("/ask", response_model=AccidentReport)
async def process_accident_report(payload: UserRequest) -> AccidentReport:
    """
    Process an accident report and coordinate emergency response.
    
    This endpoint:
    1. Analyzes the accident description using AI
    2. Classifies the severity (minor vs major trauma)
    3. Provides first aid guidance
    4. Finds nearby hospitals
    5. Contacts hospitals for major trauma cases
    
    Args:
        payload: User request containing accident description and location
        
    Returns:
        AccidentReport with classification, first aid tips, and details
        
    Raises:
        HTTPException: If processing fails or required data is missing
    """
    try:
        # Validate input
        if not payload.request.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Accident description cannot be empty"
            )
        
        if not payload.latitude or not payload.longitude:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location coordinates (latitude and longitude) are required"
            )
        
        # Process the accident report
        result = await handle_question(payload)
        return result
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid input: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )