# Data Import Guide

## Importing Customers

To import customers from CSV:

```bash
python import_customers.py "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"
```

Or with relative path:
```bash
python import_customers.py ../Downloads/Customers.csv
```

### Customer CSV Format Expected:
- Code: Customer code
- Name: Full customer name
- Short_Name: Short name
- Address_1, Address_2, Address_3: Address components
- Telephone: Phone number
- Contact_Person: Contact person name
- Mobile_1, Mobile_2: Mobile numbers
- Email_1, Email_2: Email addresses

## Importing Inventory Items

### Option 1: Import Base Items Only (Recommended)

This imports each item code once without size variations:

```bash
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv"
```

### Option 2: Import with Size Variations

This creates separate inventory entries for each size (45-110 in increments of 5, and XS-XXL):

```bash
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv" --with-sizes
```

**Note:** Using `--with-sizes` will create many more inventory items. For example, if you have 100 base items that need sizes, it will create:
- 100 items × 14 numeric sizes (45-110) = 1,400 items
- 100 items × 6 alphabetic sizes (XS-XXL) = 600 items
- Total: ~2,000 inventory items

### Inventory CSV Format Expected:
- Status: ACTIVE, INACTIVE, or DISCONTINUED
- Item Class: Category classification
- Item: Product code
- Description: Product description
- UOM: Unit of measure (defaults to PCS)
- Commodity: Commodity type

## Size Handling

The system supports two approaches:

### Approach 1: Single Item with Size Field
- Each item has one inventory entry
- Size is stored as a field in the inventory record
- Use this when sizes are managed at the order/item level

### Approach 2: Separate Items per Size
- Each size gets its own inventory entry
- Product codes like: `ITEM-45`, `ITEM-50`, `ITEM-XS`, `ITEM-S`, etc.
- Use this when you need to track inventory separately for each size

## After Import

1. **Update Quantities**: All imported items start with 0 quantity. Update them via:
   - API: `PUT /inventory/{id}`
   - Or create a separate script to update from your ERP

2. **Verify Data**: Check imported data:
   ```bash
   # Check customers
   GET http://localhost:8000/customers/
   
   # Check inventory
   GET http://localhost:8000/inventory/
   ```

3. **Set Credit Limits**: Update customer credit limits and periods as needed:
   ```bash
   PUT http://localhost:8000/customers/{id}
   {
     "credit_limit": 100000,
     "credit_period_days": 30
   }
   ```

## Troubleshooting

### Import Errors
- Check CSV file encoding (should be UTF-8)
- Verify CSV headers match expected format
- Check for special characters in data

### Duplicate Errors
- The script skips duplicates automatically
- Check skipped count in import output

### Database Errors
- Make sure database is initialized: `python init_db.py`
- Check database file permissions

## Example Import Workflow

1. Initialize database:
   ```bash
   python init_db.py
   ```

2. Import customers:
   ```bash
   python import_customers.py "path/to/Customers.csv"
   ```

3. Import inventory (base items):
   ```bash
   python import_inventory.py "path/to/Items.csv"
   ```

4. Start server and verify:
   ```bash
   python run.py
   ```

5. Check imported data at: http://localhost:8000/docs

