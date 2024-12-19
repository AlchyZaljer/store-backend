import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:1234@storage-db:5432/storage-db")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
