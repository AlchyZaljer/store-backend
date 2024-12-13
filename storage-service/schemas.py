from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class StorageItemBase(BaseModel):
    name: str = Field(
        ...,
        max_length=255,
        description="Name of the storage item (max 250 characters)")
    quantity: int = Field(
        ...,
        ge=0,
        description="Quantity of the storage item (must be greater than 0)")
    price: float = Field(
        ...,
        gt=0,
        description="Price of the storage item (must be greater than 0)")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Description of the storage item (max 500 characters)")


class StorageItemCreate(StorageItemBase):
    pass


class StorageItemUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=255,
        description="Updated name of the storage item (max 250 characters)")
    quantity: Optional[int] = Field(
        None,
        ge=0,
        description="Updated quantity of the storage item (must be greater than 0)")
    price: Optional[float] = Field(
        None,
        gt=0,
        description="Updated price of the storage item (must be greater than 0)")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated description of the storage item (max 500 characters)")


class StorageItemResponse(StorageItemBase):
    id: int = Field(
        ...,
        description="ID of the storage item")

    class Config:
        model_config = ConfigDict(from_attributes=True)
