from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends

from database import get_db
from schemas import OrderCreate, OrderResponse, OrderUpdate
from utils import reserve_products, return_products


router = APIRouter()


@router.get("/")
def root():
    return {"message": "Order Service API"}


@router.get("/orders/{order_id}", response_model=OrderResponse)
async def get_order(order_id: str, db=Depends(get_db)):
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order["id"] = str(order["_id"])
    return order


@router.get("/orders/", response_model=list[OrderResponse])
async def list_orders(db=Depends(get_db)):
    orders = await db.orders.find().to_list(100)
    for order in orders:
        order["id"] = str(order["_id"])
    return orders


@router.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, db=Depends(get_db)):
    items_to_reserve = [{"product_id": item.product_id, "quantity": item.quantity} for item in order.items]
    await reserve_products(items_to_reserve)

    order_data = order.model_dump()
    order_data["date"] = datetime.now()
    result = await db.orders.insert_one(order_data)
    order_data["id"] = str(result.inserted_id)
    return order_data


@router.patch("/orders/{order_id}", response_model=OrderResponse)
async def update_order(order_id: str, updates: OrderUpdate, db=Depends(get_db)):
    existing_order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if updates.items:
        items_to_return = [{"product_id": item["product_id"], "quantity": item["quantity"]}
                           for item in existing_order["items"]]
        await return_products(items_to_return)

        items_to_reserve = [{"product_id": item.product_id, "quantity": item.quantity} for item in updates.items]
        await reserve_products(items_to_reserve)

    update_data = updates.model_dump(exclude_unset=True)
    update_data["date"] = datetime.now()

    result = await db.orders.find_one_and_update(
        {"_id": ObjectId(order_id)},
        {"$set": update_data},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="Order not found")

    result["id"] = str(result["_id"])
    return result


@router.delete("/orders/{order_id}", response_model=dict)
async def delete_order(order_id: str, db=Depends(get_db)):
    order = await db.orders.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    items_to_return = [{"product_id": item["product_id"], "quantity": item["quantity"]} for item in order["items"]]
    await return_products(items_to_return)

    result = await db.orders.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=500, detail="Failed to delete order")

    return {"message": f"Order {order_id} deleted successfully"}
