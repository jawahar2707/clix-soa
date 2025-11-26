# Quick Start - Install Python and Import Data

## ⚠️ Python Not Installed

Python needs to be installed before importing data. Here are your options:

## Option 1: Install Python via Microsoft Store (Easiest)

1. **Open Microsoft Store**
   - Press `Windows Key` and type "Microsoft Store"
   - Click to open

2. **Search for Python**
   - Type "Python 3.11" or "Python 3.12" in the search bar
   - Click on "Python 3.11" or "Python 3.12" from Python Software Foundation

3. **Install**
   - Click "Get" or "Install"
   - Wait for installation (usually 2-5 minutes)

4. **Restart Terminal**
   - Close and reopen your terminal/command prompt
   - Or restart PowerShell

5. **Verify Installation**
   ```bash
   python --version
   ```

6. **Run Import Script**
   ```powershell
   cd "C:\Users\Hxtreme\CLIX SOA\backend"
   .\setup_and_import.ps1
   ```

## Option 2: Install Python from Official Website

1. **Download Python**
   - Go to: https://www.python.org/downloads/
   - Click "Download Python 3.x.x" (latest version)

2. **Run Installer**
   - Double-click the downloaded file
   - **CRITICAL**: Check ✅ "Add Python to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation

3. **Restart Terminal**
   - Close and reopen your terminal

4. **Verify Installation**
   ```bash
   python --version
   ```

5. **Run Import Script**
   ```powershell
   cd "C:\Users\Hxtreme\CLIX SOA\backend"
   .\setup_and_import.ps1
   ```

## Option 3: Manual Installation Steps

After installing Python, run these commands manually:

```bash
# Navigate to backend folder
cd "C:\Users\Hxtreme\CLIX SOA\backend"

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_db.py

# Import customers
python import_customers.py "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"

# Import inventory
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv"
```

## After Installation

Once Python is installed and data is imported:

1. **Start the server:**
   ```bash
   python run.py
   ```

2. **Open API documentation:**
   - Browser: http://localhost:8000/docs

3. **Verify data:**
   - Check customers: `GET /customers/`
   - Check inventory: `GET /inventory/`

## Need Help?

- See `INSTALL_PYTHON.md` for detailed installation guide
- See `SETUP_AND_IMPORT.md` for complete setup instructions
- Check `README.md` for system documentation

## What Gets Imported?

- **Customers**: ~840+ customers from your CSV
- **Inventory**: ~500+ items (or ~7,000+ with size variations)
- **Database**: Created at `backend/order_allocation.db`

