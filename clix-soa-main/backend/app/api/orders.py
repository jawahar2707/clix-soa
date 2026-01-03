"""
API endpoints for order management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Order, OrderItem, Inventory, Customer
from app.schemas import (
    OrderCreate, OrderUpdate, Order as OrderSchema, OrderItemResponse
)

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=OrderSchema, status_code=201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    """Create a new order"""
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Create order
    order_data = order.model_dump(exclude={'items'})
    db_order = Order(**order_data)
    db.add(db_order)
    db.flush()  # Get order ID
    
    # Create order items
    total_quantity = 0
    for item_data in order.items:
        # Verify inventory exists
        inventory = db.query(Inventory).filter(Inventory.id == item_data.inventory_id).first()
        if not inventory:
            raise HTTPException(
                status_code=404,
                detail=f"Inventory item {item_data.inventory_id} not found"
            )
        
        order_item = OrderItem(
            order_id=db_order.id,
            inventory_id=item_data.inventory_id,
            requested_quantity=item_data.requested_quantity
        )
        db.add(order_item)
        total_quantity += item_data.requested_quantity
    
    db_order.total_quantity = total_quantity
    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[OrderSchema])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    status: str = None,
    customer_id: int = None,
    db: Session = Depends(get_db)
):
    """Get all orders with optional filters"""
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    if customer_id:
        query = query.filter(Order.customer_id == customer_id)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=OrderSchema)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """Get a specific order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=OrderSchema)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Update an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    update_data = order_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(order, field, value)
    
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """Delete an order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    db.delete(order)
    db.commit()
    return None

