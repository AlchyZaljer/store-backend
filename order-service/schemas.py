from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class OrderItemBase(BaseModel):
    product_id: int = Field(
        ...,
        description="ID of the product")
    quantity: int = Field(
        ...,
        gt=0,
        description="Quantity of the product (must be positive)")


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemUpdate(BaseModel):
    product_id: Optional[int] = Field(
        None,
        description="ID of the product")
    quantity: Optional[int] = Field(
        None,
        gt=0,
        description="Updated quantity of the product (must be greater than 0)"
    )


class OrderBase(BaseModel):
    items: list[OrderItemCreate] = Field(
        ...,
        min_length=1,
        description="List of items in the order (must contain at least one item)")
    discount: float = Field(
        0.0,
        ge=0,
        le=1,
        description="Discount on the order (0.0 to 1.0)")


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    items: list[OrderItemCreate] = Field(
        None,
        min_length=1,
        description="Updated list of items in the order (must contain at least one item)")
    discount: Optional[float] = Field(
        None,
        ge=0,
        le=1,
        description="Updated discount on the order (0.0 to 1.0)")


class OrderResponse(OrderBase):
    id: str = Field(
        ...,
        description="Order ID")

    model_config = ConfigDict(from_attributes=True)
