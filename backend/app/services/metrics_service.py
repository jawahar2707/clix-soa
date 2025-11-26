"""
Service for calculating customer performance metrics
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import datetime, timedelta
from typing import List
from app.models import Customer, Payment, Order, CustomerMetric
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import settings


class MetricsService:
    """Service to calculate and update customer metrics"""
    
    @staticmethod
    def calculate_payment_frequency_score(customer_id: int, db: Session) -> float:
        """Calculate payment frequency score (0-100)"""
        payments = db.query(Payment).filter(
            Payment.customer_id == customer_id,
            Payment.status == "paid"
        ).all()
        
        if not payments:
            return 0.0
        
        total_payments = len(payments)
        on_time_payments = sum(1 for p in payments if p.payment_date <= p.due_date)
        
        on_time_percentage = (on_time_payments / total_payments) * 100 if total_payments > 0 else 0
        
        # Calculate average days to payment
        total_days = sum(
            (p.payment_date - p.due_date).days 
            for p in payments 
            if p.payment_date and p.due_date
        )
        avg_days = total_days / total_payments if total_payments > 0 else 0
        
        # Score based on on-time percentage and average days
        # On-time percentage contributes 70%, average days contributes 30%
        on_time_score = on_time_percentage * 0.7
        days_score = max(0, 100 - abs(avg_days) * 2) * 0.3  # Penalize late payments
        
        return min(100, max(0, on_time_score + days_score))
    
    @staticmethod
    def calculate_credit_period_score(customer_id: int, db: Session) -> float:
        """Calculate credit period adherence score (0-100)"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return 0.0
        
        payments = db.query(Payment).filter(
            Payment.customer_id == customer_id
        ).all()
        
        if not payments:
            return 50.0  # Neutral score if no payment history
        
        overdue_count = sum(1 for p in payments if p.status == "overdue")
        total_payments = len(payments)
        overdue_percentage = (overdue_count / total_payments) * 100 if total_payments > 0 else 0
        
        # Calculate average days over due date
        overdue_payments = [p for p in payments if p.payment_date and p.due_date and p.payment_date > p.due_date]
        if overdue_payments:
            avg_overdue_days = sum(
                (p.payment_date - p.due_date).days 
                for p in overdue_payments
            ) / len(overdue_payments)
        else:
            avg_overdue_days = 0
        
        # Score decreases with overdue percentage and days
        base_score = 100 - (overdue_percentage * 0.6)
        days_penalty = min(30, avg_overdue_days * 0.5)  # Max 30 point penalty
        
        return max(0, min(100, base_score - days_penalty))
    
    @staticmethod
    def calculate_performance_score(customer_id: int, db: Session) -> float:
        """Calculate overall customer performance score (0-100)"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            return 0.0
        
        # Get order statistics
        orders = db.query(Order).filter(Order.customer_id == customer_id).all()
        
        if not orders:
            return 0.0
        
        total_orders = len(orders)
        fulfilled_orders = sum(1 for o in orders if o.status == "fulfilled")
        fulfillment_rate = (fulfilled_orders / total_orders) * 100 if total_orders > 0 else 0
        
        # Calculate total order value
        total_value = sum(o.total_quantity for o in orders)
        
        # Score based on:
        # - Number of orders (30%)
        # - Fulfillment rate (40%)
        # - Order value consistency (30%)
        order_count_score = min(100, (total_orders / 10) * 100) * 0.3  # Normalize to 10 orders = 100
        fulfillment_score = fulfillment_rate * 0.4
        value_score = min(100, (total_value / 1000) * 100) * 0.3  # Normalize to 1000 units = 100
        
        return min(100, max(0, order_count_score + fulfillment_score + value_score))
    
    @staticmethod
    def calculate_all_metrics(customer_id: int, db: Session) -> CustomerMetric:
        """Calculate and update all metrics for a customer"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            raise ValueError(f"Customer {customer_id} not found")
        
        # Calculate individual scores
        payment_freq_score = MetricsService.calculate_payment_frequency_score(customer_id, db)
        credit_period_score = MetricsService.calculate_credit_period_score(customer_id, db)
        performance_score = MetricsService.calculate_performance_score(customer_id, db)
        
        # Get detailed statistics
        payments = db.query(Payment).filter(Payment.customer_id == customer_id).all()
        orders = db.query(Order).filter(Order.customer_id == customer_id).all()
        
        paid_payments = [p for p in payments if p.status == "paid"]
        on_time_payments = [p for p in paid_payments if p.payment_date <= p.due_date]
        overdue_payments = [p for p in payments if p.status == "overdue"]
        
        on_time_percentage = (len(on_time_payments) / len(paid_payments) * 100) if paid_payments else 0
        
        avg_days_to_payment = 0
        if paid_payments:
            total_days = sum(
                (p.payment_date - p.due_date).days 
                for p in paid_payments 
                if p.payment_date and p.due_date
            )
            avg_days_to_payment = total_days / len(paid_payments) if paid_payments else 0
        
        total_order_value = sum(o.total_quantity for o in orders)
        
        # Calculate weighted overall score
        overall_score = (
            performance_score * settings.performance_weight +
            payment_freq_score * settings.payment_frequency_weight +
            credit_period_score * settings.credit_period_weight
        )
        
        # Update or create metrics
        metrics = db.query(CustomerMetric).filter(CustomerMetric.customer_id == customer_id).first()
        
        if metrics:
            metrics.payment_frequency_score = payment_freq_score
            metrics.credit_period_score = credit_period_score
            metrics.performance_score = performance_score
            metrics.overall_score = overall_score
            metrics.total_orders = len(orders)
            metrics.total_order_value = total_order_value
            metrics.on_time_payment_percentage = on_time_percentage
            metrics.average_days_to_payment = avg_days_to_payment
            metrics.overdue_count = len(overdue_payments)
            metrics.total_payments = len(payments)
            metrics.last_calculated = datetime.utcnow()
        else:
            metrics = CustomerMetric(
                customer_id=customer_id,
                payment_frequency_score=payment_freq_score,
                credit_period_score=credit_period_score,
                performance_score=performance_score,
                overall_score=overall_score,
                total_orders=len(orders),
                total_order_value=total_order_value,
                on_time_payment_percentage=on_time_percentage,
                average_days_to_payment=avg_days_to_payment,
                overdue_count=len(overdue_payments),
                total_payments=len(payments),
                last_calculated=datetime.utcnow()
            )
            db.add(metrics)
        
        db.commit()
        db.refresh(metrics)
        
        return metrics
    
    @staticmethod
    def recalculate_all_metrics(db: Session) -> int:
        """Recalculate metrics for all customers"""
        customers = db.query(Customer).filter(Customer.status == "active").all()
        count = 0
        
        for customer in customers:
            try:
                MetricsService.calculate_all_metrics(customer.id, db)
                count += 1
            except Exception as e:
                print(f"Error calculating metrics for customer {customer.id}: {e}")
                continue
        
        return count

