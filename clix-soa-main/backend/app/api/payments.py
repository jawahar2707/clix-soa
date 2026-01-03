"""
API endpoints for payment management
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Payment, Customer
from app.schemas import PaymentCreate, PaymentUpdate, Payment as PaymentSchema
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/payments", tags=["payments"])


@router.post("/", response_model=PaymentSchema, status_code=201)
def create_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    """Create a new payment record"""
    # Verify customer exists
    customer = db.query(Customer).filter(Customer.id == payment.customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Determine payment status
    if payment.payment_date <= payment.due_date:
        status = "paid"
    elif payment.payment_date > payment.due_date:
        status = "overdue"
    else:
        status = "pending"
    
    payment_data = payment.model_dump()
    payment_data['status'] = status
    
    db_payment = Payment(**payment_data)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    # Recalculate customer metrics
    try:
        MetricsService.calculate_all_metrics(payment.customer_id, db)
    except:
        pass
    
    return db_payment


@router.get("/", response_model=List[PaymentSchema])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    customer_id: int = None,
    status: str = None,
    db: Session = Depends(get_db)
):
    """Get all payments with optional filters"""
    query = db.query(Payment)
    
    if customer_id:
        query = query.filter(Payment.customer_id == customer_id)
    if status:
        query = query.filter(Payment.status == status)
    
    payments = query.order_by(Payment.payment_date.desc()).offset(skip).limit(limit).all()
    return payments


@router.get("/{payment_id}", response_model=PaymentSchema)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get a specific payment"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.put("/{payment_id}", response_model=PaymentSchema)
def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate,
    db: Session = Depends(get_db)
):
    """Update a payment"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    update_data = payment_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    # Recalculate status if dates changed
    if 'payment_date' in update_data or 'due_date' in update_data:
        if payment.payment_date <= payment.due_date:
            payment.status = "paid"
        else:
            payment.status = "overdue"
    
    db.commit()
    db.refresh(payment)
    
    # Recalculate customer metrics
    try:
        MetricsService.calculate_all_metrics(payment.customer_id, db)
    except:
        pass
    
    return payment


@router.delete("/{payment_id}", status_code=204)
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    """Delete a payment"""
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    customer_id = payment.customer_id
    db.delete(payment)
    db.commit()
    
    # Recalculate customer metrics
    try:
        MetricsService.calculate_all_metrics(customer_id, db)
    except:
        pass
    
    return None

