#!/usr/bin/env python3
"""
Test script to verify cost protection is working
This script will test API limits and demo mode functionality
"""
import requests
import json
import time

def test_api_endpoint(url, payload=None, method="GET"):
    """Test an API endpoint and return response"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=payload)
        
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    base_url = "http://localhost:8000"
    
    print("[TEST] COST PROTECTION TEST SUITE")
    print("=" * 50)
    
    # Test 1: Check system status
    print("\n1. Testing system status...")
    status = test_api_endpoint(f"{base_url}/")
    print(f"   Demo mode: {status.get('demo_mode', 'unknown')}")
    print(f"   Services: {', '.join(status.get('services', []))}")
    
    # Test 2: Check API usage endpoint
    print("\n2. Testing usage monitoring...")
    usage = test_api_endpoint(f"{base_url}/api-usage")
    print(f"   Current usage tracked: {bool(usage.get('current_usage'))}")
    print(f"   Limits configured: {bool(usage.get('limits'))}")
    
    # Test 3: Test emergency response (should use fallbacks in demo mode)
    print("\n3. Testing emergency response...")
    emergency_payload = {
        "request": "I cut my finger and it's bleeding",
        "latitude": "40.7128",
        "longitude": "-74.0060"
    }
    response = test_api_endpoint(f"{base_url}/ask", emergency_payload, "POST")
    print(f"   Response received: {bool(response.get('accident_type'))}")
    print(f"   First aid provided: {bool(response.get('first_aid_tips'))}")
    
    # Test 4: Test hospital search
    print("\n4. Testing hospital search...")
    hospital_payload = {
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    hospitals = test_api_endpoint(f"{base_url}/hospitals", hospital_payload, "POST")
    print(f"   Hospital search works: {bool(hospitals.get('hospitals'))}")
    
    # Test 5: Test calling capability
    print("\n5. Testing calling capability...")
    calling = test_api_endpoint(f"{base_url}/calling-capability")
    print(f"   Calling available: {calling.get('calling_available', False)}")
    
    # Test 6: Enable/disable demo mode
    print("\n6. Testing demo mode controls...")
    demo_enable = test_api_endpoint(f"{base_url}/enable-demo-mode", method="POST")
    print(f"   Demo mode enable: {demo_enable.get('success', False)}")
    
    # Final usage check
    print("\n[STATS] Final usage check...")
    final_usage = test_api_endpoint(f"{base_url}/api-usage")
    today_usage = final_usage.get('current_usage', {}).get('today', {})
    print(f"   OpenAI requests today: {today_usage.get('openai_requests', 0)}")
    print(f"   Google Maps requests today: {today_usage.get('google_maps_requests', 0)}")
    print(f"   Twilio calls today: {today_usage.get('twilio_calls', 0)}")
    
    print("\n[OK] Cost protection test completed!")
    print("[INFO] If demo mode is enabled, no actual API charges should occur")

if __name__ == "__main__":
    print("⏳ Starting in 3 seconds... (make sure server is running)")
    time.sleep(3)
    main()
