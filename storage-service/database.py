from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base


DATABASE_URL = "postgresql://postgres:1234@localhost:5432/store-db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
