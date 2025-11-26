# Setup and Data Import Guide

## Prerequisites Check

Before importing data, ensure Python is installed:

1. **Check if Python is installed:**
   ```bash
   python --version
   ```
   OR
   ```bash
   py --version
   ```

2. **If Python is not installed:**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Restart your terminal/command prompt after installation

## Step-by-Step Import Process

### Step 1: Install Python Dependencies

Open a terminal/command prompt in the `backend` folder and run:

```bash
pip install -r requirements.txt
```

Or if you have multiple Python versions:
```bash
python -m pip install -r requirements.txt
```

### Step 2: Initialize Database

```bash
python init_db.py
```

This creates the SQLite database file `order_allocation.db`.

### Step 3: Import Customers

```bash
python import_customers.py "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"
```

**Expected output:**
- Will import ~840+ customers
- Skips duplicates automatically
- Initializes customer metrics

### Step 4: Import Inventory Items

**Option A: Base items only (Recommended - faster, less items)**
```bash
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv"
```

**Option B: With size variations (Creates separate items for each size)**
```bash
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv" --with-sizes
```

**Note:** Option B will create many more inventory items (approximately 20x more).

### Step 5: Verify Import

Start the server:
```bash
python run.py
```

Then open your browser and go to:
- http://localhost:8000/docs

Check the data:
- `GET /customers/` - Should show imported customers
- `GET /inventory/` - Should show imported inventory items

## Quick Import (Windows Batch File)

If Python is properly installed and in PATH, you can simply:

1. Double-click `import_all_data.bat`
2. Or run from command prompt:
   ```bash
   import_all_data.bat
   ```

## Troubleshooting

### "Python was not found"
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal after installation

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Make sure you're in the `backend` directory

### "File not found" errors
- Check that the CSV files exist at the specified paths
- Update the paths in the commands if needed

### "Database is locked" errors
- Close any other programs accessing the database
- Make sure the server is not running

### Import takes too long
- This is normal for large datasets
- Customer import: ~1-2 minutes for 840+ customers
- Inventory import: ~2-5 minutes for 500+ items
- With sizes: ~10-20 minutes for 7,000+ items

## After Import

1. **Update Inventory Quantities**
   - All items start with 0 quantity
   - Update via API: `PUT /inventory/{id}`
   - Or create a script to import quantities from your ERP

2. **Set Customer Credit Limits**
   - Update via API: `PUT /customers/{id}`
   - Set appropriate credit limits and periods

3. **Record Payment History**
   - Add payment records: `POST /payments/`
   - This helps calculate customer performance scores

4. **Create Orders**
   - Start creating orders: `POST /orders/`
   - Then allocate them: `POST /allocation/allocate`

## Expected Import Results

- **Customers**: ~840+ customers imported
- **Inventory (base)**: ~500+ items
- **Inventory (with sizes)**: ~7,000+ items (if using --with-sizes)

## Next Steps

Once data is imported:
1. Review imported data via API docs
2. Update inventory quantities
3. Set customer credit limits
4. Add payment history
5. Start using the allocation system!

