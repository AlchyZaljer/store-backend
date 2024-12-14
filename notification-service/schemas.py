from datetime import datetime

from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    message: str = Field(
        ...,
        max_length=500,
        description="Notification message (max 500 characters)")


class NotificationCreate(NotificationBase):
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp of the notification")


class NotificationResponse(NotificationBase):
    id: str = Field(
        ...,
        description="ID of the notification")
    timestamp: datetime = Field(
        ...,
        description="Timestamp of the notification")
