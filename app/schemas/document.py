from pydantic import BaseModel

class DocumentCreate(BaseModel):
    request_type: str
    request_id: int | None = None
    filename: str
    file_url: str