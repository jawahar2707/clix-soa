"""
Script to create mock data for testing:
- 4 sales orders with various customers
- Payment history for customers
- Customer metrics will be calculated automatically
"""
import sys
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal, init_db
from app.models import Customer, Inventory, Order, OrderItem, Payment, CustomerMetric
from app.services.metrics_service import MetricsService

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_mock_data():
    """Create mock orders, payments, and metrics"""
    db = SessionLocal()
    
    try:
        print("Creating mock data...")
        
        # Get existing customers and inventory
        customers = db.query(Customer).limit(10).all()
        inventory_items = db.query(Inventory).limit(20).all()
        
        if not customers:
            print("ERROR: No customers found. Please import customers first.")
            return
        
        if not inventory_items:
            print("ERROR: No inventory items found. Please import inventory first.")
            return
        
        print(f"Found {len(customers)} customers and {len(inventory_items)} inventory items")
        
        # Select 4 different customers for orders
        selected_customers = customers[:4] if len(customers) >= 4 else customers
        
        # Create 4 orders with different scenarios
        orders_data = [
            {
                "customer": selected_customers[0],
                "items": [
                    {"inventory": inventory_items[0] if len(inventory_items) > 0 else None, "qty": 100},
                    {"inventory": inventory_items[1] if len(inventory_items) > 1 else None, "qty": 50},
                    {"inventory": inventory_items[2] if len(inventory_items) > 2 else None, "qty": 75},
                ],
                "notes": "Priority customer - Regular order",
                "order_date": datetime.now() - timedelta(days=5)
            },
            {
                "customer": selected_customers[1] if len(selected_customers) > 1 else selected_customers[0],
                "items": [
                    {"inventory": inventory_items[3] if len(inventory_items) > 3 else None, "qty": 200},
                    {"inventory": inventory_items[4] if len(inventory_items) > 4 else None, "qty": 150},
                ],
                "notes": "Bulk order - High volume",
                "order_date": datetime.now() - timedelta(days=3)
            },
            {
                "customer": selected_customers[2] if len(selected_customers) > 2 else selected_customers[0],
                "items": [
                    {"inventory": inventory_items[5] if len(inventory_items) > 5 else None, "qty": 80},
                    {"inventory": inventory_items[6] if len(inventory_items) > 6 else None, "qty": 60},
                    {"inventory": inventory_items[7] if len(inventory_items) > 7 else None, "qty": 40},
                ],
                "notes": "Mixed order - Various sizes",
                "order_date": datetime.now() - timedelta(days=2)
            },
            {
                "customer": selected_customers[3] if len(selected_customers) > 3 else selected_customers[0],
                "items": [
                    {"inventory": inventory_items[8] if len(inventory_items) > 8 else None, "qty": 300},
                ],
                "notes": "Large single item order",
                "order_date": datetime.now() - timedelta(days=1)
            },
        ]
        
        created_orders = []
        
        # Create orders
        for order_data in orders_data:
            customer = order_data["customer"]
            items = [item for item in order_data["items"] if item["inventory"] is not None]
            
            if not items:
                print(f"Warning: Skipping order for {customer.name} - no valid inventory items")
                continue
            
            # Create order
            order = Order(
                customer_id=customer.id,
                order_date=order_data["order_date"],
                status="pending",
                notes=order_data["notes"]
            )
            db.add(order)
            db.flush()
            
            # Create order items
            total_quantity = 0
            for item_data in items:
                inventory = item_data["inventory"]
                quantity = item_data["qty"]
                
                order_item = OrderItem(
                    order_id=order.id,
                    inventory_id=inventory.id,
                    requested_quantity=quantity
                )
                db.add(order_item)
                total_quantity += quantity
            
            order.total_quantity = total_quantity
            created_orders.append(order)
            print(f"[OK] Created Order #{order.id} for {customer.name} with {len(items)} items (Total: {total_quantity})")
        
        db.commit()
        print(f"\n[OK] Created {len(created_orders)} orders")
        
        # Update inventory quantities for allocation testing
        print("\nUpdating inventory quantities for allocation testing...")
        # Get all inventory items used in orders and update quantities
        inventory_usage = {}
        for order in created_orders:
            for item in order.order_items:
                inv_id = item.inventory_id
                if inv_id not in inventory_usage:
                    inventory_usage[inv_id] = {
                        'requested': 0,
                        'inventory': db.query(Inventory).filter(Inventory.id == inv_id).first()
                    }
                inventory_usage[inv_id]['requested'] += item.requested_quantity
        
        # Update inventory with different scenarios
        for idx, (inv_id, inv_data) in enumerate(inventory_usage.items()):
            inventory = inv_data['inventory']
            if not inventory:
                continue
            
            requested = inv_data['requested']
            scenario = idx % 4
            
            if scenario == 0:
                new_quantity = int(requested * 1.5)  # Sufficient
            elif scenario == 1:
                new_quantity = int(requested * 0.7)  # Limited
            elif scenario == 2:
                new_quantity = int(requested * 0.4)  # Very Limited
            else:
                new_quantity = max(10, int(requested * 0.25))  # Scarce
            
            new_quantity = max(10, new_quantity)
            inventory.available_quantity = new_quantity
            inventory.reserved_quantity = 0
        
        db.commit()
        print(f"[OK] Updated {len(inventory_usage)} inventory items for allocation testing")
        
        # Create payment history for customers to establish metrics
        print("\nCreating payment history...")
        
        payment_scenarios = [
            # Customer 1: Excellent payer (on-time, multiple payments)
            {
                "customer": selected_customers[0],
                "payments": [
                    {"amount": 50000, "days_ago": 60, "paid_days_ago": 30, "status": "paid"},
                    {"amount": 75000, "days_ago": 30, "paid_days_ago": 0, "status": "paid"},
                    {"amount": 100000, "days_ago": 0, "paid_days_ago": None, "status": "pending"},
                ]
            },
            # Customer 2: Good payer (mostly on-time)
            {
                "customer": selected_customers[1] if len(selected_customers) > 1 else selected_customers[0],
                "payments": [
                    {"amount": 40000, "days_ago": 45, "paid_days_ago": 15, "status": "paid"},
                    {"amount": 60000, "days_ago": 15, "paid_days_ago": 2, "status": "paid"},
                ]
            },
            # Customer 3: Average payer (some delays)
            {
                "customer": selected_customers[2] if len(selected_customers) > 2 else selected_customers[0],
                "payments": [
                    {"amount": 30000, "days_ago": 50, "paid_days_ago": 20, "status": "paid"},
                    {"amount": 45000, "days_ago": 20, "paid_days_ago": 5, "status": "paid"},
                    {"amount": 35000, "days_ago": 5, "paid_days_ago": None, "status": "overdue"},
                ]
            },
            # Customer 4: New customer (limited history)
            {
                "customer": selected_customers[3] if len(selected_customers) > 3 else selected_customers[0],
                "payments": [
                    {"amount": 25000, "days_ago": 10, "paid_days_ago": None, "status": "pending"},
                ]
            },
        ]
        
        created_payments = []
        
        for scenario in payment_scenarios:
            customer = scenario["customer"]
            credit_period = customer.credit_period_days or 30
            
            for payment_data in scenario["payments"]:
                due_date = datetime.now() - timedelta(days=payment_data["days_ago"])
                
                if payment_data["paid_days_ago"] is not None:
                    payment_date = datetime.now() - timedelta(days=payment_data["paid_days_ago"])
                else:
                    payment_date = due_date  # Not paid yet
                
                payment = Payment(
                    customer_id=customer.id,
                    payment_date=payment_date,
                    amount=payment_data["amount"],
                    due_date=due_date,
                    status=payment_data["status"],
                    payment_method="Bank Transfer" if payment_data["status"] == "paid" else None,
                    reference_number=f"REF-{customer.id}-{payment_data['days_ago']}" if payment_data["status"] == "paid" else None,
                    notes=f"Payment for {customer.name}"
                )
                db.add(payment)
                created_payments.append(payment)
            
            print(f"[OK] Created {len(scenario['payments'])} payments for {customer.name}")
        
        db.commit()
        print(f"\n[OK] Created {len(created_payments)} payments")
        
        # Calculate metrics for all customers
        print("\nCalculating customer metrics...")
        all_customers = db.query(Customer).all()
        metrics_calculated = 0
        
        # Only calculate metrics for customers with orders or payments
        for customer in all_customers:
            try:
                # Check if customer has any orders or payments
                orders_count = db.query(Order).filter(Order.customer_id == customer.id).count()
                payments_count = db.query(Payment).filter(Payment.customer_id == customer.id).count()
                
                if orders_count > 0 or payments_count > 0:
                    MetricsService.calculate_all_metrics(customer.id, db)
                    metrics_calculated += 1
            except Exception as e:
                print(f"Warning: Could not calculate metrics for customer {customer.id}: {e}")
        
        db.commit()
        print(f"[OK] Calculated metrics for {metrics_calculated} customers")
        
        # Display summary
        print("\n" + "="*60)
        print("MOCK DATA CREATION SUMMARY")
        print("="*60)
        print(f"Orders Created: {len(created_orders)}")
        print(f"Payments Created: {len(created_payments)}")
        print(f"Metrics Calculated: {metrics_calculated}")
        print("\nOrder Details:")
        for order in created_orders:
            customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
            items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
            print(f"  Order #{order.id}: {customer.name} - {len(items)} items, {order.total_quantity} total qty")
        print("\n" + "="*60)
        print("Mock data creation completed successfully!")
        print("You can now test the allocation system with these orders.")
        print("="*60)
        
    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    create_mock_data()

