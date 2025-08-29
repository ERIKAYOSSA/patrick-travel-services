from pydantic import BaseModel

class AssistanceVisaCreate(BaseModel):
    user_id: int
    country: str
    visa_type: str