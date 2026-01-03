@echo off
echo Starting Order Allocation System...
echo.
echo Initializing database...
python init_db.py
echo.
echo Starting server...
python run.py
pause

