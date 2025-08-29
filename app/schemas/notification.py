from pydantic import BaseModel

class NotificationCreate(BaseModel):
    user_id: int
    type: str
    content: str