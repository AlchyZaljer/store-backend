from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query

from database import get_db
from schemas import NotificationResponse


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Notification Service API"}


@router.get("/notifications/recent", response_model=list[NotificationResponse])
async def get_recent_notifications(
        count: int = Query(
            default=1,
            gt=0,
            description="Number of most recent notifications (must be greater than 0)"
        ),
        db=Depends(get_db)
):
    notifications = await db.notifications.find(sort=[("timestamp", -1)]).limit(count).to_list(None)
    if not notifications:
        raise HTTPException(status_code=404, detail="No notifications found")

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

    notifications = await db.notifications.find({"timestamp": {"$gt": parsed_time}}).to_list(None)

    for notification in notifications:
        notification["id"] = str(notification["_id"])
    return notifications
