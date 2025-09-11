"""
Emergency Response AI System - Consolidated Routes
All API endpoints for the emergency response system
"""
from fastapi import APIRouter, HTTPException
from .models import (
    UserRequest, EmergencyAnalysisRequest, HospitalSearchRequest,
    ContactEmergencyRequest, CallHospitalRequest, AccidentReport
)
from .services import HospitalSearchService, EmergencyAnalysisService, CallingService
from .config import get_cost_protection
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
hospital_service = HospitalSearchService()
emergency_service = EmergencyAnalysisService()
calling_service = CallingService()
cost_protection = get_cost_protection()

@router.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Emergency Response AI System", "status": "operational"}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@router.post("/analyze-emergency", response_model=AccidentReport)
async def analyze_emergency(request: EmergencyAnalysisRequest):
    """Analyze emergency situation and provide first aid guidance"""
    try:
        # Check cost protection
        if not cost_protection.can_make_request("openai_requests"):
            raise HTTPException(status_code=429, detail="Daily OpenAI request limit reached")
        
        # Analyze emergency
        result = await emergency_service.analyze_emergency(request.message, request.location)
        
        # Track usage
        cost_protection.track_request("openai_requests")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in analyze_emergency: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/find-hospitals")
async def find_hospitals(request: HospitalSearchRequest):
    """Find nearby hospitals"""
    try:
        # Check cost protection
        if not cost_protection.can_make_request("google_maps_requests"):
            raise HTTPException(status_code=429, detail="Daily Google Maps request limit reached")
        
        # Find hospitals
        hospitals = await hospital_service.find_nearby_hospitals(
            request.latitude, request.longitude, request.radius
        )
        
        # Track usage
        cost_protection.track_request("google_maps_requests")
        
        return {"hospitals": hospitals}
        
    except Exception as e:
        logger.error(f"Error in find_hospitals: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/contact-emergency")
async def contact_emergency(request: ContactEmergencyRequest):
    """Contact emergency services"""
    try:
        # Check cost protection
        if not cost_protection.can_make_request("twilio_calls"):
            raise HTTPException(status_code=429, detail="Daily Twilio call limit reached")
        
        # Make emergency call
        result = await calling_service.call_emergency_services(request.phone, request.message)
        
        # Track usage
        cost_protection.track_request("twilio_calls")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in contact_emergency: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/call-hospital")
async def call_hospital(request: CallHospitalRequest):
    """Call a specific hospital"""
    try:
        # Check cost protection
        if not cost_protection.can_make_request("twilio_calls"):
            raise HTTPException(status_code=429, detail="Daily Twilio call limit reached")
        
        # Call hospital
        result = await calling_service.call_hospital(request.hospital_id, request.user_phone)
        
        # Track usage
        cost_protection.track_request("twilio_calls")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in call_hospital: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api-usage")
async def get_api_usage():
    """Get current API usage statistics"""
    try:
        return cost_protection.get_usage_report()
    except Exception as e:
        logger.error(f"Error getting API usage: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demo-mode/enable")
async def enable_demo_mode():
    """Enable demo mode to prevent API charges"""
    try:
        cost_protection.set_demo_mode(True)
        return {"status": "success", "message": "Demo mode enabled"}
    except Exception as e:
        logger.error(f"Error enabling demo mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/demo-mode/disable")
async def disable_demo_mode():
    """Disable demo mode to enable live API calls"""
    try:
        cost_protection.set_demo_mode(False)
        return {"status": "success", "message": "Demo mode disabled"}
    except Exception as e:
        logger.error(f"Error disabling demo mode: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/demo-mode/status")
async def get_demo_mode_status():
    """Get current demo mode status"""
    try:
        is_demo = cost_protection.is_demo_mode()
        return {"demo_mode": is_demo, "status": "enabled" if is_demo else "disabled"}
    except Exception as e:
        logger.error(f"Error getting demo mode status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Legacy endpoint for backward compatibility
@router.post("/ask", response_model=AccidentReport)
async def ask_question(payload: UserRequest):
    """Legacy endpoint for backward compatibility"""
    try:
        # Convert to new format
        analysis_request = EmergencyAnalysisRequest(
            message=payload.request,
            location={
                "latitude": payload.latitude,
                "longitude": payload.longitude
            }
        )
        
        return await analyze_emergency(analysis_request)
        
    except Exception as e:
        logger.error(f"Error in legacy ask endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))