from typing import List, Union

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import StorageItem
from schemas import StorageItemCreate, StorageItemUpdate, StorageItemRemove, StorageItemResponse
import utils

router = APIRouter()


@router.get("/", response_model=dict)
def root():
    return {"message": "Storage Service API"}


@router.get("/items/{product_id}", response_model=StorageItemResponse)
def get_item(product_id: int, db: Session = Depends(get_db)):
    item = db.query(StorageItem).filter(StorageItem.product_id == product_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items/", response_model=list[StorageItemResponse])
def list_items(db: Session = Depends(get_db)):
    items = db.query(StorageItem).all()
    return items


@router.post("/items/add/", response_model=StorageItemResponse)
def add_item(item: StorageItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(StorageItem).filter(StorageItem.product_id == item.product_id).first()
    if db_item:
        db_item.quantity += item.quantity
    else:
        if not utils.is_product_exist(item.product_id):
            raise HTTPException(
                status_code=404,
                detail=f"Product not found in Glossary"
            )

        db_item = StorageItem(
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.post("/items/remove/", response_model=Union[StorageItemResponse, dict[str, str]])
def remove_item(item: StorageItemRemove, db: Session = Depends(get_db)):
    db_item = db.query(StorageItem).filter(StorageItem.product_id == item.product_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.quantity < item.quantity:
        raise HTTPException(
            status_code=400, detail="Not enough items in storage to remove"
        )

    db_item.quantity -= item.quantity

    if db_item.quantity == 0:
        db.delete(db_item)
        db.commit()
        return {"message": f"Product {item.product_id} deleted"}

    db.commit()
    return db_item


@router.patch("/items/", response_model=list[StorageItemResponse])
def update_items(updates: List[StorageItemUpdate], db: Session = Depends(get_db)):
    update_ids = [item.product_id for item in updates]

    db_items = db.query(StorageItem).filter(StorageItem.product_id.in_(update_ids)).all()
    db_items_dict = {db_item.product_id: db_item for db_item in db_items}

    not_found_products = [upd_id for upd_id in update_ids if upd_id not in db_items_dict.keys()]
    if not_found_products:
        raise HTTPException(status_code=404, detail={"not_found_products": not_found_products})

    for upd in updates:
        for key, value in upd.model_dump(exclude_unset=True).items():
            setattr(db_items_dict[upd.product_id], key, value)

    db.commit()
    for item in db_items:
        db.refresh(item)
    return db_items


@router.post("/reserve/", response_model=dict[str, str])
def reserve_items(items: List[StorageItemRemove], db: Session = Depends(get_db)):
    reserve_products_dict = {item.product_id: item for item in items}

    db_items = db.query(StorageItem).filter(StorageItem.product_id.in_(reserve_products_dict.keys())).all()
    db_items_dict = {db_item.product_id: db_item for db_item in db_items}

    insufficient_items = []

    for product_id, reserve_item in reserve_products_dict.items():
        db_item = db_items_dict.get(product_id)

        if not db_item or db_item.quantity < reserve_item.quantity:
            insufficient_items.append({"product_id": product_id})
            continue

        db_item.quantity -= reserve_item.quantity
        if db_item.quantity == 0:
            db.delete(db_item)

    if insufficient_items:
        raise HTTPException(status_code=400, detail={"insufficient_items": insufficient_items})

    db.commit()
    return {"message": "Items reserved successfully"}
