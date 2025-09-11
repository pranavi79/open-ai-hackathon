"""
Cost Protection System for Emergency Response AI
Tracks API usage and prevents unexpected charges
"""
import json
import os
from datetime import datetime
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class CostProtection:
    """Cost protection and usage tracking system"""
    
    def __init__(self, usage_file: str = "api_usage.json"):
        self.usage_file = usage_file
        self.ensure_usage_file_exists()
    
    def ensure_usage_file_exists(self):
        """Ensure the usage tracking file exists"""
        if not os.path.exists(self.usage_file):
            initial_data = {
                "usage": {},
                "daily_limits": {
                    "openai_requests": int(os.getenv("MAX_DAILY_OPENAI_REQUESTS", "50")),
                    "google_maps_requests": int(os.getenv("MAX_DAILY_GOOGLE_REQUESTS", "100")),
                    "twilio_calls": int(os.getenv("MAX_DAILY_TWILIO_CALLS", "5")),
                    "twilio_minutes": int(os.getenv("MAX_DAILY_TWILIO_MINUTES", "10"))
                }
            }
            
            with open(self.usage_file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def is_demo_mode(self) -> bool:
        """Check if demo mode is enabled"""
        return os.getenv("DEMO_MODE", "true").lower() == "true"
    
    def set_demo_mode(self, enabled: bool):
        """Enable or disable demo mode"""
        # This would update the .env file in a real implementation
        # For now, we'll just update the environment variable
        os.environ["DEMO_MODE"] = "true" if enabled else "false"
        logger.info(f"Demo mode {'enabled' if enabled else 'disabled'}")
    
    def enable_demo_mode(self):
        """Enable demo mode"""
        self.set_demo_mode(True)
    
    def disable_demo_mode(self):
        """Disable demo mode"""
        self.set_demo_mode(False)

    def can_make_request(self, request_type: str) -> bool:
        """Check if a request can be made within daily limits"""
        if self.is_demo_mode():
            return True  # Demo mode allows all requests
        
        try:
            with open(self.usage_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            today_usage = data.get("usage", {}).get(today, {})
            daily_limits = data.get("daily_limits", {})
            
            current_usage = today_usage.get(request_type, 0)
            limit = daily_limits.get(request_type, 0)
            
            return current_usage < limit
            
        except Exception as e:
            logger.error(f"Error checking request limits: {e}")
            return True  # Allow request if we can't check limits
    
    def track_request(self, request_type: str, cost: float = 0.0):
        """Track a completed API request"""
        try:
            with open(self.usage_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            # Initialize today's usage if not exists
            if "usage" not in data:
                data["usage"] = {}
            if today not in data["usage"]:
                data["usage"][today] = {}
            
            # Increment usage counter
            current_count = data["usage"][today].get(request_type, 0)
            data["usage"][today][request_type] = current_count + 1
            
            # Track cost if provided
            if cost > 0:
                cost_key = f"{request_type}_cost"
                current_cost = data["usage"][today].get(cost_key, 0.0)
                data["usage"][today][cost_key] = current_cost + cost
            
            # Save updated data
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.info(f"Tracked {request_type} request for {today}")
            
        except Exception as e:
            logger.error(f"Error tracking request: {e}")
    
    def get_usage_report(self) -> Dict[str, Any]:
        """Get current usage report"""
        try:
            with open(self.usage_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            today_usage = data.get("usage", {}).get(today, {})
            daily_limits = data.get("daily_limits", {})
            
            # Calculate costs
            openai_requests = today_usage.get("openai_requests", 0)
            google_requests = today_usage.get("google_maps_requests", 0)
            twilio_calls = today_usage.get("twilio_calls", 0)
            twilio_minutes = today_usage.get("twilio_minutes", 0)
            
            # Estimated costs (approximate)
            openai_cost = openai_requests * 0.002
            google_cost = google_requests * 0.005
            twilio_cost = twilio_minutes * 0.013
            total_cost = openai_cost + google_cost + twilio_cost
            
            return {
                "date": today,
                "demo_mode": self.is_demo_mode(),
                "usage": {
                    "openai_requests": {
                        "used": openai_requests,
                        "limit": daily_limits.get("openai_requests", 50),
                        "cost": round(openai_cost, 4)
                    },
                    "google_maps_requests": {
                        "used": google_requests,
                        "limit": daily_limits.get("google_maps_requests", 100),
                        "cost": round(google_cost, 4)
                    },
                    "twilio_calls": {
                        "used": twilio_calls,
                        "limit": daily_limits.get("twilio_calls", 5),
                        "minutes": twilio_minutes,
                        "cost": round(twilio_cost, 4)
                    }
                },
                "total_cost": round(total_cost, 4),
                "status": "demo_mode" if self.is_demo_mode() else "live"
            }
            
        except Exception as e:
            logger.error(f"Error generating usage report: {e}")
            return {
                "error": "Could not generate usage report",
                "demo_mode": self.is_demo_mode()
            }
    
    def get_current_usage(self) -> Dict[str, Any]:
        """Get current usage - alias for get_usage_report for compatibility"""
        return self.get_usage_report()
    
    def reset_daily_usage(self):
        """Reset today's usage counters"""
        try:
            with open(self.usage_file, 'r') as f:
                data = json.load(f)
            
            today = datetime.now().strftime("%Y-%m-%d")
            
            if today in data.get("usage", {}):
                del data["usage"][today]
                
                with open(self.usage_file, 'w') as f:
                    json.dump(data, f, indent=2)
                
                logger.info(f"Reset usage counters for {today}")
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error resetting usage: {e}")
            return False
