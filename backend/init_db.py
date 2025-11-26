"""
Database initialization script
"""
from app.database import init_db, engine
from app.models import Base

if __name__ == "__main__":
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")
    print("Database file: order_allocation.db")

