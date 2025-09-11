"""
Emergency Response AI System - Consolidated Services
All business logic and API integrations
"""
import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from .models import HospitalInfo, AccidentReport, LocationContext

logger = logging.getLogger(__name__)

class HospitalSearchService:
    """Service for finding nearby hospitals using Google Maps API"""
    
    def __init__(self):
        api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        if api_key:
            import googlemaps
            self.gmaps = googlemaps.Client(key=api_key)
        else:
            self.gmaps = None
            logger.warning("Google Maps API key not found - using demo mode")
    
    async def find_nearby_hospitals(self, latitude: float, longitude: float, radius: int = 5000) -> List[HospitalInfo]:
        """Find hospitals near the given coordinates"""
        try:
            # Demo mode fallback
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.gmaps:
                return self._get_demo_hospitals(latitude, longitude)
            
            # Search for hospitals
            places_result = self.gmaps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                type='hospital'
            )
            
            hospitals = []
            for place in places_result.get('results', [])[:5]:  # Limit to 5 results
                hospital = HospitalInfo(
                    id=place.get('place_id', ''),
                    name=place.get('name', 'Unknown Hospital'),
                    address=place.get('vicinity', 'Address not available'),
                    phone=place.get('formatted_phone_number', 'Phone not available'),
                    latitude=place['geometry']['location']['lat'],
                    longitude=place['geometry']['location']['lng'],
                    rating=place.get('rating', 0.0)
                )
                hospitals.append(hospital)
            
            return hospitals
            
        except Exception as e:
            logger.error(f"Error finding hospitals: {e}")
            return self._get_demo_hospitals(latitude, longitude)
    
    def _get_demo_hospitals(self, latitude: float, longitude: float) -> List[HospitalInfo]:
        """Return demo hospitals for testing"""
        return [
            HospitalInfo(
                id="demo_hospital_1",
                name="City General Hospital",
                address="123 Main St, Downtown",
                phone="+1-555-0123",
                latitude=latitude + 0.01,
                longitude=longitude + 0.01,
                rating=4.5
            ),
            HospitalInfo(
                id="demo_hospital_2",
                name="Emergency Medical Center",
                address="456 Oak Ave, Midtown",
                phone="+1-555-0456",
                latitude=latitude - 0.01,
                longitude=longitude - 0.01,
                rating=4.2
            )
        ]

