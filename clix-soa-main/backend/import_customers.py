"""
Script to import customers from CSV file
"""
import csv
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal, init_db
from app.models import Customer
from app.services.metrics_service import MetricsService

def import_customers_from_csv(csv_file_path: str):
    """Import customers from CSV file"""
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
                    # Extract customer data
                    code = row.get('Code', '').strip()
                    name = row.get('Name', '').strip()
                    short_name = row.get('Short_Name', '').strip()
                    
                    if not name or not code:
                        skipped_count += 1
                        continue
                    
                    # Check if customer already exists (by code or name)
                    existing = db.query(Customer).filter(
                        (Customer.name == name) | 
                        (Customer.contact == code)
                    ).first()
                    
                    if existing:
                        skipped_count += 1
                        continue
                    
                    # Combine address fields
                    address_parts = [
                        row.get('Address_1', '').strip(),
                        row.get('Address_2', '').strip(),
                        row.get('Address_3', '').strip()
                    ]
                    address = ', '.join([part for part in address_parts if part])
                    
                    # Get contact information
                    telephone = row.get('Telephone', '').strip()
                    mobile_1 = row.get('Mobile_1', '').strip()
                    mobile_2 = row.get('Mobile_2', '').strip()
                    contact = mobile_1 or mobile_2 or telephone or code
                    
                    email_1 = row.get('Email_1', '').strip()
                    email_2 = row.get('Email_2', '').strip()
                    email = email_1 or email_2
                    
                    # Create customer
                    customer = Customer(
                        name=name,
                        contact=contact,
                        email=email if email else None,
                        address=address if address else None,
                        status='active',
                        credit_limit=0.0,  # Default, can be updated later
                        credit_period_days=30  # Default, can be updated later
                    )
                    
                    db.add(customer)
                    imported_count += 1
                    
                    # Commit every 100 records
                    if imported_count % 100 == 0:
                        db.commit()
                        print(f"Imported {imported_count} customers...")
                
                except Exception as e:
                    error_count += 1
                    print(f"Error importing row {row.get('Code', 'unknown')}: {e}")
                    continue
        
        # Final commit
        db.commit()
        
        print(f"\nImport completed!")
        print(f"  - Imported: {imported_count} customers")
        print(f"  - Skipped (duplicates/empty): {skipped_count}")
        print(f"  - Errors: {error_count}")
        
        # Initialize metrics for imported customers
        print("\nInitializing customer metrics...")
        customers = db.query(Customer).all()
        for customer in customers:
            try:
                MetricsService.calculate_all_metrics(customer.id, db)
            except:
                pass
        
        print("Customer metrics initialized!")
        
    except Exception as e:
        print(f"Error importing customers: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python import_customers.py <csv_file_path>")
        print("Example: python import_customers.py Customers.csv")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    import_customers_from_csv(csv_path)

