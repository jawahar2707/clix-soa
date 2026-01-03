"""
API endpoints for inventory management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Inventory
from app.schemas import (
    InventoryCreate, InventoryUpdate, Inventory as InventorySchema
)

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/", response_model=InventorySchema, status_code=201)
def create_inventory_item(item: InventoryCreate, db: Session = Depends(get_db)):
    """Create a new inventory item"""
    # Check if product code already exists
    existing = db.query(Inventory).filter(
        Inventory.product_code == item.product_code
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail=f"Inventory item with product code {item.product_code} already exists"
        )
    
    db_item = Inventory(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.get("/", response_model=List[InventorySchema])
def get_inventory_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all inventory items"""
    items = db.query(Inventory).offset(skip).limit(limit).all()
    return items


@router.get("/{inventory_id}", response_model=InventorySchema)
def get_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """Get a specific inventory item"""
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.get("/code/{product_code}", response_model=InventorySchema)
def get_inventory_by_code(product_code: str, db: Session = Depends(get_db)):
    """Get inventory item by product code"""
    item = db.query(Inventory).filter(Inventory.product_code == product_code).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return item


@router.put("/{inventory_id}", response_model=InventorySchema)
def update_inventory_item(
    inventory_id: int,
    item_update: InventoryUpdate,
    db: Session = Depends(get_db)
):
    """Update an inventory item"""
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    update_data = item_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{inventory_id}", status_code=204)
def delete_inventory_item(inventory_id: int, db: Session = Depends(get_db)):
    """Delete an inventory item"""
    item = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    
    db.delete(item)
    db.commit()
    return None

