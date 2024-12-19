import os

from motor.motor_asyncio import AsyncIOMotorClient


MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "order-db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]


def get_db():
    try:
        yield db
    finally:
        pass
