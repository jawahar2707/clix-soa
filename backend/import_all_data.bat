@echo off
echo ========================================
echo Order Allocation System - Data Import
echo ========================================
echo.

echo Step 1: Initializing database...
python init_db.py
echo.

echo Step 2: Importing customers...
python import_customers.py "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"
echo.

echo Step 3: Importing inventory items (base items only)...
python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv"
echo.

echo ========================================
echo Import completed!
echo ========================================
echo.
echo Note: To import inventory with size variations, run:
echo   python import_inventory.py "C:\Users\Hxtreme\Downloads\Items (7).csv" --with-sizes
echo.
pause

