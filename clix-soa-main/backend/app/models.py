"""
Database models for Order Allocation System
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, index=True)
    contact = Column(String(50))
    email = Column(String(100))
    address = Column(Text)
    status = Column(String(20), default="active")  # active, inactive
    credit_limit = Column(Float, default=0.0)
    credit_period_days = Column(Integer, default=30)  # Default credit period
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    payments = relationship("Payment", back_populates="customer")
    metrics = relationship("CustomerMetric", back_populates="customer", uselist=False)


class Inventory(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    product_code = Column(String(50), unique=True, nullable=False, index=True)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100))
    size = Column(String(10))  # Size: 45-110 or XS, S, M, L, XL, XXL
    available_quantity = Column(Float, default=0.0, nullable=False)
    reserved_quantity = Column(Float, default=0.0)
    unit = Column(String(20), default="pieces")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="inventory")
    allocations = relationship("Allocation", back_populates="inventory")


class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    total_quantity = Column(Float, default=0.0)
    status = Column(String(20), default="pending")  # pending, allocated, fulfilled, cancelled
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    allocations = relationship("Allocation", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    requested_quantity = Column(Float, nullable=False)
    allocated_quantity = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    inventory = relationship("Inventory", back_populates="order_items")


class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    payment_date = Column(DateTime(timezone=True), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(20), default="pending")  # pending, paid, overdue, partial
    payment_method = Column(String(50))
    reference_number = Column(String(100))
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="payments")


class CustomerMetric(Base):
    __tablename__ = "customer_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), unique=True, nullable=False)
    
    # Calculated metrics
    total_orders = Column(Integer, default=0)
    total_order_value = Column(Float, default=0.0)
    payment_frequency_score = Column(Float, default=0.0)  # 0-100
    credit_period_score = Column(Float, default=0.0)  # 0-100
    performance_score = Column(Float, default=0.0)  # 0-100
    overall_score = Column(Float, default=0.0)  # Weighted overall score
    
    # Detailed metrics
    on_time_payment_percentage = Column(Float, default=0.0)
    average_days_to_payment = Column(Float, default=0.0)
    overdue_count = Column(Integer, default=0)
    total_payments = Column(Integer, default=0)
    
    last_calculated = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    customer = relationship("Customer", back_populates="metrics")


class Allocation(Base):
    __tablename__ = "allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    inventory_id = Column(Integer, ForeignKey("inventory.id"), nullable=False)
    allocated_quantity = Column(Float, nullable=False)
    allocation_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    algorithm_version = Column(String(20), default="v1.0")
    notes = Column(Text)
    
    # Relationships
    order = relationship("Order", back_populates="allocations")
    inventory = relationship("Inventory", back_populates="allocations")

