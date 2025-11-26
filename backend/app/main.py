"""
Main FastAPI application for Order Allocation System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api import customers, inventory, orders, payments, allocation, metrics, export

# Create FastAPI app
app = FastAPI(
    title="Order Allocation System",
    description="Backend API for allocating orders to customers based on performance metrics",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(customers.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(payments.router)
app.include_router(allocation.router)
app.include_router(metrics.router)
app.include_router(export.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Order Allocation System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

