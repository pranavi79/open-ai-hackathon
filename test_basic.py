"""
Basic tests for the Emergency Accident Response System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.models.user_request import UserRequest
from backend.app.models.accident_report import AccidentReport
from backend.app.models.hospital_info import HospitalInfo
from backend.app.models.location_context import LocationContext


def test_user_request_model():
    """Test UserRequest model validation"""
    request = UserRequest(
        request="Test accident description",
        longitude="77.6107",
        latitude="12.9345"
    )
    assert request.request == "Test accident description"
    assert request.longitude == "77.6107"
    assert request.latitude == "12.9345"
    print("✅ UserRequest model test passed")

def test_accident_report_model():
    """Test AccidentReport model validation"""
    report = AccidentReport(
        accident_type="minor",
        first_aid_tips="Apply pressure to wound",
        location="Test location",
        details="Test accident details"
    )
    assert report.accident_type == "minor"
    assert report.first_aid_tips == "Apply pressure to wound"
    print("✅ AccidentReport model test passed")

def test_hospital_info_model():
    """Test HospitalInfo model validation"""
    hospital = HospitalInfo(
        name="Test Hospital",
        address="123 Test St",
        rating=4.5,
        user_ratings_total=100,
        phone_number="+1234567890"
    )
    assert hospital.name == "Test Hospital"
    assert hospital.rating == 4.5
    assert hospital.user_ratings_total == 100
    print("✅ HospitalInfo model test passed")

def test_hospital_info_optional_fields():
    """Test HospitalInfo with optional fields"""
    hospital = HospitalInfo(
        name="Test Hospital",
        address="123 Test St"
    )
    assert hospital.name == "Test Hospital"
    assert hospital.rating is None
    assert hospital.phone_number is None
    print("✅ HospitalInfo optional fields test passed")

def test_location_context_model():
    """Test LocationContext model validation"""
    location = LocationContext(
        latitude="12.9345",
        longitude="77.6107"
    )
    assert location.latitude == "12.9345"
    assert location.longitude == "77.6107"
    print("✅ LocationContext model test passed")


if __name__ == "__main__":
    print("🧪 Running basic model validation tests...")
    
    try:
        test_user_request_model()
        test_accident_report_model()
        test_hospital_info_model()
        test_hospital_info_optional_fields()
        test_location_context_model()
        
        print("\n🎉 All basic tests passed!")
        print("📝 Models are properly structured and validated")
        print("💡 To run full test suite: pip install pytest && pytest")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)