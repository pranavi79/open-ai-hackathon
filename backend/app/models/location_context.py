from pydantic import BaseModel

class LocationContext(BaseModel):
    latitude: str
    longitude: str