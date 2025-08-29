from pydantic import BaseModel

class PartnerCreate(BaseModel):
    name: str
    type: str
    contact_email: str | None = None
    contact_phone: str | None = None
    address: str | None = None