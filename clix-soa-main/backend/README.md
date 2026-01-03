# Order Allocation System - Backend

A backend system for allocating orders to customers based on performance metrics, payment history, credit period adherence, and stock availability.

## Features

- **Customer Management**: Create, update, and manage customer information
- **Inventory Management**: Track product inventory and availability
- **Order Management**: Create and manage customer orders
- **Payment Tracking**: Record and track customer payments
- **Performance Metrics**: Automatic calculation of customer performance scores
- **Intelligent Allocation**: Allocate orders based on multiple criteria:
  - Customer Performance (30%)
  - Payment Frequency (25%)
  - Credit Period Adherence (25%)
  - Stock Availability (20%)

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: SQLite (offline, file-based)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python init_db.py
```

## Running the Server

```bash
python run.py
```

Or using uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Customers
- `POST /customers/` - Create a new customer
- `GET /customers/` - Get all customers
- `GET /customers/{id}` - Get a specific customer
- `PUT /customers/{id}` - Update a customer
- `DELETE /customers/{id}` - Delete a customer

### Inventory
- `POST /inventory/` - Create inventory item
- `GET /inventory/` - Get all inventory items
- `GET /inventory/{id}` - Get specific inventory item
- `GET /inventory/code/{code}` - Get inventory by product code
- `PUT /inventory/{id}` - Update inventory item
- `DELETE /inventory/{id}` - Delete inventory item

### Orders
- `POST /orders/` - Create a new order
- `GET /orders/` - Get all orders (with optional filters)
- `GET /orders/{id}` - Get a specific order
- `PUT /orders/{id}` - Update an order
- `DELETE /orders/{id}` - Delete an order

### Payments
- `POST /payments/` - Create a payment record
- `GET /payments/` - Get all payments (with optional filters)
- `GET /payments/{id}` - Get a specific payment
- `PUT /payments/{id}` - Update a payment
- `DELETE /payments/{id}` - Delete a payment

### Allocation
- `POST /allocation/allocate` - Allocate orders to customers
- `GET /allocation/history` - Get allocation history
- `GET /allocation/order/{id}` - Get allocations for an order

### Metrics
- `GET /metrics/customer/{id}` - Get customer metrics
- `POST /metrics/customer/{id}/recalculate` - Recalculate customer metrics
- `POST /metrics/recalculate-all` - Recalculate all customer metrics

## Usage Example

### 1. Create a Customer
```bash
curl -X POST "http://localhost:8000/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ABC Textiles",
    "contact": "1234567890",
    "email": "abc@example.com",
    "credit_limit": 100000,
    "credit_period_days": 30
  }'
```

### 2. Add Inventory
```bash
curl -X POST "http://localhost:8000/inventory/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_code": "INW-001",
    "product_name": "Cotton Briefs",
    "category": "Men",
    "available_quantity": 1000,
    "unit": "pieces"
  }'
```

### 3. Create an Order
```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "items": [
      {
        "inventory_id": 1,
        "requested_quantity": 500
      }
    ]
  }'
```

### 4. Record a Payment
```bash
curl -X POST "http://localhost:8000/payments/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "payment_date": "2024-01-15T10:00:00",
    "amount": 50000,
    "due_date": "2024-01-10T10:00:00",
    "status": "paid"
  }'
```

### 5. Allocate Orders
```bash
curl -X POST "http://localhost:8000/allocation/allocate" \
  -H "Content-Type: application/json" \
  -d '{
    "order_ids": [1, 2, 3],
    "recalculate_metrics": true
  }'
```

## Database

The system uses SQLite, which creates a file `order_allocation.db` in the project root. This file contains all your data and can be easily backed up by copying the file.

## Configuration

Edit `config.py` to adjust:
- Allocation algorithm weights
- Minimum/maximum allocation percentages
- Database settings

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   │   ├── customers.py
│   │   ├── inventory.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   ├── allocation.py
│   │   └── metrics.py
│   ├── services/         # Business logic
│   │   ├── metrics_service.py
│   │   └── allocation_service.py
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # Database connection
│   └── main.py          # FastAPI app
├── config.py            # Configuration
├── init_db.py           # Database initialization
├── run.py               # Server runner
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Notes

- The system is designed for offline use with SQLite
- All data is stored locally in a single database file
- The allocation algorithm automatically considers customer performance, payment history, and stock availability
- Customer metrics are recalculated automatically when payments or orders are updated

