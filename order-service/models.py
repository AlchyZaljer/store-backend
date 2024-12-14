from datetime import datetime

from pydantic import BaseModel


class OrderItem(BaseModel):
    product_id: str
    quantity: int


class Order(BaseModel):
    id: str
    date: datetime
    items: list[OrderItem]
    discount: float = 0.0