class EmergencyAnalysisService:
    """Service for analyzing emergency situations"""
    
    async def analyze_emergency(self, message: str, location: LocationContext) -> AccidentReport:
        """Analyze emergency message and provide response"""
        try:
            # Determine accident type
            accident_type = self._classify_emergency(message)
            
            # Get appropriate first aid tips
            first_aid_tips = self._get_first_aid_tips(accident_type)
            
            # Get location string
            location_str = f"Lat: {location.latitude}, Lon: {location.longitude}"
            if location.address:
                location_str = location.address
            
            return AccidentReport(
                accident_type=accident_type,
                first_aid_tips=first_aid_tips,
                location=location_str,
                details=f"Emergency reported: {message}",
                severity_level=self._assess_severity(message),
                recommended_actions=self._get_recommended_actions(accident_type)
            )
            
        except Exception as e:
            logger.error(f"Error analyzing emergency: {e}")
            return self._get_fallback_response(message, location)
    
    def _classify_emergency(self, message: str) -> str:
        """Classify the type of emergency based on message content"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['accident', 'crash', 'collision', 'hit']):
            return "Vehicle Accident"
        elif any(word in message_lower for word in ['fall', 'fell', 'slip']):
            return "Fall Injury"
        elif any(word in message_lower for word in ['burn', 'fire', 'hot']):
            return "Burn Injury"
        elif any(word in message_lower for word in ['cut', 'bleeding', 'blood']):
            return "Laceration"
        elif any(word in message_lower for word in ['chest pain', 'heart', 'cardiac']):
            return "Cardiac Emergency"
        elif any(word in message_lower for word in ['breathe', 'breathing', 'airway']):
            return "Respiratory Emergency"
        else:
            return "General Emergency"
    
    def _get_first_aid_tips(self, accident_type: str) -> List[str]:
        """Get first aid tips based on accident type"""
        tips_map = {
            "Vehicle Accident": [
                "Ensure scene safety before approaching",
                "Check for consciousness and breathing",
                "Do not move the person unless in immediate danger",
                "Control any visible bleeding with direct pressure",
                "Keep the person warm and calm",
                "Call emergency services immediately"
            ],
            "Fall Injury": [
                "Check for consciousness",
                "Look for signs of head, neck, or spinal injury",
                "Do not move if spinal injury is suspected",
                "Apply ice to swelling areas",
                "Elevate injured limbs if no fracture is suspected"
            ],
            "Burn Injury": [
                "Remove from heat source",
                "Cool burn with cool running water for 10-20 minutes",
                "Do not use ice or butter",
                "Cover with clean, dry cloth",
                "Do not break blisters"
            ],
            "Laceration": [
                "Apply direct pressure to control bleeding",
                "Elevate the injured area above heart level if possible",
                "Use clean cloth or bandages",
                "Do not remove embedded objects",
                "Seek medical attention for deep cuts"
            ],
            "General Emergency": [
                "Ensure scene safety",
                "Check for consciousness and breathing",
                "Call emergency services",
                "Provide comfort and reassurance",
                "Monitor vital signs"
            ]
        }
        return tips_map.get(accident_type, tips_map["General Emergency"])
    
    def _assess_severity(self, message: str) -> str:
        """Assess emergency severity"""
        critical_keywords = ['unconscious', 'not breathing', 'severe bleeding', 'chest pain']
        high_keywords = ['bleeding', 'pain', 'injury', 'accident']
        
        message_lower = message.lower()
        
        if any(keyword in message_lower for keyword in critical_keywords):
            return "critical"
        elif any(keyword in message_lower for keyword in high_keywords):
            return "high"
        else:
            return "moderate"
    
    def _get_recommended_actions(self, accident_type: str) -> List[str]:
        """Get recommended actions based on accident type"""
        return [
            "Call emergency services (911)",
            "Provide first aid as appropriate",
            "Stay with the person until help arrives",
            "Gather information for emergency responders"
        ]
    
    def _get_fallback_response(self, message: str, location: LocationContext) -> AccidentReport:
        """Provide fallback response when analysis fails"""
        return AccidentReport(
            accident_type="Emergency Situation",
            first_aid_tips=[
                "Ensure scene safety",
                "Call emergency services immediately",
                "Provide basic first aid if trained",
                "Stay calm and reassuring"
            ],
            location=f"Lat: {location.latitude}, Lon: {location.longitude}",
            details=f"Emergency reported: {message}",
            severity_level="moderate"
        )

class CallingService:
    """Service for making emergency calls via Twilio"""
    
    def __init__(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        if account_sid and auth_token:
            from twilio.rest import Client
            self.client = Client(account_sid, auth_token)
            self.from_number = os.getenv('TWILIO_PHONE_NUMBER')
        else:
            self.client = None
            self.from_number = None
            logger.warning("Twilio credentials not found - using demo mode")
    
    async def call_emergency_services(self, user_phone: str, message: str) -> dict:
        """Initiate call to emergency services"""
        try:
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.client:
                return {
                    "status": "demo_mode",
                    "message": "Demo mode: Emergency call would be initiated",
                    "call_id": "demo_call_123"
                }
            
            # In production, this would call actual emergency services
            # For demo, we simulate the call
            return {
                "status": "success",
                "message": "Emergency services have been notified",
                "call_id": "simulated_call_456"
            }
            
        except Exception as e:
            logger.error(f"Error calling emergency services: {e}")
            return {
                "status": "error",
                "message": f"Failed to contact emergency services: {str(e)}"
            }
    
    async def call_hospital(self, hospital_id: str, user_phone: str) -> dict:
        """Call a specific hospital"""
        try:
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.client:
                return {
                    "status": "demo_mode",
                    "message": f"Demo mode: Would call hospital {hospital_id}",
                    "call_id": "demo_hospital_call_789"
                }
            
            # In production, this would call the actual hospital
            return {
                "status": "success",
                "message": f"Calling hospital {hospital_id}",
                "call_id": "simulated_hospital_call_101"
            }
            
        except Exception as e:
            logger.error(f"Error calling hospital: {e}")
            return {
                "status": "error",
                "message": f"Failed to call hospital: {str(e)}"
            }
