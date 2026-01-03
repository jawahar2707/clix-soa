"""
Service for exporting allocation data to CSV and print formats
"""
import csv
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from sqlalchemy.orm import Session
from app.models import Allocation, Order, Customer, Inventory

class ExportService:
    """Service for exporting allocation data"""
    
    # Export directory - always relative to backend directory
    # Get backend directory (3 levels up from this file: app/services/export_service.py -> backend/)
    _BACKEND_DIR = Path(__file__).parent.parent.parent.absolute()
    EXPORT_DIR = _BACKEND_DIR / "exports"
    CSV_DIR = EXPORT_DIR / "csv"
    PRINT_DIR = EXPORT_DIR / "print"
    
    @staticmethod
    def ensure_directories():
        """Ensure export directories exist"""
        ExportService.CSV_DIR.mkdir(parents=True, exist_ok=True)
        ExportService.PRINT_DIR.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def export_allocation_to_csv(
        allocation_results: List[Dict],
        order_ids: List[int] = None,
        db: Session = None
    ) -> str:
        """
        Export allocation results to CSV file
        Returns the file path of the created CSV
        """
        ExportService.ensure_directories()
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if order_ids:
            filename = f"allocation_orders_{'_'.join(map(str, order_ids))}_{timestamp}.csv"
        else:
            filename = f"allocation_all_{timestamp}.csv"
        
        filepath = ExportService.CSV_DIR / filename
        
        # Get detailed allocation data from database
        if order_ids:
            allocations = db.query(Allocation).filter(
                Allocation.order_id.in_(order_ids)
            ).order_by(Allocation.allocation_date.desc()).all()
        else:
            # Get latest allocations (from this run)
            latest_date = db.query(Allocation).order_by(
                Allocation.allocation_date.desc()
            ).first()
            if latest_date:
                allocations = db.query(Allocation).filter(
                    Allocation.allocation_date >= latest_date.allocation_date
                ).all()
            else:
                allocations = []
        
        # Write CSV file
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Allocation ID',
                'Allocation Date',
                'Order ID',
                'Customer ID',
                'Customer Name',
                'Product Code',
                'Product Name',
                'Category',
                'Size',
                'Requested Quantity',
                'Allocated Quantity',
                'Allocation Percentage',
                'Unit',
                'Algorithm Version',
                'Order Date',
                'Order Status'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for allocation in allocations:
                # Get related data
                order = db.query(Order).filter(Order.id == allocation.order_id).first()
                customer = db.query(Customer).filter(Customer.id == order.customer_id).first() if order else None
                inventory = db.query(Inventory).filter(Inventory.id == allocation.inventory_id).first()
                
                # Get order item for requested quantity
                requested_qty = 0
                if order:
                    for item in order.order_items:
                        if item.inventory_id == allocation.inventory_id:
                            requested_qty = item.requested_quantity
                            break
                
                allocation_pct = (allocation.allocated_quantity / requested_qty * 100) if requested_qty > 0 else 0
                
                writer.writerow({
                    'Allocation ID': allocation.id,
                    'Allocation Date': allocation.allocation_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'Order ID': allocation.order_id,
                    'Customer ID': order.customer_id if order else '',
                    'Customer Name': customer.name if customer else '',
                    'Product Code': inventory.product_code if inventory else '',
                    'Product Name': inventory.product_name if inventory else '',
                    'Category': inventory.category if inventory else '',
                    'Size': inventory.size if inventory else '',
                    'Requested Quantity': requested_qty,
                    'Allocated Quantity': allocation.allocated_quantity,
                    'Allocation Percentage': f"{allocation_pct:.2f}%",
                    'Unit': inventory.unit if inventory else '',
                    'Algorithm Version': allocation.algorithm_version,
                    'Order Date': order.order_date.strftime('%Y-%m-%d') if order and order.order_date else '',
                    'Order Status': order.status if order else ''
                })
        
        return str(filepath)
    
    @staticmethod
    def export_allocation_summary_to_csv(
        allocation_results: List[Dict],
        db: Session = None
    ) -> str:
        """
        Export allocation summary (order-level) to CSV
        Returns the file path of the created CSV
        """
        ExportService.ensure_directories()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"allocation_summary_{timestamp}.csv"
        filepath = ExportService.CSV_DIR / filename
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Order ID',
                'Customer Name',
                'Order Date',
                'Total Requested',
                'Total Allocated',
                'Allocation Percentage',
                'Status',
                'Items Count',
                'Message'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in allocation_results:
                writer.writerow({
                    'Order ID': result.get('order_id', ''),
                    'Customer Name': result.get('customer_name', ''),
                    'Order Date': '',  # Can be added if needed
                    'Total Requested': result.get('total_requested', 0),
                    'Total Allocated': result.get('total_allocated', 0),
                    'Allocation Percentage': f"{result.get('allocation_percentage', 0):.2f}%",
                    'Status': 'Success' if result.get('success', False) else 'Failed',
                    'Items Count': len(result.get('items', [])),
                    'Message': result.get('message', '')
                })
        
        return str(filepath)
    
    @staticmethod
    def prepare_print_format_data(
        allocation_results: List[Dict],
        order_ids: List[int] = None,
        db: Session = None
    ) -> Dict:
        """
        Prepare data for print format (to be implemented later)
        Returns structured data for print formatting
        """
        # Get allocations from database
        if order_ids:
            allocations = db.query(Allocation).filter(
                Allocation.order_id.in_(order_ids)
            ).order_by(Allocation.allocation_date.desc()).all()
        else:
            latest_date = db.query(Allocation).order_by(
                Allocation.allocation_date.desc()
            ).first()
            if latest_date:
                allocations = db.query(Allocation).filter(
                    Allocation.allocation_date >= latest_date.allocation_date
                ).all()
            else:
                allocations = []
        
        # Group by order
        orders_data = {}
        for allocation in allocations:
            order_id = allocation.order_id
            if order_id not in orders_data:
                order = db.query(Order).filter(Order.id == order_id).first()
                customer = db.query(Customer).filter(Customer.id == order.customer_id).first() if order else None
                
                orders_data[order_id] = {
                    'order_id': order_id,
                    'order_date': order.order_date.strftime('%Y-%m-%d') if order and order.order_date else '',
                    'customer_name': customer.name if customer else '',
                    'customer_id': order.customer_id if order else None,
                    'items': []
                }
            
            inventory = db.query(Inventory).filter(Inventory.id == allocation.inventory_id).first()
            order = db.query(Order).filter(Order.id == order_id).first()
            
            requested_qty = 0
            if order:
                for item in order.order_items:
                    if item.inventory_id == allocation.inventory_id:
                        requested_qty = item.requested_quantity
                        break
            
            orders_data[order_id]['items'].append({
                'product_code': inventory.product_code if inventory else '',
                'product_name': inventory.product_name if inventory else '',
                'category': inventory.category if inventory else '',
                'size': inventory.size if inventory else '',
                'requested': requested_qty,
                'allocated': allocation.allocated_quantity,
                'unit': inventory.unit if inventory else ''
            })
        
        return {
            'allocation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'orders': list(orders_data.values()),
            'total_orders': len(orders_data),
            'summary': {
                'total_requested': sum(r.get('total_requested', 0) for r in allocation_results),
                'total_allocated': sum(r.get('total_allocated', 0) for r in allocation_results)
            }
        }

