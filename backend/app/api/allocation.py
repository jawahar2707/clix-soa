"""
API endpoints for order allocation
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Allocation, Order
from app.schemas import (
    AllocationRequest, AllocationResult, AllocationResponse
)
from app.services.allocation_service import AllocationService

router = APIRouter(prefix="/allocation", tags=["allocation"])


@router.post("/allocate", response_model=List[AllocationResult])
def allocate_orders(
    request: AllocationRequest,
    db: Session = Depends(get_db)
):
    """Allocate orders to customers based on performance metrics and stock availability"""
    try:
        results = AllocationService.allocate_orders(
            order_ids=request.order_ids,
            db=db,
            recalculate_metrics=request.recalculate_metrics
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Allocation failed: {str(e)}")


@router.get("/history", response_model=List[AllocationResponse])
def get_allocation_history(
    skip: int = 0,
    limit: int = 100,
    order_id: int = None,
    inventory_id: int = None,
    db: Session = Depends(get_db)
):
    """Get allocation history"""
    query = db.query(Allocation)
    
    if order_id:
        query = query.filter(Allocation.order_id == order_id)
    if inventory_id:
        query = query.filter(Allocation.inventory_id == inventory_id)
    
    allocations = query.order_by(Allocation.allocation_date.desc()).offset(skip).limit(limit).all()
    return allocations


@router.get("/order/{order_id}", response_model=List[AllocationResponse])
def get_order_allocations(order_id: int, db: Session = Depends(get_db)):
    """Get all allocations for a specific order"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    allocations = db.query(Allocation).filter(Allocation.order_id == order_id).all()
    return allocations

