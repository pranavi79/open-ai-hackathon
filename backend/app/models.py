"""
Emergency Response AI System - Consolidated Models
All data models for the emergency response system
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User Request Model
class UserRequest(BaseModel):
    request: str
    latitude: float
    longitude: float

# Location Context Model
class LocationContext(BaseModel):
    latitude: float
    longitude: float
    address: Optional[str] = None
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None

# Hospital Info Model
class HospitalInfo(BaseModel):
    id: str
    name: str
    address: str
    phone: str
    latitude: float
    longitude: float
    distance: Optional[float] = None
    rating: Optional[float] = None
    website: Optional[str] = None
    emergency_services: bool = True

# Accident Report Model
class AccidentReport(BaseModel):
    accident_type: str
    first_aid_tips: List[str]
    location: str
    details: str
    timestamp: str = datetime.now().isoformat()
    severity_level: Optional[str] = "moderate"
    recommended_actions: Optional[List[str]] = []
    nearest_hospitals: Optional[List[HospitalInfo]] = []
    response_time_needed: Optional[str] = "Standard"
    priority_level: Optional[str] = "medium"
    confidence_score: Optional[float] = 0.8

# API Request Models
class EmergencyAnalysisRequest(BaseModel):
    message: str
    location: LocationContext
    scenario_type: Optional[str] = "custom-emergency"
    force_new_analysis: Optional[bool] = False
    timestamp: Optional[str] = None

class HospitalSearchRequest(BaseModel):
    latitude: float
    longitude: float
    radius: int = 5000
    emergency_type: Optional[str] = "general"

class ContactEmergencyRequest(BaseModel):
    phone_number: str
    message: str
    location: Optional[LocationContext] = None

class CallHospitalRequest(BaseModel):
    hospital_id: str
    user_phone: str
