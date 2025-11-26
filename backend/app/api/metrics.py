"""
API endpoints for customer metrics
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import CustomerMetric, Customer
from app.schemas import CustomerMetric as CustomerMetricSchema
from app.services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/customer/{customer_id}", response_model=CustomerMetricSchema)
def get_customer_metrics(customer_id: int, db: Session = Depends(get_db)):
    """Get metrics for a specific customer"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    metrics = db.query(CustomerMetric).filter(
        CustomerMetric.customer_id == customer_id
    ).first()
    
    if not metrics:
        # Calculate metrics if not available
        metrics = MetricsService.calculate_all_metrics(customer_id, db)
    
    return metrics


@router.post("/customer/{customer_id}/recalculate", response_model=CustomerMetricSchema)
def recalculate_customer_metrics(customer_id: int, db: Session = Depends(get_db)):
    """Recalculate metrics for a specific customer"""
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    metrics = MetricsService.calculate_all_metrics(customer_id, db)
    return metrics


@router.post("/recalculate-all")
def recalculate_all_metrics(db: Session = Depends(get_db)):
    """Recalculate metrics for all customers"""
    count = MetricsService.recalculate_all_metrics(db)
    return {"message": f"Recalculated metrics for {count} customers", "count": count}

