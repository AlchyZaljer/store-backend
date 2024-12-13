from database import engine, Base
from sqlalchemy import inspect
from models import Product


inspector = inspect(engine)
if not inspector.has_table("products"):
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
else:
    print("Tables already exist.")
