"""
Service for allocating orders to customers based on multiple criteria
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from typing import List, Dict
from app.models import (
    Order, OrderItem, Inventory, Customer, CustomerMetric, Allocation
)
from app.services.metrics_service import MetricsService
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from config import settings


class AllocationService:
    """Service to allocate orders based on customer performance and stock availability"""
    
    @staticmethod
    def allocate_orders(order_ids: List[int] = None, db: Session = None, recalculate_metrics: bool = True) -> List[Dict]:
        """
        Allocate orders to customers based on:
        - Customer performance (30%)
        - Payment frequency (25%)
        - Credit period adherence (25%)
        - Stock availability (20%)
        """
        if recalculate_metrics:
            # Recalculate all customer metrics
            MetricsService.recalculate_all_metrics(db)
        
        # Get orders to allocate
        if order_ids:
            orders = db.query(Order).filter(
                Order.id.in_(order_ids),
                Order.status == "pending"
            ).all()
        else:
            orders = db.query(Order).filter(Order.status == "pending").all()
        
        if not orders:
            return []
        
        results = []
        
        # Group orders by customer
        customer_orders = {}
        for order in orders:
            if order.customer_id not in customer_orders:
                customer_orders[order.customer_id] = []
            customer_orders[order.customer_id].append(order)
        
        # Get all inventory items needed
        all_inventory_needed = {}
        for order in orders:
            for item in order.order_items:
                inv_id = item.inventory_id
                if inv_id not in all_inventory_needed:
                    all_inventory_needed[inv_id] = {
                        'total_requested': 0,
                        'inventory': db.query(Inventory).filter(Inventory.id == inv_id).first()
                    }
                all_inventory_needed[inv_id]['total_requested'] += item.requested_quantity
        
        # Allocate each inventory item
        for inv_id, inv_data in all_inventory_needed.items():
            inventory = inv_data['inventory']
            if not inventory:
                continue
            
            total_requested = inv_data['total_requested']
            available = inventory.available_quantity - inventory.reserved_quantity
            
            if available <= 0:
                # No stock available
                continue
            
            # Get customer priorities for this inventory item
            customer_priorities = AllocationService._calculate_customer_priorities(
                customer_orders.keys(), db
            )
            
            # Allocate stock to customers based on priority
            customer_allocations = AllocationService._allocate_inventory_to_customers(
                inv_id, available, customer_priorities, customer_orders, db
            )
            
            # Create allocation records for each order-item combination
            total_allocated = 0
            for customer_id, allocated_qty in [(a['customer_id'], a['quantity']) for a in customer_allocations]:
                # Distribute allocation across orders for this customer
                customer_orders_list = customer_orders.get(customer_id, [])
                total_customer_demand = sum(
                    item.requested_quantity 
                    for order in customer_orders_list 
                    for item in order.order_items 
                    if item.inventory_id == inv_id
                )
                
                if total_customer_demand > 0:
                    for order in customer_orders_list:
                        for item in order.order_items:
                            if item.inventory_id == inv_id:
                                # Calculate proportional allocation for this item
                                item_share = item.requested_quantity / total_customer_demand
                                item_allocated = min(
                                    allocated_qty * item_share,
                                    item.requested_quantity,
                                    available - total_allocated
                                )
                                
                                if item_allocated > 0:
                                    # Create allocation record
                                    allocation = Allocation(
                                        order_id=order.id,
                                        inventory_id=inv_id,
                                        allocated_quantity=item_allocated,
                                        allocation_date=datetime.utcnow(),
                                        algorithm_version="v1.0"
                                    )
                                    db.add(allocation)
                                    item.allocated_quantity = item_allocated
                                    total_allocated += item_allocated
            
            # Update inventory
            inventory.reserved_quantity += total_allocated
            inventory.available_quantity -= total_allocated
        
        # Process each order
        for order in orders:
            result = AllocationService._process_order_allocation(order, db)
            results.append(result)
        
        db.commit()
        return results
    
    @staticmethod
    def _calculate_customer_priorities(customer_ids: List[int], db: Session) -> Dict[int, float]:
        """Calculate priority scores for customers"""
        priorities = {}
        
        for customer_id in customer_ids:
            metrics = db.query(CustomerMetric).filter(
                CustomerMetric.customer_id == customer_id
            ).first()
            
            if metrics:
                # Use overall score as priority
                priorities[customer_id] = metrics.overall_score
            else:
                # Calculate metrics if not available
                try:
                    metrics = MetricsService.calculate_all_metrics(customer_id, db)
                    priorities[customer_id] = metrics.overall_score
                except:
                    priorities[customer_id] = 0.0
        
        # Normalize priorities (0-100 scale)
        if priorities:
            max_priority = max(priorities.values())
            if max_priority > 0:
                priorities = {k: (v / max_priority) * 100 for k, v in priorities.items()}
        
        return priorities
    
    @staticmethod
    def _allocate_inventory_to_customers(
        inventory_id: int,
        available_quantity: float,
        customer_priorities: Dict[int, float],
        customer_orders: Dict[int, List[Order]],
        db: Session
    ) -> List[Dict]:
        """Allocate inventory to customers based on priority and demand"""
        allocations = []
        
        # Calculate total demand per customer for this inventory
        customer_demands = {}
        for customer_id, orders in customer_orders.items():
            total_demand = 0
            for order in orders:
                for item in order.order_items:
                    if item.inventory_id == inventory_id:
                        total_demand += item.requested_quantity
            if total_demand > 0:
                customer_demands[customer_id] = total_demand
        
        if not customer_demands:
            return allocations
        
        # Sort customers by priority (descending)
        sorted_customers = sorted(
            customer_demands.keys(),
            key=lambda cid: customer_priorities.get(cid, 0),
            reverse=True
        )
        
        remaining_stock = available_quantity
        total_priority = sum(customer_priorities.get(cid, 0) for cid in customer_demands.keys())
        
        # First pass: Allocate based on priority-weighted distribution
        for customer_id in sorted_customers:
            if remaining_stock <= 0:
                break
            
            priority = customer_priorities.get(customer_id, 0)
            if priority <= 0:
                continue
            
            demand = customer_demands[customer_id]
            
            # Calculate allocation based on priority and demand
            if total_priority > 0:
                priority_share = priority / total_priority
                allocated = min(
                    demand,
                    available_quantity * priority_share,
                    remaining_stock
                )
            else:
                # Equal distribution if no priority
                allocated = min(demand, remaining_stock / len(customer_demands))
            
            # Apply min/max constraints
            min_allocation = available_quantity * settings.min_allocation_percentage
            max_allocation = available_quantity * settings.max_allocation_percentage
            
            allocated = max(min_allocation, min(allocated, max_allocation, demand, remaining_stock))
            
            if allocated > 0:
                allocations.append({
                    'customer_id': customer_id,
                    'quantity': allocated
                })
                remaining_stock -= allocated
        
        # Second pass: Distribute remaining stock proportionally
        if remaining_stock > 0 and allocations:
            # Distribute remaining stock based on priority
            total_allocated_priority = sum(
                customer_priorities.get(a['customer_id'], 0) 
                for a in allocations
            )
            
            if total_allocated_priority > 0:
                for allocation in allocations:
                    customer_id = allocation['customer_id']
                    priority = customer_priorities.get(customer_id, 0)
                    share = priority / total_allocated_priority
                    additional = min(
                        remaining_stock * share,
                        customer_demands.get(customer_id, 0) - allocation['quantity']
                    )
                    if additional > 0:
                        allocation['quantity'] += additional
                        remaining_stock -= additional
                        if remaining_stock <= 0:
                            break
        
        return allocations
    
    @staticmethod
    def _process_order_allocation(order: Order, db: Session) -> Dict:
        """Process allocation for a single order"""
        customer = db.query(Customer).filter(Customer.id == order.customer_id).first()
        customer_name = customer.name if customer else "Unknown"
        
        total_requested = sum(item.requested_quantity for item in order.order_items)
        total_allocated = 0
        allocation_items = []
        
        success = True
        message = "Allocation completed"
        
        # Check each order item
        for item in order.order_items:
            inventory = db.query(Inventory).filter(Inventory.id == item.inventory_id).first()
            if not inventory:
                continue
            
            # Find allocation for this item
            allocation = db.query(Allocation).filter(
                Allocation.order_id == order.id,
                Allocation.inventory_id == item.inventory_id
            ).first()
            
            if allocation:
                item.allocated_quantity = allocation.allocated_quantity
                total_allocated += allocation.allocated_quantity
                allocation_items.append({
                    'inventory_id': item.inventory_id,
                    'product_code': inventory.product_code,
                    'product_name': inventory.product_name,
                    'requested': item.requested_quantity,
                    'allocated': allocation.allocated_quantity
                })
            else:
                # No allocation found - might be insufficient stock
                allocation_items.append({
                    'inventory_id': item.inventory_id,
                    'product_code': inventory.product_code if inventory else 'N/A',
                    'product_name': inventory.product_name if inventory else 'N/A',
                    'requested': item.requested_quantity,
                    'allocated': 0
                })
                if item.requested_quantity > 0:
                    success = False
                    message = "Partial allocation - insufficient stock for some items"
        
        # Update order status
        if total_allocated > 0:
            if total_allocated >= total_requested * 0.95:  # 95% threshold for "fulfilled"
                order.status = "allocated"
            else:
                order.status = "partially_allocated"
        else:
            order.status = "pending"
            success = False
            message = "No allocation possible - insufficient stock"
        
        order.total_quantity = total_allocated
        db.commit()
        
        allocation_percentage = (total_allocated / total_requested * 100) if total_requested > 0 else 0
        
        return {
            'order_id': order.id,
            'customer_id': order.customer_id,
            'customer_name': customer_name,
            'total_requested': total_requested,
            'total_allocated': total_allocated,
            'allocation_percentage': round(allocation_percentage, 2),
            'items': allocation_items,
            'success': success,
            'message': message
        }
    
    @staticmethod
    def create_allocations(
        order_id: int,
        inventory_id: int,
        quantity: float,
        db: Session
    ) -> Allocation:
        """Create an allocation record"""
        allocation = Allocation(
            order_id=order_id,
            inventory_id=inventory_id,
            allocated_quantity=quantity,
            allocation_date=datetime.utcnow(),
            algorithm_version="v1.0"
        )
        db.add(allocation)
        db.commit()
        db.refresh(allocation)
        return allocation

