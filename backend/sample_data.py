"""
Script to populate sample data for testing
"""
from app.database import init_db, SessionLocal
from app.models import Customer, Inventory, Order, OrderItem, Payment
from datetime import datetime, timedelta
from app.services.metrics_service import MetricsService

def create_sample_data():
    """Create sample customers, inventory, orders, and payments"""
    db = SessionLocal()
    
    try:
        # Initialize database
        init_db()
        
        print("Creating sample data...")
        
        # Create Customers
        customers_data = [
            {
                "name": "ABC Textiles Ltd",
                "contact": "9876543210",
                "email": "abc@textiles.com",
                "address": "123 Textile Street, Mumbai",
                "credit_limit": 500000,
                "credit_period_days": 30
            },
            {
                "name": "XYZ Garments",
                "contact": "9876543211",
                "email": "xyz@garments.com",
                "address": "456 Garment Road, Delhi",
                "credit_limit": 300000,
                "credit_period_days": 45
            },
            {
                "name": "Premium Innerwear Co",
                "contact": "9876543212",
                "email": "premium@innerwear.com",
                "address": "789 Fashion Avenue, Bangalore",
                "credit_limit": 750000,
                "credit_period_days": 30
            },
            {
                "name": "Budget Wear Solutions",
                "contact": "9876543213",
                "email": "budget@wear.com",
                "address": "321 Economy Lane, Chennai",
                "credit_limit": 200000,
                "credit_period_days": 60
            }
        ]
        
        customers = []
        for data in customers_data:
            customer = Customer(**data)
            db.add(customer)
            customers.append(customer)
        
        db.commit()
        print(f"Created {len(customers)} customers")
        
        # Create Inventory
        inventory_data = [
            {
                "product_code": "INW-M-001",
                "product_name": "Men's Cotton Briefs - White",
                "category": "Men",
                "available_quantity": 5000,
                "unit": "pieces"
            },
            {
                "product_code": "INW-M-002",
                "product_name": "Men's Cotton Briefs - Black",
                "category": "Men",
                "available_quantity": 4500,
                "unit": "pieces"
            },
            {
                "product_code": "INW-W-001",
                "product_name": "Women's Cotton Panties - White",
                "category": "Women",
                "available_quantity": 6000,
                "unit": "pieces"
            },
            {
                "product_code": "INW-W-002",
                "product_name": "Women's Cotton Panties - Black",
                "category": "Women",
                "available_quantity": 5500,
                "unit": "pieces"
            },
            {
                "product_code": "INW-K-001",
                "product_name": "Kids Cotton Underwear - White",
                "category": "Kids",
                "available_quantity": 3000,
                "unit": "pieces"
            }
        ]
        
        inventory_items = []
        for data in inventory_data:
            item = Inventory(**data)
            db.add(item)
            inventory_items.append(item)
        
        db.commit()
        print(f"Created {len(inventory_items)} inventory items")
        
        # Create Orders
        orders_data = [
            {
                "customer": customers[0],
                "items": [
                    {"inventory": inventory_items[0], "quantity": 1000},
                    {"inventory": inventory_items[1], "quantity": 800}
                ]
            },
            {
                "customer": customers[1],
                "items": [
                    {"inventory": inventory_items[2], "quantity": 1200},
                    {"inventory": inventory_items[3], "quantity": 1000}
                ]
            },
            {
                "customer": customers[2],
                "items": [
                    {"inventory": inventory_items[0], "quantity": 1500},
                    {"inventory": inventory_items[1], "quantity": 1200},
                    {"inventory": inventory_items[2], "quantity": 2000}
                ]
            },
            {
                "customer": customers[3],
                "items": [
                    {"inventory": inventory_items[4], "quantity": 500}
                ]
            }
        ]
        
        orders = []
        for order_data in orders_data:
            order = Order(
                customer_id=order_data["customer"].id,
                order_date=datetime.utcnow() - timedelta(days=5),
                status="pending"
            )
            db.add(order)
            db.flush()
            
            total_qty = 0
            for item_data in order_data["items"]:
                order_item = OrderItem(
                    order_id=order.id,
                    inventory_id=item_data["inventory"].id,
                    requested_quantity=item_data["quantity"]
                )
                db.add(order_item)
                total_qty += item_data["quantity"]
            
            order.total_quantity = total_qty
            orders.append(order)
        
        db.commit()
        print(f"Created {len(orders)} orders")
        
        # Create Payments (with varying payment behaviors)
        payments_data = [
            # Customer 0 - Good payer (on time)
            {
                "customer": customers[0],
                "amount": 50000,
                "due_date": datetime.utcnow() - timedelta(days=30),
                "payment_date": datetime.utcnow() - timedelta(days=28),
                "status": "paid"
            },
            {
                "customer": customers[0],
                "amount": 75000,
                "due_date": datetime.utcnow() - timedelta(days=15),
                "payment_date": datetime.utcnow() - timedelta(days=14),
                "status": "paid"
            },
            # Customer 1 - Late payer
            {
                "customer": customers[1],
                "amount": 40000,
                "due_date": datetime.utcnow() - timedelta(days=45),
                "payment_date": datetime.utcnow() - timedelta(days=50),
                "status": "paid"
            },
            {
                "customer": customers[1],
                "amount": 60000,
                "due_date": datetime.utcnow() - timedelta(days=20),
                "payment_date": datetime.utcnow() - timedelta(days=25),
                "status": "paid"
            },
            # Customer 2 - Excellent payer
            {
                "customer": customers[2],
                "amount": 100000,
                "due_date": datetime.utcnow() - timedelta(days=30),
                "payment_date": datetime.utcnow() - timedelta(days=28),
                "status": "paid"
            },
            {
                "customer": customers[2],
                "amount": 120000,
                "due_date": datetime.utcnow() - timedelta(days=10),
                "payment_date": datetime.utcnow() - timedelta(days=8),
                "status": "paid"
            },
            # Customer 3 - Overdue payment
            {
                "customer": customers[3],
                "amount": 25000,
                "due_date": datetime.utcnow() - timedelta(days=60),
                "payment_date": datetime.utcnow() - timedelta(days=70),
                "status": "overdue"
            }
        ]
        
        payments = []
        for payment_data in payments_data:
            payment = Payment(**payment_data)
            db.add(payment)
            payments.append(payment)
        
        db.commit()
        print(f"Created {len(payments)} payment records")
        
        # Calculate metrics for all customers
        print("\nCalculating customer metrics...")
        for customer in customers:
            try:
                MetricsService.calculate_all_metrics(customer.id, db)
                print(f"  - Metrics calculated for {customer.name}")
            except Exception as e:
                print(f"  - Error calculating metrics for {customer.name}: {e}")
        
        print("\nSample data created successfully!")
        print(f"\nSummary:")
        print(f"  - Customers: {len(customers)}")
        print(f"  - Inventory Items: {len(inventory_items)}")
        print(f"  - Orders: {len(orders)}")
        print(f"  - Payments: {len(payments)}")
        print(f"\nYou can now start the server and test the allocation system!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()

