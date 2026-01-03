# CLIX SOA - Complete Setup Guide

This guide will help you set up the entire CLIX SOA system, including both the frontend and backend.

## Prerequisites

Before starting, you need to install:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Or install from Microsoft Store (search for "Python 3.11")
   - ⚠️ **Important**: During installation, check "Add Python to PATH"

2. **Node.js (LTS version recommended)**
   - Download from: https://nodejs.org/
   - This will also install npm (Node Package Manager)

## Quick Setup (Automated)

1. **Open PowerShell in the project root directory** (`clix-soa-main`)

2. **Run the setup script:**
   ```powershell
   .\setup.ps1
   ```

   This script will:
   - Check if Python and Node.js are installed
   - Install all Python dependencies
   - Initialize the database
   - Install all Node.js dependencies

## Manual Setup

If you prefer to set up manually or the automated script doesn't work:

### Backend Setup

1. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

2. **Install Python dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```
   Or if you have multiple Python versions:
   ```powershell
   python -m pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```powershell
   python init_db.py
   ```

### Frontend Setup

1. **Navigate to project root:**
   ```powershell
   cd ..
   ```
   (or navigate to `clix-soa-main` directory)

2. **Install Node.js dependencies:**
   ```powershell
   npm install
   ```

## Starting the Application

### Start Backend Server

1. **Open a terminal/PowerShell window**

2. **Navigate to backend directory:**
   ```powershell
   cd backend
   ```

3. **Start the server:**
   ```powershell
   python run.py
   ```

   The API will be available at: **http://localhost:8000**
   - API Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Start Frontend Server

1. **Open a NEW terminal/PowerShell window** (keep backend running)

2. **Navigate to project root:**
   ```powershell
   cd clix-soa-main
   ```

3. **Start the development server:**
   ```powershell
   npm run dev
   ```

   The frontend will be available at: **http://localhost:3001**

## Verifying the Setup

1. **Check Backend:**
   - Open http://localhost:8000/docs in your browser
   - You should see the FastAPI interactive documentation
   - Try the `/customers/` endpoint to verify the API is working

2. **Check Frontend:**
   - Open http://localhost:3001 in your browser
   - You should see the CLIX SOA application interface

## Importing Data (Optional)

If you have CSV files with customer or inventory data, you can import them:

1. **Import Customers:**
   ```powershell
   cd backend
   python import_customers.py "path\to\customers.csv"
   ```

2. **Import Inventory:**
   ```powershell
   python import_inventory.py "path\to\inventory.csv"
   ```

For more details, see:
- `backend/QUICK_START.md`
- `backend/IMPORT_GUIDE.md`

## Troubleshooting

### Python not found
- Make sure Python is installed and added to PATH
- Try using `py` instead of `python` on Windows
- Restart your terminal after installing Python

### Node.js/npm not found
- Make sure Node.js is installed (includes npm)
- Restart your terminal after installing Node.js
- Verify with: `node --version` and `npm --version`

### Port already in use
- Backend uses port 8000 - make sure nothing else is using it
- Frontend uses port 3001 - make sure nothing else is using it
- You can change ports in:
  - Backend: Edit `backend/run.py`
  - Frontend: Edit `package.json` (change the port in the "dev" script)

### Database errors
- Delete `backend/order_allocation.db` and run `python init_db.py` again
- Make sure you have write permissions in the backend directory

### Module not found errors
- Make sure you're in the correct directory
- Reinstall dependencies:
  - Backend: `pip install -r requirements.txt --force-reinstall`
  - Frontend: Delete `node_modules` folder and run `npm install` again

## Project Structure

```
clix-soa-main/
├── app/              # Next.js frontend pages
├── backend/          # Python FastAPI backend
├── components/       # React components
├── lib/             # Utility functions
├── types/           # TypeScript type definitions
└── setup.ps1        # Automated setup script
```

## Need Help?

- Check the documentation in the `backend/` directory
- See `README.md` for project overview
- Review `backend/QUICK_START.md` for quick reference

