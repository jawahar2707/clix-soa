"""
Script to run the FastAPI server
"""
import uvicorn
import os
from pathlib import Path

# Ensure we're running from the backend directory
# This makes the script work regardless of where it's called from
backend_dir = Path(__file__).parent.absolute()
os.chdir(backend_dir)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        reload_dirs=[str(backend_dir)]  # Only watch backend directory for changes
    )

