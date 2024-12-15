from pydantic import BaseModel, Field


class StorageItemBase(BaseModel):
    product_id: int = Field(
        ...,
        description="ID of the product")
    quantity: int = Field(
        ...,
        gt=0,
        description="Quantity of the product (must be greater than 0)")


class StorageItemCreate(StorageItemBase):
    pass


class StorageItemRemove(StorageItemBase):
    pass


class StorageItemUpdate(StorageItemBase):
    quantity: int = Field(
        ...,
        ge=0,
        description="Updated quantity of the product (must be greater than or equal 0)")


class StorageItemResponse(StorageItemBase):
    pass
