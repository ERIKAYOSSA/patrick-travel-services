from pydantic import BaseModel
from datetime import datetime

class FlightBookingCreate(BaseModel):
    user_id: int
    departure: str
    arrival: str
    travel_date: datetime