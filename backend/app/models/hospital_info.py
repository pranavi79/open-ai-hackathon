from pydantic import BaseModel

class HospitalInfo(BaseModel):
    name: str
    address: str
    rating: str
    user_ratings_total: str
    phone_number: str