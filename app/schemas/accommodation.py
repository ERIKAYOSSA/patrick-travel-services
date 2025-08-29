from pydantic import BaseModel
from datetime import datetime

class AccommodationCreate(BaseModel):
    user_id: int
    location: str
    check_in: datetime
    check_out: datetime