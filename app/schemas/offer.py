from pydantic import BaseModel

class OfferCreate(BaseModel):
    title: str
    type: str  # "bourse", "logement", "admission"
    description: str | None = None
    conditions: str | None = None
    partner_id: int | None = None