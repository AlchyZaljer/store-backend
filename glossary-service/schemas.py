from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProductBase(BaseModel):
    name: str = Field(
        ...,
        max_length=255,
        description="Name of the product (max 250 characters)")
    price: float = Field(
        ...,
        gt=0,
        description="Price of the product (must be greater than 0)")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Description of the product (optional, max 500 characters)")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        max_length=255,
        description="Updated name of the product (max 250 characters)")
    price: Optional[float] = Field(
        None,
        gt=0,
        description="Updated price of the product (must be greater than 0)")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated description of the product (max 500 characters)")


class ProductResponse(ProductBase):
    id: int = Field(
        ...,
        description="ID of the product")

    class Config:
        model_config = ConfigDict(from_attributes=True)
