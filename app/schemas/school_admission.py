from pydantic import BaseModel

class SchoolAdmissionCreate(BaseModel):
    user_id: int
    school_name: str
    program: str
    country: str