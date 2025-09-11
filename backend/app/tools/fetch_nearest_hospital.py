from dataclasses import dataclass
import os
import googlemaps
from dotenv import load_dotenv
from agents import function_tool
import googlemaps


load_dotenv()

gmaps = googlemaps.Client(os.getenv("GOOGLE_MAPS_API_KEY"))

@function_tool
def fetch_nearest_hospital(latitude: str = '12.9345', longitude: str = '77.6107') -> list[str]:

    """
    Calls Google Maps API to get the best nearby hospital.
    Location should be 'latitude,longitude' format.
    """
    hospitals = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=150,
        type='hospital',
        ).get('results',[])
    
    hospitals_list = []
    for hospital in hospitals:
        hospitals_list.append(
            f'''
                name={hospital.get('name', 'Unknown')},
                address={hospital.get('vicinity', 'Unknown')},
                rating={str(hospital.get('rating', '0'))},
                user_ratings_total={str(hospital.get('user_ratings_total', '0'))},
                phone_number={hospital.get('formatted_phone_number', 'N/A')}
                '''     
        )
    
    return hospitals_list
    
if __name__ == "__main__":
    print(fetch_nearest_hospital('12.9345','77.6107'))

