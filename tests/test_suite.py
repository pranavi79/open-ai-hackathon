"""
Comprehensive test suite for Emergency Response AI System
Tests all components including API endpoints, AI integration, and safety features
"""
import pytest
import requests
import json
import time
from typing import Dict, List

# Test configuration
BASE_URL = "http://127.0.0.1:8000/api/v1"
TEST_TIMEOUT = 30  # seconds

class EmergencyResponseTester:
    """Comprehensive test suite for the emergency response system"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.test_results = []
    
    def run_all_tests(self) -> Dict:
        """Run complete test suite and return results"""
        print("[START] Starting Emergency Response System Test Suite")
        print("=" * 60)
        
        tests = [
            ("System Health Check", self.test_system_health),
            ("API Documentation", self.test_api_docs),
            ("Vehicle Accident Response", self.test_vehicle_accident),
            ("Medical Emergency Response", self.test_medical_emergency),
            ("Fire Emergency Response", self.test_fire_emergency),
            ("Critical Emergency Override", self.test_critical_emergency),
            ("Prank Detection", self.test_prank_detection),
            ("Invalid Input Handling", self.test_invalid_input),
            ("Global Location Support", self.test_global_locations),
            ("Performance Test", self.test_performance),
            ("Calling Capability Check", self.test_calling_capability),
            ("OpenAI Integration", self.test_openai_integration),
            ("Google Maps Integration", self.test_google_maps),
            ("Safety Guardrails", self.test_safety_guardrails)
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            try:
                print(f"\n[TEST] Running: {test_name}")
                result = test_func()
                if result["passed"]:
                    print(f"[OK] PASSED: {test_name}")
                    passed += 1
                else:
                    print(f"[ERROR] FAILED: {test_name} - {result['error']}")
                    failed += 1
                self.test_results.append({"name": test_name, "result": result})
            except Exception as e:
                print(f"💥 ERROR: {test_name} - {str(e)}")
                failed += 1
                self.test_results.append({"name": test_name, "result": {"passed": False, "error": str(e)}})
        
        print("\n" + "=" * 60)
        print(f"[STATS] TEST SUMMARY: {passed} passed, {failed} failed")
        
        return {
            "total_tests": len(tests),
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / len(tests)) * 100,
            "details": self.test_results
        }
    
    def test_system_health(self) -> Dict:
        """Test system health endpoint"""
        try:
            response = requests.get(f"{self.base_url}/", timeout=5)
            data = response.json()
            
            # Check response structure
            required_fields = ["message", "services", "ai_models"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return {"passed": False, "error": f"Missing fields: {missing_fields}"}
            
            if response.status_code != 200:
                return {"passed": False, "error": f"Status code: {response.status_code}"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_api_docs(self) -> Dict:
        """Test API documentation accessibility"""
        try:
            response = requests.get(f"http://127.0.0.1:8000/docs", timeout=5)
            if response.status_code != 200:
                return {"passed": False, "error": f"Docs not accessible: {response.status_code}"}
            
            # Check if it contains Swagger UI
            if "swagger-ui" not in response.text.lower():
                return {"passed": False, "error": "Swagger UI not found"}
            
            return {"passed": True, "data": "API documentation accessible"}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_vehicle_accident(self) -> Dict:
        """Test vehicle accident emergency response"""
        try:
            payload = {
                "request": "Car accident on Highway 101, person unconscious",
                "latitude": "37.4419",
                "longitude": "-122.1430"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Validate response structure
            required_fields = ["accident_type", "first_aid_tips", "location", "details"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return {"passed": False, "error": f"Missing fields: {missing_fields}"}
            
            # Check if accident type is relevant
            if "vehicle" not in data["accident_type"].lower() and "accident" not in data["accident_type"].lower():
                return {"passed": False, "error": f"Unexpected accident type: {data['accident_type']}"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_medical_emergency(self) -> Dict:
        """Test medical emergency response"""
        try:
            payload = {
                "request": "Person having chest pains and difficulty breathing",
                "latitude": "40.7128",
                "longitude": "-74.0060"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check for cardiac/medical classification
            accident_type = data["accident_type"].lower()
            if not any(word in accident_type for word in ["cardiac", "medical", "heart", "emergency"]):
                return {"passed": False, "error": f"Unexpected classification: {data['accident_type']}"}
            
            # Check for 911 recommendation
            first_aid = data["first_aid_tips"].lower()
            if "911" not in first_aid and "call" not in first_aid:
                return {"passed": False, "error": "Missing 911 recommendation"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_fire_emergency(self) -> Dict:
        """Test fire emergency response"""
        try:
            payload = {
                "request": "Kitchen fire spreading, smoke everywhere",
                "latitude": "34.0522",
                "longitude": "-118.2437"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check for fire classification
            if "fire" not in data["accident_type"].lower():
                return {"passed": False, "error": f"Fire not detected: {data['accident_type']}"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_critical_emergency(self) -> Dict:
        """Test critical emergency override"""
        try:
            payload = {
                "request": "someone is dying, not breathing, cardiac arrest",
                "latitude": "37.7749",
                "longitude": "-122.4194"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check for critical emergency detection
            if data["accident_type"] != "CRITICAL_EMERGENCY":
                return {"passed": False, "error": f"Critical emergency not detected: {data['accident_type']}"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_prank_detection(self) -> Dict:
        """Test prank/fake emergency detection"""
        try:
            payload = {
                "request": "this is just a test lol haha fake emergency",
                "latitude": "37.4419",
                "longitude": "-122.1430"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check for prank detection in safety alerts
            first_aid = data["first_aid_tips"]
            if "PRANK_DETECTED" not in first_aid:
                return {"passed": False, "error": "Prank not detected"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_invalid_input(self) -> Dict:
        """Test handling of invalid input"""
        try:
            payload = {
                "request": "",
                "latitude": "invalid",
                "longitude": "invalid"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=10)
            
            # Should not crash, should provide fallback response
            if response.status_code >= 500:
                return {"passed": False, "error": f"Server error: {response.status_code}"}
            
            data = response.json()
            if "fallback" not in data["first_aid_tips"].lower():
                return {"passed": False, "error": "No fallback response provided"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_global_locations(self) -> Dict:
        """Test global location support"""
        try:
            # Test London coordinates
            payload = {
                "request": "Minor injury need hospital",
                "latitude": "51.5074",
                "longitude": "-0.1278"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check if hospitals were found
            if "Nearest Hospitals:" not in data["location"]:
                return {"passed": False, "error": "No hospitals found for London"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_performance(self) -> Dict:
        """Test system performance"""
        try:
            start_time = time.time()
            
            payload = {
                "request": "Minor cut on finger",
                "latitude": "37.4419",
                "longitude": "-122.1430"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response_time > 5:  # Should respond within 5 seconds
                return {"passed": False, "error": f"Response too slow: {response_time:.2f}s"}
            
            return {"passed": True, "data": {"response_time": f"{response_time:.2f}s"}}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_calling_capability(self) -> Dict:
        """Test calling capability check"""
        try:
            response = requests.get(f"{self.base_url}/calling-capability", timeout=5)
            data = response.json()
            
            # Should have calling status information
            required_fields = ["calling_available", "message", "configuration_needed"]
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                return {"passed": False, "error": f"Missing fields: {missing_fields}"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_openai_integration(self) -> Dict:
        """Test OpenAI GPT-3 integration"""
        try:
            payload = {
                "request": "Bicycle accident, rider fell",
                "latitude": "37.4419",
                "longitude": "-122.1430"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check if AI analysis is present
            if "AI Analysis:" not in data["details"]:
                return {"passed": False, "error": "AI analysis not found in response"}
            
            # Check if accident classification is reasonable
            accident_type = data["accident_type"].lower()
            if not any(word in accident_type for word in ["bicycle", "fall", "accident", "injury"]):
                return {"passed": False, "error": f"Poor AI classification: {data['accident_type']}"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_google_maps(self) -> Dict:
        """Test Google Maps integration"""
        try:
            payload = {
                "request": "Need nearest hospital",
                "latitude": "37.4419",
                "longitude": "-122.1430"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check hospital information format
            location_info = data["location"]
            if "Nearest Hospitals:" not in location_info:
                return {"passed": False, "error": "Hospital search failed"}
            
            # Check for hospital details (rating, phone)
            if "Rating:" not in location_info or "Phone:" not in location_info:
                return {"passed": False, "error": "Hospital details missing"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}
    
    def test_safety_guardrails(self) -> Dict:
        """Test safety guardrails functionality"""
        try:
            # Test with critical keywords
            payload = {
                "request": "massive bleeding, unconscious victim",
                "latitude": "37.4419",
                "longitude": "-122.1430"
            }
            
            response = requests.post(f"{self.base_url}/ask", json=payload, timeout=TEST_TIMEOUT)
            data = response.json()
            
            # Check for safety alerts
            first_aid = data["first_aid_tips"]
            if "CRITICAL_EMERGENCY" not in first_aid:
                return {"passed": False, "error": "Critical emergency not flagged"}
            
            return {"passed": True, "data": data}
            
        except Exception as e:
            return {"passed": False, "error": str(e)}

def run_tests():
    """Main function to run all tests"""
    tester = EmergencyResponseTester()
    results = tester.run_all_tests()
    
    # Save results to file
    with open("test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Detailed results saved to: test_results.json")
    return results

if __name__ == "__main__":
    run_tests()
