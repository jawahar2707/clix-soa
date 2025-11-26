"""
Script to import inventory items from CSV file
"""
import csv
import sys
from pathlib import Path
from typing import List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal, init_db
from app.models import Inventory

# Size variations
NUMERIC_SIZES = [str(i) for i in range(45, 111, 5)]  # 45, 50, 55, ..., 110
ALPHABETIC_SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

def generate_product_codes(base_item: str, description: str) -> List[dict]:
    """Generate product codes with all size variations"""
    products = []
    
    # Generate numeric sizes
    for size in NUMERIC_SIZES:
        product_code = f"{base_item}-{size}"
        product_name = f"{description} - Size {size}"
        products.append({
            'product_code': product_code,
            'product_name': product_name,
            'size': size
        })
    
    # Generate alphabetic sizes
    for size in ALPHABETIC_SIZES:
        product_code = f"{base_item}-{size}"
        product_name = f"{description} - Size {size}"
        products.append({
            'product_code': product_code,
            'product_name': product_name,
            'size': size
        })
    
    return products

def import_inventory_from_csv(csv_file_path: str):
    """Import inventory items from CSV file"""
    db = SessionLocal()
    
    try:
        # Initialize database
        init_db()
        
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                try:
                    status = row.get('Status', '').strip().upper()
                    
                    # Skip inactive/discontinued items
                    if status in ['INACTIVE', 'DISCONTINUED']:
                        skipped_count += 1
                        continue
                    
                    item_code = row.get('Item', '').strip()
                    description = row.get('Description', '').strip()
                    item_class = row.get('Item Class', '').strip()
                    uom = row.get('UOM', 'PCS').strip()
                    commodity = row.get('Commodity', '').strip()
                    
                    if not item_code or not description:
                        skipped_count += 1
                        continue
                    
                    # Check if item already exists
                    existing = db.query(Inventory).filter(
                        Inventory.product_code == item_code
                    ).first()
                    
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # Determine category from Item Class
                    category = item_class.split('::')[0].strip() if '::' in item_class else item_class
                    
                    # Create inventory item
                    # For items that need sizes, we'll create base item first
                    # You can later add size variations if needed
                    inventory = Inventory(
                        product_code=item_code,
                        product_name=description,
                        category=category if category else None,
                        available_quantity=0.0,  # Start with 0, update later
                        reserved_quantity=0.0,
                        unit=uom if uom else 'PCS'
                    )
                    
                    db.add(inventory)
                    imported_count += 1
                    
                    # Commit every 100 records
                    if imported_count % 100 == 0:
                        db.commit()
                        print(f"Imported {imported_count} items...")
                
                except Exception as e:
                    error_count += 1
                    print(f"Error importing row {row.get('Item', 'unknown')}: {e}")
                    continue
        
        # Final commit
        db.commit()
        
        print(f"\nImport completed!")
        print(f"  - Imported: {imported_count} items")
        print(f"  - Skipped (inactive/duplicates/empty): {skipped_count}")
        print(f"  - Errors: {error_count}")
        print(f"\nNote: All items start with 0 quantity. Update quantities as needed.")
        
    except Exception as e:
        print(f"Error importing inventory: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def import_inventory_with_sizes(csv_file_path: str, create_size_variations: bool = False):
    """
    Import inventory with size variations for items that need them
    
    If create_size_variations is True, creates separate inventory items
    for each size (45-110 in 5 increments and XS-XXL)
    """
    db = SessionLocal()
    
    try:
        init_db()
        
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        # Items that typically need sizes (you can customize this list)
        items_needing_sizes = [
            'BANIAN', 'BRIEF', 'TRUNKS', 'PANTIES', 'SLIP', 
            'BRASSIERS', 'T-SHIRTS', 'TRACKS', 'LEGGING'
        ]
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            for row in csv_reader:
                try:
                    status = row.get('Status', '').strip().upper()
                    
                    if status in ['INACTIVE', 'DISCONTINUED']:
                        skipped_count += 1
                        continue
                    
                    item_code = row.get('Item', '').strip()
                    description = row.get('Description', '').strip()
                    item_class = row.get('Item Class', '').strip()
                    uom = row.get('UOM', 'PCS').strip()
                    
                    if not item_code or not description:
                        skipped_count += 1
                        continue
                    
                    category = item_class.split('::')[0].strip() if '::' in item_class else item_class
                    
                    # Check if this item type needs sizes
                    needs_sizes = any(item_type in item_class.upper() for item_type in items_needing_sizes)
                    
                    if create_size_variations and needs_sizes:
                        # Create size variations
                        products = generate_product_codes(item_code, description)
                        
                        for product in products:
                            # Check if already exists
                            existing = db.query(Inventory).filter(
                                Inventory.product_code == product['product_code']
                            ).first()
                            
                            if existing:
                                continue
                            
                            inventory = Inventory(
                                product_code=product['product_code'],
                                product_name=product['product_name'],
                                category=category if category else None,
                                available_quantity=0.0,
                                reserved_quantity=0.0,
                                unit=uom if uom else 'PCS'
                            )
                            
                            db.add(inventory)
                            imported_count += 1
                    else:
                        # Create single item without size variations
                        existing = db.query(Inventory).filter(
                            Inventory.product_code == item_code
                        ).first()
                        
                        if existing:
                            skipped_count += 1
                            continue
                        
                        inventory = Inventory(
                            product_code=item_code,
                            product_name=description,
                            category=category if category else None,
                            available_quantity=0.0,
                            reserved_quantity=0.0,
                            unit=uom if uom else 'PCS'
                        )
                        
                        db.add(inventory)
                        imported_count += 1
                    
                    # Commit every 100 records
                    if imported_count % 100 == 0:
                        db.commit()
                        print(f"Imported {imported_count} items...")
                
                except Exception as e:
                    error_count += 1
                    print(f"Error importing row {row.get('Item', 'unknown')}: {e}")
                    continue
        
        db.commit()
        
        print(f"\nImport completed!")
        print(f"  - Imported: {imported_count} items")
        print(f"  - Skipped: {skipped_count}")
        print(f"  - Errors: {error_count}")
        
    except Exception as e:
        print(f"Error importing inventory: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python import_inventory.py <csv_file_path> [--with-sizes]")
        print("Example: python import_inventory.py Items.csv")
        print("Example: python import_inventory.py Items.csv --with-sizes")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    create_sizes = '--with-sizes' in sys.argv
    
    if create_sizes:
        print("Importing inventory with size variations...")
        import_inventory_with_sizes(csv_path, create_size_variations=True)
    else:
        print("Importing inventory (base items only)...")
        import_inventory_from_csv(csv_path)

