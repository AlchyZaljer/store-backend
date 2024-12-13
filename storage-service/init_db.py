from database import engine, Base
from sqlalchemy import inspect
from models import StorageItem


inspector = inspect(engine)
if not inspector.has_table("storage"):
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
else:
    print("Tables already exist.")
