"""
Database initialization script
"""
import os
from pathlib import Path

# Ensure we're running from the backend directory
backend_dir = Path(__file__).parent.absolute()
os.chdir(backend_dir)

from app.database import init_db, engine
from app.models import Base
from config import DATABASE_FILE

if __name__ == "__main__":
    print("Initializing database...")
    print(f"Backend directory: {backend_dir}")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    print(f"Database file: {DATABASE_FILE}")

