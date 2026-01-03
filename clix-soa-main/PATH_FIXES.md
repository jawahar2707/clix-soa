# Path Fixes Documentation

## Overview

This document describes all the path-related fixes made to ensure the project works correctly regardless of where it's located or how it's run.

## Changes Made

### 1. Backend Configuration (`backend/config.py`)

**Issue**: Database path was relative (`sqlite:///./order_allocation.db`), which could fail if the script wasn't run from the correct directory.

**Fix**: 
- Now uses absolute path based on the backend directory
- Database file is always created in the backend directory
- Added `BACKEND_DIR` and `DATABASE_FILE` constants for reference

```python
BACKEND_DIR = Path(__file__).parent.absolute()
DATABASE_FILE = BACKEND_DIR / "order_allocation.db"
database_url: str = f"sqlite:///{DATABASE_FILE}"
```

### 2. Database Connection (`backend/app/database.py`)

**Issue**: Used `sys.path.insert` which could cause import issues.

**Fix**:
- Uses try/except for config import
- Falls back to sys.path manipulation only if needed
- More robust import handling

### 3. Export Service (`backend/app/services/export_service.py`)

**Issue**: Export directory path was relative and could break.

**Fix**:
- Uses absolute path based on backend directory
- Export directories are always created relative to backend folder
- `_BACKEND_DIR` is calculated from the file's location

```python
_BACKEND_DIR = Path(__file__).parent.parent.parent.absolute()
EXPORT_DIR = _BACKEND_DIR / "exports"
CSV_DIR = EXPORT_DIR / "csv"
PRINT_DIR = EXPORT_DIR / "print"
```

### 4. Allocation Service (`backend/app/services/allocation_service.py`)

**Issue**: Used `sys.path.insert` for config import.

**Fix**:
- Tries direct import first
- Falls back to sys.path manipulation only if needed
- More robust error handling

### 5. Metrics Service (`backend/app/services/metrics_service.py`)

**Issue**: Used `sys.path.insert` for config import.

**Fix**:
- Same as allocation service - try direct import, fallback if needed

### 6. Server Runner (`backend/run.py`)

**Issue**: Could fail if not run from backend directory.

**Fix**:
- Automatically changes to backend directory before running
- Sets `reload_dirs` to only watch backend directory
- Works regardless of where the script is called from

```python
backend_dir = Path(__file__).parent.absolute()
os.chdir(backend_dir)
```

### 7. Database Initialization (`backend/init_db.py`)

**Issue**: Could fail if not run from backend directory.

**Fix**:
- Automatically changes to backend directory before running
- Shows the database file path for clarity
- Works regardless of where the script is called from

## How Paths Work Now

### Backend Paths

All backend paths are now calculated relative to the `backend/` directory:

1. **Database**: Always in `backend/order_allocation.db`
2. **Exports**: Always in `backend/exports/`
3. **Config**: Always imports from `backend/config.py`

### Frontend Paths

Frontend paths use Next.js conventions:
- TypeScript path aliases: `@/*` maps to project root
- API URL: Configurable via `NEXT_PUBLIC_API_URL` environment variable
- Default: `http://localhost:8000`

## Running the Project

### Backend

The backend scripts now work from any directory:

```bash
# From project root
cd backend
python run.py

# Or from anywhere
python C:\path\to\project\backend\run.py
```

### Frontend

Frontend should be run from the project root:

```bash
# From project root
npm run dev
```

## Environment Variables

### Frontend (Optional)

Create `.env.local` in the project root:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If not set, defaults to `http://localhost:8000`.

### Backend

No environment variables required. Database path is automatically configured.

## Verification

To verify paths are working correctly:

1. **Backend**:
   ```bash
   cd backend
   python init_db.py
   # Should show: Database file: C:\...\backend\order_allocation.db
   ```

2. **Frontend**:
   ```bash
   npm run dev
   # Should start on http://localhost:3001
   ```

3. **Check exports**:
   - Run an allocation
   - Check that CSV files are created in `backend/exports/csv/`

## Benefits

✅ **Portable**: Project can be moved to any location
✅ **Robust**: Paths work regardless of working directory
✅ **Clear**: All paths are explicit and absolute
✅ **Maintainable**: Centralized path configuration
✅ **Error-resistant**: Better error handling for imports

## Notes

- All paths use `Path(__file__).parent` to calculate relative to the file location
- Absolute paths ensure consistency across different execution contexts
- The database file is always in the backend directory for easy backup
- Export files are always in the backend/exports directory

## Troubleshooting

If you encounter path-related errors:

1. **Import errors**: Make sure you're running scripts from the correct directory or they handle directory changes
2. **Database not found**: Check that `order_allocation.db` is in the `backend/` directory
3. **Export errors**: Check that `backend/exports/` directory exists (created automatically)
4. **Frontend API errors**: Verify `NEXT_PUBLIC_API_URL` is set correctly or using default

All scripts now handle these issues automatically, but if problems persist, check the file paths in the error messages.

