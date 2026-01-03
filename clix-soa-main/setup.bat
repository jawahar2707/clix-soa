@echo off
echo ========================================
echo CLIX SOA - Complete System Setup
echo ========================================
echo.

REM Check for Python
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo.
    echo Please install Python 3.8+ from:
    echo - Microsoft Store: Search for "Python 3.11"
    echo - Official site: https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
) else (
    python --version
    echo [OK] Python found
)

REM Check for Node.js
echo.
echo Checking Node.js installation...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed!
    echo.
    echo Please install Node.js from:
    echo - Official site: https://nodejs.org/
    echo - Download LTS version (recommended)
    echo.
    pause
    exit /b 1
) else (
    node --version
    echo [OK] Node.js found
)

REM Check for npm
echo.
echo Checking npm installation...
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed!
    pause
    exit /b 1
) else (
    npm --version
    echo [OK] npm found
)

echo.
echo ========================================
echo Setting up Backend (Python)
echo ========================================
echo.

cd backend
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found in backend directory
    pause
    exit /b 1
)

echo Installing Python dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [OK] Python dependencies installed

echo.
echo Initializing database...
python init_db.py
if %errorlevel% neq 0 (
    echo [ERROR] Failed to initialize database
    pause
    exit /b 1
)
echo [OK] Database initialized

cd ..

echo.
echo ========================================
echo Setting up Frontend (Node.js)
echo ========================================
echo.

if not exist "package.json" (
    echo [ERROR] package.json not found
    pause
    exit /b 1
)

echo Installing Node.js dependencies...
npm install
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Node.js dependencies
    pause
    exit /b 1
)
echo [OK] Node.js dependencies installed

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Start the backend server:
echo    cd backend
echo    python run.py
echo    (API will be available at http://localhost:8000)
echo.
echo 2. Start the frontend server (in a new terminal):
echo    npm run dev
echo    (Frontend will be available at http://localhost:3001)
echo.
echo 3. Access the application:
echo    - Frontend: http://localhost:3001
echo    - API Docs: http://localhost:8000/docs
echo.
pause

