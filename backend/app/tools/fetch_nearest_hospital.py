import os
from dotenv import load_dotenv
from agents import function_tool
import googlemaps
from backend.app.models.hospital_info import HospitalInfo
from backend.app.models.location_context import LocationContext

load_dotenv()

gmaps = googlemaps.Client(os.getenv("GOOGLE_MAPS_API_KEY"))

@function_tool
def fetch_nearest_hospital(location: LocationContext) -> list[HospitalInfo]:
    """
    Calls Google Maps API to get the best nearby hospital.
    Location should be 'latitude,longitude' format.
    """
    hospitals = gmaps.places_nearby(
        location=(location.latitude,location.longitude),
        radius=5000,
        type='hospital',
        
        ).get('results',[])
    
    hospitals_list = []
    for hospital in hospitals:
        hospitals_list.append(
            HospitalInfo(
                name= hospital.get('name'),
                address= hospital.get('vicinity'),
                rating=hospital.get('rating'),
                user_ratings_total=hospital.get('user_ratings_total'),
                phone_number=hospital.get('formatted_phone_number')
            )
        )
    
    return hospitals_list
    
if __name__ == "__main__":
    fetch_nearest_hospital(location=LocationContext('12.9345','77.6107'))

