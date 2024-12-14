from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import StorageItem
from schemas import StorageItemCreate, StorageItemUpdate, StorageItemResponse


router = APIRouter()


@router.get("/", response_model=dict)
def root():
    return {"message": "Storage Service API"}


@router.get("/items/{item_id}", response_model=StorageItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(StorageItem).filter(StorageItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/items/", response_model=list[StorageItemResponse])
def list_items(db: Session = Depends(get_db)):
    items = db.query(StorageItem).all()
    return items


@router.patch("/items/{item_id}", response_model=StorageItemResponse)
def update_item(item_id: int, updates: StorageItemUpdate, db: Session = Depends(get_db)):
    item = db.query(StorageItem).filter(StorageItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)
    return item


@router.post("/items/add/", response_model=StorageItemResponse)
def add_item(item: StorageItemCreate, db: Session = Depends(get_db)):
    db_item = db.query(StorageItem).filter(StorageItem.name == item.name).first()
    if db_item:
        db_item.quantity += item.quantity
        db_item.price = item.price
    else:
        db_item = StorageItem(
            name=item.name,
            quantity=item.quantity,
            price=item.price,
            description=item.description,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_item)
    return db_item


@router.post("/items/remove/", response_model=Union[StorageItemResponse, dict])
def remove_item(item_id: int, quantity: int, db: Session = Depends(get_db)):
    db_item = db.query(StorageItem).filter(StorageItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.quantity < quantity:
        raise HTTPException(
            status_code=400, detail="Not enough items in storage to remove"
        )

    db_item.quantity -= quantity

    if db_item.quantity == 0:
        db.delete(db_item)
        db.commit()
        return {"message": f"Product {item_id} deleted"}

    db.commit()
    return db_item
