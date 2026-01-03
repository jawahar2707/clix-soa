"""
Configuration settings for the Order Allocation System
"""
from pydantic_settings import BaseSettings
from pathlib import Path
import os

# Get the backend directory (where this config.py file is located)
BACKEND_DIR = Path(__file__).parent.absolute()
# Database file path - always in the backend directory
DATABASE_FILE = BACKEND_DIR / "order_allocation.db"

class Settings(BaseSettings):
    # Database configuration - use absolute path
    database_url: str = f"sqlite:///{DATABASE_FILE}"
    
    # Allocation algorithm weights
    performance_weight: float = 0.30
    payment_frequency_weight: float = 0.25
    credit_period_weight: float = 0.25
    stock_availability_weight: float = 0.20
    
    # Minimum allocation rules
    min_allocation_percentage: float = 0.05  # 5% minimum allocation
    max_allocation_percentage: float = 0.40  # 40% maximum allocation per customer
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

