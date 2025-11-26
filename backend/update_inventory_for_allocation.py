"""
Script to update inventory quantities based on mock orders
This creates realistic allocation scenarios:
- Some items with sufficient stock (full allocation possible)
- Some items with limited stock (partial allocation)
- Some items with very low stock (scarcity testing)
"""
import sys
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Order, OrderItem, Inventory

def update_inventory_for_allocation():
    """Update inventory quantities to test allocation scenarios"""
    db = SessionLocal()
    
    try:
        print("Updating inventory for allocation testing...")
        
        # Get all pending orders
        orders = db.query(Order).filter(Order.status == "pending").all()
        
        if not orders:
            print("No pending orders found. Please create mock orders first.")
            return
        
        print(f"Found {len(orders)} pending orders")
        
        # Collect all inventory items used in orders
        inventory_usage = {}
        for order in orders:
            for item in order.order_items:
                inv_id = item.inventory_id
                if inv_id not in inventory_usage:
                    inventory_usage[inv_id] = {
                        'requested': 0,
                        'inventory': db.query(Inventory).filter(Inventory.id == inv_id).first()
                    }
                inventory_usage[inv_id]['requested'] += item.requested_quantity
        
        print(f"\nFound {len(inventory_usage)} unique inventory items in orders")
        
        # Update inventory with different scenarios
        updated_count = 0
        
        for idx, (inv_id, inv_data) in enumerate(inventory_usage.items()):
            inventory = inv_data['inventory']
            if not inventory:
                continue
            
            requested = inv_data['requested']
            
            # Create different scenarios based on index
            # This ensures we have variety: sufficient, limited, and scarce stock
            scenario = idx % 4
            
            if scenario == 0:
                # Scenario 1: Sufficient stock - can fulfill all orders (150% of requested)
                new_quantity = int(requested * 1.5)
                scenario_name = "Sufficient Stock"
            elif scenario == 1:
                # Scenario 2: Limited stock - can fulfill ~70% of total demand
                new_quantity = int(requested * 0.7)
                scenario_name = "Limited Stock"
            elif scenario == 2:
                # Scenario 3: Very limited stock - can fulfill ~40% of total demand
                new_quantity = int(requested * 0.4)
                scenario_name = "Very Limited Stock"
            else:
                # Scenario 4: Scarcity - can fulfill ~25% of total demand
                new_quantity = max(10, int(requested * 0.25))  # At least 10 units
                scenario_name = "Scarce Stock"
            
            # Ensure minimum of 10 units for testing
            new_quantity = max(10, new_quantity)
            
            old_quantity = inventory.available_quantity
            inventory.available_quantity = new_quantity
            inventory.reserved_quantity = 0  # Reset reserved quantity
            
            updated_count += 1
            print(f"  Item {inventory.product_code}: {old_quantity} -> {new_quantity} ({scenario_name}, Requested: {requested})")
        
        db.commit()
        
        print(f"\n{'='*60}")
        print("INVENTORY UPDATE SUMMARY")
        print("="*60)
        print(f"Items Updated: {updated_count}")
        print("\nAllocation Scenarios Created:")
        print("  - Sufficient Stock: Items with 150% of demand (full allocation)")
        print("  - Limited Stock: Items with 70% of demand (partial allocation)")
        print("  - Very Limited Stock: Items with 40% of demand (high competition)")
        print("  - Scarce Stock: Items with 25% of demand (maximum competition)")
        print("="*60)
        print("\nInventory is now ready for allocation testing!")
        print("Run the allocation algorithm to see how it distributes limited stock.")
        print("="*60)
        
    except Exception as e:
        db.rollback()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    update_inventory_for_allocation()

