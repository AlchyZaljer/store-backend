from pymongo import MongoClient


MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "order-db"
COLLECTION_NAME = "orders"

DEFAULT_STATUS = "pending"


def migrate():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    result = collection.update_many(
        {"status": {"$exists": False}},
        {"$set": {"status": DEFAULT_STATUS}}
    )

    print(f"Migration completed: updated {result.modified_count} documents")

    client.close()


if __name__ == "__main__":
    migrate()
