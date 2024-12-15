from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class StorageItem(Base):
    __tablename__ = "storage"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, nullable=False, unique=True, index=True)
    quantity = Column(Integer, default=0, nullable=False)
