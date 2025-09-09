from pydantic import BaseModel
from typing import Optional

class HospitalInfo(BaseModel):
    name: str
    address: str
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    phone_number: Optional[str] = None