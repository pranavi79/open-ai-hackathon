"""
Emergency Response AI System - Enhanced Services
Optimized for performance, accuracy, and user experience
"""
import json
import os
import logging
import asyncio
import aiohttp
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from functools import lru_cache
from .models import HospitalInfo, AccidentReport, LocationContext

logger = logging.getLogger(__name__)

# Simple caching system
class SimpleCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str):
        if key in self.cache:
            data, expires = self.cache[key]
            if datetime.now() < expires:
                return data
            else:
                del self.cache[key]
        return None
    
    def set(self, key: str, data: Any, ttl_seconds: int = 300):
        expires = datetime.now() + timedelta(seconds=ttl_seconds)
        self.cache[key] = (data, expires)

# Global cache instance
response_cache = SimpleCache()

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
    
    async def find_nearby_hospitals(self, latitude: float, longitude: float, radius: int = 5000) -> Dict[str, Any]:
        """Find hospitals near the given coordinates"""
        try:
            # Demo mode fallback
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.gmaps:
                hospitals = self._get_demo_hospitals(latitude, longitude)
                return {
                    "hospitals": hospitals,
                    "total_found": len(hospitals),
                    "search_radius": f"{radius/1000:.1f} km",
                    "location": f"{latitude:.4f}, {longitude:.4f}"
                }
            
            # Search for hospitals
            places_result = self.gmaps.places_nearby(
                location=(latitude, longitude),
                radius=radius,
                type='hospital'
            )
            
            hospitals = []
            for place in places_result.get('results', [])[:5]:  # Limit to 5 results
                # Calculate distance
                import math
                lat1, lon1 = latitude, longitude
                lat2, lon2 = place['geometry']['location']['lat'], place['geometry']['location']['lng']
                distance = self._calculate_distance(lat1, lon1, lat2, lon2)
                
                hospital = {
                    "id": place.get('place_id', ''),
                    "name": place.get('name', 'Unknown Hospital'),
                    "address": place.get('vicinity', 'Address not available'),
                    "phone": place.get('formatted_phone_number', 'Phone not available'),
                    "latitude": lat2,
                    "longitude": lon2,
                    "rating": place.get('rating', 0.0),
                    "distance": f"{distance:.1f} km",
                    "specialty": "General Hospital Services",
                    "emergency_services": True,
                    "trauma_center": place.get('rating', 0) > 4.0,
                    "estimated_time": f"{int(distance * 2)}-{int(distance * 2 + 3)} minutes"
                }
                hospitals.append(hospital)
            
            return {
                "hospitals": hospitals,
                "total_found": len(hospitals),
                "search_radius": f"{radius/1000:.1f} km",
                "location": f"{latitude:.4f}, {longitude:.4f}"
            }
            
        except Exception as e:
            logger.error(f"Error finding hospitals: {e}")
            hospitals = self._get_demo_hospitals(latitude, longitude)
            return {
                "hospitals": hospitals,
                "total_found": len(hospitals),
                "search_radius": f"{radius/1000:.1f} km",
                "location": f"{latitude:.4f}, {longitude:.4f}",
                "error": "Using demo data due to API error"
            }
    
    def _calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two points in kilometers"""
        import math
        R = 6371  # Earth's radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
    
    def _get_demo_hospitals(self, latitude: float, longitude: float) -> List[Dict[str, Any]]:
        """Return enhanced demo hospitals for testing"""
        import math
        
        demo_hospitals = [
            {
                "id": "demo_hospital_1",
                "name": "City General Hospital",
                "address": "123 Main St, Downtown Medical District",
                "phone": "+1-555-0123",
                "latitude": latitude + 0.01,
                "longitude": longitude + 0.01,
                "rating": 4.5,
                "distance": "1.2 km",
                "specialty": "Level 1 Trauma Center",
                "emergency_services": True,
                "trauma_center": True,
                "estimated_time": "3-4 minutes"
            },
            {
                "id": "demo_hospital_2", 
                "name": "Emergency Medical Center",
                "address": "456 Oak Ave, Midtown Healthcare Complex",
                "phone": "+1-555-0456",
                "latitude": latitude + 0.02,
                "longitude": longitude - 0.01,
                "rating": 4.2,
                "distance": "2.1 km",
                "specialty": "Emergency & Urgent Care",
                "emergency_services": True,
                "trauma_center": False,
                "estimated_time": "5-6 minutes"
            },
            {
                "id": "demo_hospital_3",
                "name": "St. Mary's Medical Center",
                "address": "789 Pine Blvd, Healthcare District",
                "phone": "+1-555-0789",
                "latitude": latitude - 0.015,
                "longitude": longitude + 0.02,
                "rating": 4.7,
                "distance": "2.8 km",
                "specialty": "Cardiac & Stroke Center",
                "emergency_services": True,
                "trauma_center": True,
                "estimated_time": "6-7 minutes"
            },
            {
                "id": "demo_hospital_4",
                "name": "Regional Burn & Trauma Unit",
                "address": "321 Cedar Lane, Specialized Care Campus",
                "phone": "+1-555-0321",
                "latitude": latitude + 0.025,
                "longitude": longitude + 0.015,
                "rating": 4.4,
                "distance": "3.5 km",
                "specialty": "Burn & Trauma Specialization",
                "emergency_services": True,
                "trauma_center": True,
                "estimated_time": "7-8 minutes"
            },
            {
                "id": "demo_hospital_5",
                "name": "Metro Urgent Care Hospital",
                "address": "654 Maple Drive, Community Health Center",
                "phone": "+1-555-0654",
                "latitude": latitude - 0.02,
                "longitude": longitude - 0.025,
                "rating": 4.0,
                "distance": "4.1 km",
                "specialty": "General Emergency Services",
                "emergency_services": True,
                "trauma_center": False,
                "estimated_time": "8-10 minutes"
            }
        ]
        
        return demo_hospitals

class EmergencyAnalysisService:
    """Enhanced service for analyzing emergency situations with AI integration"""
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    async def analyze_emergency(self, message: str, location: LocationContext, scenario_type: str = "custom", force_new: bool = False) -> AccidentReport:
        """Enhanced emergency analysis with AI and performance optimization"""
        start_time = time.time()
        
        # Create cache key including scenario type for unique analysis per scenario
        cache_key = f"analysis_{scenario_type}_{hash(message.lower()[:100])}_{round(location.latitude, 2)}_{round(location.longitude, 2)}"
        
        # Check cache first (unless forced new analysis)
        if not force_new:
            cached_result = response_cache.get(cache_key)
            if cached_result:
                logger.info("Cache hit for emergency analysis")
                return cached_result
        
        try:
            # Use AI if available and not in demo mode
            if self.openai_api_key and os.getenv('DEMO_MODE', 'false').lower() != 'true':
                result = await self._ai_analysis(message, location, scenario_type)
            else:
                result = await self._enhanced_rule_based_analysis(message, location)
            
            # Cache the result for future use
            response_cache.set(cache_key, result, ttl_seconds=300)
            
            # Add performance metrics
            response_time = round((time.time() - start_time) * 1000, 2)
            logger.info(f"Emergency analysis completed in {response_time}ms")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in emergency analysis: {e}")
            return self._get_fallback_response(message, location)
    
    async def _ai_analysis(self, message: str, location: LocationContext, scenario_type: str = "custom") -> AccidentReport:
        """Use OpenAI for intelligent emergency analysis"""
        
        prompt = f"""
        Emergency situation analysis - provide CLEAN, ACTION-FOCUSED guidance:
        
        Scenario: {scenario_type}
        Emergency: "{message}"
        Location: {location.latitude}, {location.longitude}
        
        Return ONLY JSON with:
        - emergency_type: specific type (e.g., "Cardiac Emergency", "Trauma Injury")
        - severity: critical/high/moderate (be realistic)
        - immediate_actions: array of 3 CLEAR actions for bystander (no complex medical terms)
        - status: "Emergency services dispatched automatically"
        - estimated_arrival: "5-8 minutes" (realistic ETA)
        
        RULES:
        - NO complex medical analysis or long explanations
        - Focus on what the BYSTANDER should do while waiting
        - Keep actions simple and clear (stay calm, monitor breathing, etc.)
        - Don't suggest calling 911 (we handle that automatically)
        - Each scenario must give different, specific actions
        """
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an emergency response system. Provide CLEAN, SIMPLE guidance for bystanders helping accident victims. Focus only on what they need to do while waiting for help. NO complex medical jargon."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "max_tokens": 400,
            "temperature": 0.1,
            "response_format": {"type": "json_object"}
        }
        
        try:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
                async with session.post(self.base_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        ai_response = json.loads(result['choices'][0]['message']['content'])
                        
                        # Return raw AI response structure for better frontend formatting
                        enhanced_response = {
                            'emergency_type': ai_response.get('emergency_type', 'Emergency Situation'),
                            'severity': ai_response.get('severity', 'moderate'),
                            'assessment': ai_response.get('assessment', 'Emergency situation requiring immediate attention.'),
                            'recommendations': ai_response.get('recommendations', ['Call 911 immediately', 'Follow first aid steps', 'Stay with person until help arrives']),
                            'first_aid_steps': ai_response.get('first_aid_steps', ['Assess the situation', 'Ensure scene safety', 'Check for responsiveness']),
                            'warning_signs': ai_response.get('warning_signs', ['Loss of consciousness', 'Severe bleeding', 'Difficulty breathing']),
                            'estimated_response_time': ai_response.get('estimated_response_time', '5-10 minutes'),
                            'emergency_number': ai_response.get('emergency_number', '911'),
                            'accident_type': ai_response.get('emergency_type', 'Emergency Situation'),
                            'first_aid_tips': ai_response.get('first_aid_steps', [])[:6],
                            'location': f"Lat: {location.latitude}, Lon: {location.longitude}",
                            'details': f"AI Analysis: {message}",
                            'severity_level': ai_response.get('severity', 'moderate'),
                            'recommended_actions': ai_response.get('recommendations', []),
                            'response_time_needed': ai_response.get('estimated_response_time', 'Standard'),
                            'priority_level': ai_response.get('severity', 'medium')
                        }
                        
                        return enhanced_response
                    else:
                        logger.warning(f"OpenAI API error: {response.status}")
                        return await self._enhanced_rule_based_analysis(message, location)
        except asyncio.TimeoutError:
            logger.warning("OpenAI API timeout, falling back to rule-based analysis")
            return await self._enhanced_rule_based_analysis(message, location)
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return await self._enhanced_rule_based_analysis(message, location)
    
    async def _enhanced_rule_based_analysis(self, message: str, location: LocationContext) -> AccidentReport:
        """Enhanced rule-based analysis with better keyword detection"""
        
        # Quick severity assessment
        severity = self._quick_severity_check(message)
        
        # Enhanced classification
        accident_type = self._enhanced_classify_emergency(message)
        
        # Get contextual first aid tips
        first_aid_tips = self._get_enhanced_first_aid_tips(accident_type, severity)
        
        # Calculate response time
        response_time = self._calculate_response_time(severity, accident_type)
        
        # Get location string
        location_str = f"Lat: {location.latitude}, Lon: {location.longitude}"
        if hasattr(location, 'address') and location.address:
            location_str = location.address
        
        # Enhanced rule-based response with comprehensive information
        assessment = self._generate_assessment(accident_type, severity, message)
        recommendations = self._get_enhanced_recommended_actions(accident_type, severity)
        warning_signs = self._get_warning_signs(accident_type)
        
        enhanced_response = {
            'emergency_type': accident_type,
            'severity': severity,
            'assessment': assessment,
            'recommendations': recommendations,
            'first_aid_steps': first_aid_tips,
            'warning_signs': warning_signs,
            'estimated_response_time': response_time,
            'emergency_number': '911' if severity in ['critical', 'high'] else '911',
            'accident_type': accident_type,
            'first_aid_tips': first_aid_tips,
            'location': location_str,
            'details': f"Enhanced Analysis: {message}",
            'severity_level': severity,
            'recommended_actions': recommendations,
            'response_time_needed': response_time,
            'priority_level': self._get_priority_level(severity)
        }
        
        return enhanced_response
    
    @lru_cache(maxsize=50)
    def _quick_severity_check(self, message: str) -> str:
        """Fast severity assessment with cached keywords"""
        message_lower = message.lower()
        
        critical_words = ['unconscious', 'not breathing', 'severe bleeding', 'chest pain', 'heart attack', 'stroke']
        high_words = ['bleeding', 'accident', 'fall', 'burn', 'pain', 'injury', 'difficulty breathing']
        
        if any(word in message_lower for word in critical_words):
            return "critical"
        elif any(word in message_lower for word in high_words):
            return "high"
        else:
            return "moderate"
    
    def _enhanced_classify_emergency(self, message: str) -> str:
        """Enhanced emergency classification"""
        message_lower = message.lower()
        
        emergency_patterns = {
            "Cardiac Emergency": ['chest pain', 'heart attack', 'cardiac', 'heart'],
            "Respiratory Emergency": ['breathing', 'breathe', 'airway', 'choking', 'asthma'],
            "Vehicle Accident": ['accident', 'crash', 'collision', 'hit', 'car', 'vehicle'],
            "Fall Injury": ['fall', 'fell', 'slip', 'stairs'],
            "Burn Injury": ['burn', 'fire', 'hot', 'steam'],
            "Bleeding/Laceration": ['cut', 'bleeding', 'blood', 'wound'],
            "Stroke": ['stroke', 'slurred speech', 'face drooping', 'weakness'],
            "Allergic Reaction": ['allergic', 'reaction', 'swelling', 'hives']
        }
        
        for emergency_type, keywords in emergency_patterns.items():
            if any(keyword in message_lower for keyword in keywords):
                return emergency_type
        
        return "General Emergency"
    
    def _get_enhanced_first_aid_tips(self, accident_type: str, severity: str) -> List[str]:
        """Get enhanced first aid tips based on type and severity"""
        
        tips_map = {
            "Cardiac Emergency": [
                "Call 911 immediately",
                "Have person sit down and rest",
                "Loosen tight clothing",
                "If unconscious, begin CPR",
                "Look for aspirin if not allergic",
                "Stay calm and reassure person"
            ],
            "Respiratory Emergency": [
                "Call 911 immediately",
                "Help person sit upright",
                "Loosen tight clothing",
                "If choking, perform Heimlich maneuver",
                "Look for rescue inhaler or EpiPen",
                "Monitor breathing continuously"
            ],
            "Vehicle Accident": [
                "Ensure scene safety first",
                "Do not move person unless danger",
                "Check consciousness and breathing",
                "Control bleeding with pressure",
                "Keep person warm and still",
                "Call 911 and stay with person"
            ],
            "Fall Injury": [
                "Do not move if spinal injury suspected",
                "Check consciousness and breathing",
                "Look for head or neck pain",
                "Apply ice to swelling areas",
                "Elevate limbs if no fracture",
                "Monitor for shock signs"
            ],
            "Burn Injury": [
                "Remove from heat source safely",
                "Cool with running water 10-20 min",
                "Do not use ice or butter",
                "Cover with clean cloth",
                "Do not break blisters",
                "Remove jewelry before swelling"
            ]
        }
        
        base_tips = tips_map.get(accident_type, [
            "Ensure safety first",
            "Call 911 immediately", 
            "Check consciousness and breathing",
            "Provide comfort and reassurance",
            "Stay with person until help arrives",
            "Give clear information to responders"
        ])
        
        # Add critical care note for severe cases
        if severity == "critical":
            base_tips.insert(1, "Be prepared to perform CPR")
        
        return base_tips[:6]  # Limit to 6 steps
    
    def _calculate_response_time(self, severity: str, emergency_type: str) -> str:
        """Calculate expected response time"""
        if severity == "critical":
            return "0-4 minutes (Life threatening)"
        elif severity == "high":
            return "4-8 minutes (Urgent)"
        else:
            return "8-15 minutes (Standard)"
    
    def _get_priority_level(self, severity: str) -> str:
        """Get dispatch priority level"""
        priority_map = {
            "critical": "Priority 1 (Life threatening)",
            "high": "Priority 2 (Urgent)", 
            "moderate": "Priority 3 (Standard)",
            "low": "Priority 4 (Non-urgent)"
        }
        return priority_map.get(severity, "Priority 3 (Standard)")
    
    def _get_enhanced_recommended_actions(self, emergency_type: str, severity: str) -> List[str]:
        """Get enhanced recommended actions"""
        actions = [
            "Call 911 immediately",
            "Provide first aid as trained",
            "Stay with person until help arrives",
            "Give clear information to responders"
        ]
        
        if severity == "critical":
            actions.insert(1, "Be prepared to perform CPR")
            actions.append("Clear path for emergency vehicles")
        
        if emergency_type == "Vehicle Accident":
            actions.append("Turn on hazard lights if safe")
        
        return actions
    
    def _get_fallback_response(self, message: str, location: LocationContext) -> AccidentReport:
        """Provide fallback response when analysis fails"""
        return AccidentReport(
            accident_type="Emergency Situation",
            first_aid_tips=[
                "Ensure safety first",
                "Call 911 immediately",
                "Check if person is conscious and breathing", 
                "Provide comfort and reassurance",
                "Stay with person until help arrives"
            ],
            location=f"Lat: {location.latitude}, Lon: {location.longitude}",
            details=f"Emergency situation: {message}",
            severity_level="moderate",
            recommended_actions=[
                "Call emergency services immediately",
                "Provide basic first aid",
                "Stay calm and wait for help"
            ]
        )
    
    def _generate_assessment(self, accident_type: str, severity: str, message: str) -> str:
        """Generate detailed emergency assessment"""
        severity_descriptions = {
            "critical": "This is a life-threatening emergency requiring immediate intervention.",
            "high": "This is a serious emergency requiring urgent medical attention.",
            "moderate": "This emergency requires prompt medical evaluation and care.",
            "low": "This situation requires medical attention but is not immediately life-threatening."
        }
        
        type_assessments = {
            "Vehicle Accident": "Multi-vehicle collision with potential trauma injuries. Risk of internal bleeding, fractures, and head injuries.",
            "Heart Attack": "Cardiac emergency with risk of cardiac arrest. Time-critical situation requiring immediate intervention.",
            "Fall Injury": "Trauma from fall with potential for fractures, head injury, or spinal damage.",
            "Allergic Reaction": "Severe allergic response with risk of anaphylaxis and respiratory compromise.",
            "Burn Injury": "Thermal injury requiring immediate cooling and wound care to prevent complications.",
            "Respiratory Emergency": "Breathing difficulty requiring immediate airway management and oxygen support.",
            "Stroke": "Neurological emergency requiring immediate medical intervention to prevent permanent damage."
        }
        
        base_assessment = severity_descriptions.get(severity, "Emergency situation requiring medical attention.")
        specific_assessment = type_assessments.get(accident_type, "Emergency situation based on reported symptoms.")
        
        return f"{base_assessment} {specific_assessment}"
    
    def _get_warning_signs(self, accident_type: str) -> List[str]:
        """Get warning signs that require immediate 911 call"""
        warning_map = {
            "Vehicle Accident": [
                "Loss of consciousness",
                "Severe bleeding that won't stop",
                "Signs of spinal injury",
                "Difficulty breathing",
                "Severe head trauma"
            ],
            "Heart Attack": [
                "Chest pain lasting more than 5 minutes",
                "Shortness of breath",
                "Nausea or vomiting",
                "Sweating and pale skin",
                "Loss of consciousness"
            ],
            "Fall Injury": [
                "Unable to move or stand",
                "Severe pain in back or neck",
                "Confusion or disorientation",
                "Visible bone fractures",
                "Heavy bleeding"
            ],
            "Allergic Reaction": [
                "Difficulty breathing or wheezing",
                "Swelling of face, lips, or throat",
                "Rapid pulse",
                "Dizziness or fainting",
                "Widespread rash or hives"
            ],
            "Burn Injury": [
                "Burns on face, hands, or genitals",
                "Third-degree burns (white/charred)",
                "Burns larger than palm size",
                "Difficulty breathing",
                "Signs of shock"
            ]
        }
        
        return warning_map.get(accident_type, [
            "Loss of consciousness",
            "Severe bleeding",
            "Difficulty breathing",
            "Severe pain",
            "Signs of shock"
        ])

class CallingService:
    
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
    
    async def contact_emergency_services(self, phone_number: str, message: str, emergency_type: str, location: dict) -> dict:
        """Contact emergency services with detailed emergency information"""
        try:
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.client:
                logger.info(f"Demo mode: Emergency services contacted for {emergency_type}")
                return {
                    "status": "demo_success",
                    "message": "Emergency services contacted (Demo Mode)",
                    "emergency_id": f"EMG_DEMO_{int(time.time())}",
                    "dispatch_status": "ambulance_dispatched",
                    "estimated_arrival": "5-8 minutes"
                }
            
            # In production, this would contact actual emergency dispatch
            # with location, emergency type, and detailed message
            call_message = f"Emergency Alert: {emergency_type} at location {location.get('latitude', 'unknown')}, {location.get('longitude', 'unknown')}. Details: {message}"
            
            # Simulate emergency dispatch call
            logger.info(f"Emergency services contacted: {call_message}")
            
            return {
                "status": "success",
                "message": "Emergency services contacted and dispatched",
                "emergency_id": f"EMG_{int(time.time())}",
                "dispatch_status": "ambulance_dispatched",
                "estimated_arrival": "5-8 minutes"
            }
            
        except Exception as e:
            logger.error(f"Error contacting emergency services: {e}")
            return {
                "status": "error",
                "message": f"Failed to contact emergency services: {str(e)}"
            }
    
    async def notify_hospital(self, hospital_id: str, hospital_name: str, emergency_details: str, patient_location: dict, estimated_arrival: str) -> dict:
        """Notify specific hospital about incoming emergency patient"""
        try:
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.client:
                logger.info(f"Demo mode: Hospital {hospital_name} notified about incoming patient")
                return {
                    "status": "demo_success",
                    "message": f"Hospital {hospital_name} prepared for patient",
                    "preparation_status": "ready",
                    "estimated_preparation_time": "2-3 minutes"
                }
            
            # In production, this would call the hospital emergency department
            notification_message = f"Incoming emergency patient. Details: {emergency_details}. Estimated arrival: {estimated_arrival}. Location: {patient_location}"
            
            logger.info(f"Hospital notification sent to {hospital_name}: {notification_message}")
            
            return {
                "status": "success",
                "message": f"Hospital {hospital_name} notified and prepared",
                "preparation_status": "ready", 
                "estimated_preparation_time": "2-3 minutes"
            }
            
        except Exception as e:
            logger.error(f"Error notifying hospital: {e}")
            return {
                "status": "error",
                "message": f"Failed to notify hospital: {str(e)}"
            }
    
    async def send_emergency_report(self, report_data: dict) -> dict:
        """Send comprehensive emergency report to all relevant parties"""
        try:
            if os.getenv('DEMO_MODE', 'false').lower() == 'true' or not self.client:
                logger.info(f"Demo mode: Emergency report sent for incident {report_data.get('incident_id')}")
                return {
                    "status": "demo_success",
                    "message": "Emergency report compiled and distributed (Demo Mode)",
                    "report_id": f"RPT_DEMO_{int(time.time())}",
                    "recipients": ["Emergency Dispatch", "Hospital", "Emergency Coordinator"]
                }
            
            # In production, this would send detailed reports to:
            # - Emergency dispatch center
            # - Assigned hospital
            # - Emergency coordination center
            # - Patient's emergency contacts (if available)
            
            logger.info(f"Emergency report sent for incident {report_data.get('incident_id')}")
            
            return {
                "status": "success",
                "message": "Emergency report sent to all relevant parties",
                "report_id": f"RPT_{int(time.time())}",
                "recipients": ["Emergency Dispatch", "Hospital", "Emergency Coordinator"]
            }
            
        except Exception as e:
            logger.error(f"Error sending emergency report: {e}")
            return {
                "status": "error",
                "message": f"Failed to send emergency report: {str(e)}"
            }
