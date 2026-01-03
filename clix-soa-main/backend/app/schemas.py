"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


# Customer Schemas
class CustomerBase(BaseModel):
    name: str
    contact: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    credit_limit: float = 0.0
    credit_period_days: int = 30


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    status: Optional[str] = None
    credit_limit: Optional[float] = None
    credit_period_days: Optional[int] = None


class Customer(CustomerBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Inventory Schemas
class InventoryBase(BaseModel):
    product_code: str
    product_name: str
    category: Optional[str] = None
    size: Optional[str] = None  # Size: 45-110 or XS, S, M, L, XL, XXL
    available_quantity: float
    unit: str = "pieces"


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    product_name: Optional[str] = None
    category: Optional[str] = None
    size: Optional[str] = None
    available_quantity: Optional[float] = None
    reserved_quantity: Optional[float] = None
    unit: Optional[str] = None


class Inventory(InventoryBase):
    id: int
    reserved_quantity: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


# Order Schemas
class OrderItemCreate(BaseModel):
    inventory_id: int
    requested_quantity: float


class OrderItemResponse(BaseModel):
    id: int
    inventory_id: int
    requested_quantity: float
    allocated_quantity: float
    inventory: Inventory
    
    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_id: int
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: datetime
    total_quantity: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    customer: Customer
    order_items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True


# Payment Schemas
class PaymentBase(BaseModel):
    customer_id: int
    payment_date: datetime
    amount: float
    due_date: datetime
    payment_method: Optional[str] = None
    reference_number: Optional[str] = None
    notes: Optional[str] = None


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[str] = None
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    notes: Optional[str] = None


class Payment(PaymentBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Customer Metrics Schemas
class CustomerMetric(BaseModel):
    id: int
    customer_id: int
    total_orders: int
    total_order_value: float
    payment_frequency_score: float
    credit_period_score: float
    performance_score: float
    overall_score: float
    on_time_payment_percentage: float
    average_days_to_payment: float
    overdue_count: int
    total_payments: int
    last_calculated: datetime
    
    class Config:
        from_attributes = True


# Allocation Schemas
class AllocationResponse(BaseModel):
    id: int
    order_id: int
    inventory_id: int
    allocated_quantity: float
    allocation_date: datetime
    algorithm_version: str
    inventory: Inventory
    
    class Config:
        from_attributes = True


# Allocation Request
class AllocationRequest(BaseModel):
    order_ids: Optional[List[int]] = None  # If None, allocate all pending orders
    recalculate_metrics: bool = True


class AllocationResult(BaseModel):
    order_id: int
    customer_id: int
    customer_name: str
    total_requested: float
    total_allocated: float
    allocation_percentage: float
    items: List[dict]
    success: bool
    message: str

