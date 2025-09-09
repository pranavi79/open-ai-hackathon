from pydantic import BaseModel

class UserRequest(BaseModel):
    request: str
    longitude: str
    latitude: str