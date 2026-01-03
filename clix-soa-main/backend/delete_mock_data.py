"""
Script to delete mock data created for testing
This will delete:
- Orders created by create_mock_data.py (Orders #5-8 or latest 4 orders)
- Payments created for those customers
- Customer metrics (will be recalculated automatically)
"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Order, Payment, OrderItem, CustomerMetric

def delete_mock_data():
    """Delete mock orders and related data"""
    db = SessionLocal()
    
    try:
        print("Deleting mock data...")
        
        # Find the mock orders (assuming they are the latest 4 orders)
        # Or you can specify order IDs if you know them
        all_orders = db.query(Order).order_by(Order.id.desc()).limit(10).all()
        
        # Get order IDs to delete (you can modify this to target specific orders)
        # For now, we'll delete the last 4 orders created
        orders_to_delete = all_orders[:4] if len(all_orders) >= 4 else all_orders
        
        if not orders_to_delete:
            print("No orders found to delete.")
            return
        
        order_ids = [order.id for order in orders_to_delete]
        customer_ids = list(set([order.customer_id for order in orders_to_delete]))
        
        print(f"Found {len(orders_to_delete)} orders to delete:")
        for order in orders_to_delete:
            customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
            print(f"  Order #{order.id}: {customer.name if customer else 'Unknown'}")
        
        # Delete order items first (due to foreign key constraints)
        deleted_items = db.query(OrderItem).filter(OrderItem.order_id.in_(order_ids)).delete(synchronize_session=False)
        print(f"Deleted {deleted_items} order items")
        
        # Delete orders
        deleted_orders = db.query(Order).filter(Order.id.in_(order_ids)).delete(synchronize_session=False)
        print(f"Deleted {deleted_orders} orders")
        
        # Delete payments for those customers (optional - you may want to keep payment history)
        # Uncomment the following lines if you want to delete payments too:
        # deleted_payments = db.query(Payment).filter(Payment.customer_id.in_(customer_ids)).delete(synchronize_session=False)
        # print(f"Deleted {deleted_payments} payments")
        
        # Delete customer metrics for those customers (they will be recalculated when needed)
        deleted_metrics = db.query(CustomerMetric).filter(CustomerMetric.customer_id.in_(customer_ids)).delete(synchronize_session=False)
        print(f"Deleted {deleted_metrics} customer metrics")
        
        db.commit()
        
        print("\n" + "="*60)
        print("MOCK DATA DELETION SUMMARY")
        print("="*60)
        print(f"Orders Deleted: {deleted_orders}")
        print(f"Order Items Deleted: {deleted_items}")
        print(f"Metrics Deleted: {deleted_metrics}")
        print("="*60)
        print("Mock data deletion completed successfully!")
        print("="*60)
        
    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    from app.models import Customer
    delete_mock_data()

