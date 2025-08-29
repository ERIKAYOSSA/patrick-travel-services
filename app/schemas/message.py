from pydantic import BaseModel

class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    content: str | None = None
    filename: str | None = None
    file_url: str | None = None
    
    
    