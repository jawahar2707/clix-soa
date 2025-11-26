# Quick Import Guide

## Import Your Data

### Option 1: Use the Batch Script (Windows)

Simply double-click `import_all_data.bat` or run:
```bash
import_all_data.bat
```

This will:
1. Initialize the database
2. Import all customers from your CSV
3. Import all inventory items (base items only)

### Option 2: Manual Import

#### 1. Initialize Database
```bash
python init_db.py
```

#### 2. Import Customers
```bash
python import_customers.py "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"
```

#### 3. Import Inventory

**Base items only (recommended):**
```bash
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv"
```

**With size variations (creates separate items for each size):**
```bash
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv" --with-sizes
```

## About Size Variations

Your items support sizes:
- **Numeric**: 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 105, 110
- **Alphabetic**: XS, S, M, L, XL, XXL

### Two Approaches:

1. **Single Item with Size Field** (Default)
   - One inventory entry per item code
   - Size stored as a field
   - Better for items where size doesn't affect inventory tracking separately

2. **Separate Items per Size** (Use `--with-sizes`)
   - Creates separate inventory entries: `ITEM-45`, `ITEM-50`, `ITEM-XS`, etc.
   - Better when you need to track inventory separately for each size
   - Creates many more inventory records

## After Import

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Verify data:**
   - Open: http://localhost:8000/docs
   - Check customers: `GET /customers/`
   - Check inventory: `GET /inventory/`

3. **Update quantities:**
   - All items start with 0 quantity
   - Update via API or create update script from your ERP

4. **Set customer credit limits:**
   - Update via API: `PUT /customers/{id}`

## Expected Results

From your CSV files:
- **Customers**: ~840+ customers will be imported
- **Inventory**: ~500+ items (base) or ~7,000+ items (with sizes)

## Troubleshooting

- **File not found**: Check the file path in the command
- **Encoding errors**: CSV files should be UTF-8 encoded
- **Duplicate errors**: Script automatically skips duplicates
- **Database locked**: Close any other connections to the database

