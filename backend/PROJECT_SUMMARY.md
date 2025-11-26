# Order Allocation System - Project Summary

## Overview

A complete offline backend system for allocating orders to customers based on multiple performance criteria. Built with FastAPI and SQLite for a single-user, offline deployment scenario.

## What Has Been Built

### 1. Database Layer
- **SQLite Database**: File-based, no server required
- **7 Core Tables**:
  - `customers` - Customer information and credit settings
  - `inventory` - Product stock information
  - `orders` - Customer orders
  - `order_items` - Order line items
  - `payments` - Payment history
  - `customer_metrics` - Calculated performance scores
  - `allocations` - Allocation history records

### 2. Business Logic Services

#### Metrics Service (`metrics_service.py`)
- Calculates customer performance scores (0-100)
- Payment frequency scoring based on on-time payments
- Credit period adherence scoring
- Overall customer performance metrics
- Automatic recalculation on data changes

#### Allocation Service (`allocation_service.py`)
- Intelligent order allocation algorithm
- Multi-criteria decision making:
  - Customer Performance (30% weight)
  - Payment Frequency (25% weight)
  - Credit Period Adherence (25% weight)
  - Stock Availability (20% weight)
- Priority-based distribution
- Min/max allocation constraints (5%-40%)
- Creates allocation records for tracking

### 3. REST API Endpoints

#### Customers API (`/customers`)
- Create, read, update, delete customers
- Automatic metrics calculation on creation/update

#### Inventory API (`/inventory`)
- Manage product inventory
- Track available and reserved quantities
- Search by product code

#### Orders API (`/orders`)
- Create orders with multiple items
- Filter by status, customer
- Track order status (pending, allocated, fulfilled)

#### Payments API (`/payments`)
- Record customer payments
- Automatic status calculation (paid, overdue)
- Triggers metrics recalculation

#### Allocation API (`/allocation`)
- Allocate orders based on algorithm
- View allocation history
- Get allocations for specific orders

#### Metrics API (`/metrics`)
- View customer performance metrics
- Recalculate metrics on demand
- Bulk recalculation for all customers

### 4. Configuration
- Adjustable algorithm weights
- Min/max allocation percentages
- Database settings
- All configurable via `config.py`

## Key Features

✅ **Offline Operation**: No internet required, SQLite file-based database
✅ **Automatic Metrics**: Customer scores calculated automatically
✅ **Intelligent Allocation**: Multi-criteria algorithm for fair distribution
✅ **Complete API**: Full CRUD operations for all entities
✅ **API Documentation**: Auto-generated Swagger/ReDoc docs
✅ **Sample Data**: Script to populate test data
✅ **Easy Setup**: Simple installation and initialization

## Technology Stack

- **Framework**: FastAPI (Python 3.8+)
- **Database**: SQLite
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Server**: Uvicorn

## File Structure

```
backend/
├── app/
│   ├── api/                    # API endpoints
│   │   ├── customers.py
│   │   ├── inventory.py
│   │   ├── orders.py
│   │   ├── payments.py
│   │   ├── allocation.py
│   │   └── metrics.py
│   ├── services/               # Business logic
│   │   ├── metrics_service.py
│   │   └── allocation_service.py
│   ├── models.py               # Database models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # DB connection
│   └── main.py                 # FastAPI app
├── config.py                   # Configuration
├── init_db.py                  # Database initialization
├── run.py                      # Server runner
├── sample_data.py              # Sample data generator
├── requirements.txt            # Dependencies
├── README.md                   # Full documentation
├── QUICKSTART.md              # Quick start guide
└── INSTALL.md                 # Installation instructions
```

## How It Works

1. **Data Entry**: Add customers, inventory, orders, and payments via API
2. **Metrics Calculation**: System automatically calculates customer performance scores
3. **Allocation Request**: Call allocation API with pending orders
4. **Algorithm Execution**:
   - Calculates priority scores for each customer
   - Distributes available stock based on priority and demand
   - Creates allocation records
   - Updates inventory and order status
5. **Results**: View allocation results and history

## Allocation Algorithm Details

The allocation algorithm uses a weighted scoring system:

1. **Calculate Customer Priorities**
   - Get overall performance score from metrics
   - Normalize scores (0-100 scale)

2. **Distribute Stock**
   - Sort customers by priority (descending)
   - Allocate based on priority share and demand
   - Apply min/max constraints
   - Distribute remaining stock proportionally

3. **Create Records**
   - Create allocation records for each order-item
   - Update order item allocated quantities
   - Update inventory (reserved/available)
   - Update order status

## Usage Scenarios

### Scenario 1: New Order Allocation
1. Customer places order → Create via `/orders/`
2. System calculates metrics → Automatic or via `/metrics/`
3. Run allocation → `POST /allocation/allocate`
4. Review results → `GET /allocation/history`

### Scenario 2: Payment Updates
1. Record payment → `POST /payments/`
2. Metrics auto-recalculate → Customer score updates
3. Future allocations reflect new scores

### Scenario 3: Inventory Updates
1. Update stock → `PUT /inventory/{id}`
2. New allocations use updated quantities
3. System prevents overallocation

## Next Steps for Production

1. **Frontend Development**: Build web or desktop UI
2. **Authentication**: Add user authentication if needed
3. **Reporting**: Add advanced reporting and analytics
4. **Export**: Add data export functionality
5. **Backup**: Implement automated database backup
6. **Integration**: Connect with existing ERP systems

## Support & Documentation

- **API Docs**: http://localhost:8000/docs (when server running)
- **Full README**: See `README.md`
- **Quick Start**: See `QUICKSTART.md`
- **Installation**: See `INSTALL.md`

## Notes

- Database file: `order_allocation.db` (created in backend directory)
- All data is stored locally - easy to backup by copying the .db file
- System designed for single-user offline operation
- Can be extended to online/multi-user with PostgreSQL

