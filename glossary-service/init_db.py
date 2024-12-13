from database import engine, Base
from models import Product


if not engine.dialect.has_table(engine, "products"):
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")
else:
    print("Tables already exist.")
