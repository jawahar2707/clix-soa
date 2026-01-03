"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os

# Import config from parent directory
# This works because backend/ is in Python path when running from backend/
try:
    from config import settings
except ImportError:
    # Fallback: add parent directory to path
    import sys
    backend_dir = Path(__file__).parent.parent.absolute()
    if str(backend_dir) not in sys.path:
        sys.path.insert(0, str(backend_dir))
    from config import settings

# Create SQLite engine
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

