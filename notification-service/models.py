from datetime import datetime

from pydantic import BaseModel


class Notification(BaseModel):
    id: str
    message: str
    timestamp: datetime
