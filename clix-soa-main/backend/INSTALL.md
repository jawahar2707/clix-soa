# Installation Instructions

## Prerequisites

1. **Python 3.8 or higher** must be installed on your system
   - Download from: https://www.python.org/downloads/
   - During installation, make sure to check "Add Python to PATH"

## Installation Steps

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if you have multiple Python versions:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```bash
   python init_db.py
   ```
   
   Or:
   ```bash
   python3 init_db.py
   ```

4. **Run the server:**
   ```bash
   python run.py
   ```
   
   Or:
   ```bash
   python3 run.py
   ```

## Verify Installation

Once the server is running, you should see:
- Server running on `http://localhost:8000`
- API documentation at `http://localhost:8000/docs`

## Troubleshooting

### Python not found
- Make sure Python is installed and added to PATH
- Try using `python3` instead of `python`
- On Windows, you may need to use `py` launcher

### Module not found errors
- Make sure you're in the `backend` directory
- Verify all dependencies are installed: `pip list`
- Try reinstalling: `pip install -r requirements.txt --force-reinstall`

### Database errors
- Delete `order_allocation.db` and run `python init_db.py` again
- Make sure you have write permissions in the backend directory

