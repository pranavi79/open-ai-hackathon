from pydantic import BaseModel

class AccidentReport(BaseModel):
    accident_type: str 
    first_aid_tips: str
    location: str
    details: str