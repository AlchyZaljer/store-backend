from sqlalchemy import Column, Integer, String, Float
from database import Base


class StorageItem(Base):
    __tablename__ = "storage"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
