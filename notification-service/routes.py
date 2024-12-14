from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query

from database import get_db
from schemas import NotificationResponse


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Notification Service API"}


@router.get("/notifications/last", response_model=NotificationResponse)
async def get_last_notification(db=Depends(get_db)):
    notification = await db.notifications.find_one(sort=[("timestamp", -1)])
    if not notification:
        raise HTTPException(status_code=404, detail="No notifications found")
    notification["id"] = str(notification["_id"])
    return notification


@router.get("/notifications/recent", response_model=list[NotificationResponse])
async def get_recent_notifications(db=Depends(get_db)):
    notifications = await db.notifications.find(sort=[("timestamp", -1)]).to_list(5)
    for notification in notifications:
        notification["id"] = str(notification["_id"])
    return notifications


@router.get("/notifications/after", response_model=list[NotificationResponse])
async def get_notifications_after(
    timestamp: str = Query(
        ...,
        description="Date or datetime in the format 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'"),
    db=Depends(get_db)
):
    try:
        if " " in timestamp:
            parsed_time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        else:
            parsed_time = datetime.strptime(timestamp, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use 'YYYY-MM-DD' or 'YYYY-MM-DD HH:MM:SS'")

    notifications = await db.notifications.find({"timestamp": {"$gt": parsed_time}}).to_list(100)

    for notification in notifications:
        notification["id"] = str(notification["_id"])
    return notifications
