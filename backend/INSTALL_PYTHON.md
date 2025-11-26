# Python Installation Guide

## Quick Installation

### Option 1: Microsoft Store (Easiest)
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Click "Install"
4. Wait for installation to complete
5. Restart your terminal/command prompt

### Option 2: Official Python Website (Recommended)
1. Go to: https://www.python.org/downloads/
2. Download the latest Python 3.x version
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH" during installation
5. Click "Install Now"
6. Restart your terminal/command prompt

### Option 3: Using PowerShell Script
Run the provided PowerShell script:
```powershell
.\setup_and_import.ps1
```

This script will:
- Check if Python is installed
- Guide you through installation if needed
- Install dependencies
- Import your data

## Verify Installation

After installation, verify Python is working:

```bash
python --version
```

You should see something like:
```
Python 3.11.5
```

## After Python Installation

Once Python is installed, you can:

1. **Run the setup script:**
   ```powershell
   cd "C:\Users\Hxtreme\CLIX SOA\backend"
   .\setup_and_import.ps1
   ```

2. **Or manually:**
   ```bash
   cd "C:\Users\Hxtreme\CLIX SOA\backend"
   pip install -r requirements.txt
   python init_db.py
   python import_customers.py "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"
   python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv"
   ```

## Troubleshooting

### "Python was not found" after installation
- Make sure you checked "Add Python to PATH" during installation
- Restart your terminal/command prompt
- If still not working, reinstall Python and ensure PATH is checked

### Permission errors
- Run terminal as Administrator
- Or use `--user` flag: `pip install --user -r requirements.txt`

### Module not found errors
- Make sure you're in the `backend` directory
- Run: `pip install -r requirements.txt`

