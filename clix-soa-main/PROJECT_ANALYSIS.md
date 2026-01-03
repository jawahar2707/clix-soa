# CLIX SOA - Complete Project Analysis

## Executive Summary

**CLIX SOA** (Service-Oriented Architecture) is a full-stack order allocation system designed for intelligent distribution of inventory to customers based on performance metrics, payment history, and stock availability. The system operates offline using SQLite and provides a modern web interface for managing customers, inventory, orders, payments, and automated allocation.

---

## 1. Architecture Overview

### Technology Stack

**Frontend:**
- **Framework**: Next.js 14 (React 18.3.1) with App Router
- **Language**: TypeScript 5.5.4
- **Styling**: Tailwind CSS 3.4.7
- **HTTP Client**: Axios 1.7.7
- **Charts**: Recharts 2.12.7
- **Icons**: Lucide React 0.427.0
- **CSV Processing**: PapaParse 5.4.1
- **Date Handling**: date-fns 3.6.0

**Backend:**
- **Framework**: FastAPI (Python)
- **Database**: SQLite (file-based, offline)
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Server**: Uvicorn (with auto-reload)

### System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (Next.js)                   │
│  Port: 3001                                             │
│  - Dashboard, Customers, Inventory, Orders, Payments    │
│  - Allocation Interface, Metrics Dashboard               │
│  - Import/Export Functionality                          │
└──────────────────┬──────────────────────────────────────┘
                   │ HTTP/REST API
┌──────────────────▼──────────────────────────────────────┐
│              Backend API (FastAPI)                       │
│  Port: 8000                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   API Layer  │  │ Service Layer│  │  Data Layer   │ │
│  │  (Routers)   │→ │ (Business    │→ │  (SQLAlchemy) │ │
│  │              │  │  Logic)      │  │               │ │
│  └──────────────┘  └──────────────┘  └───────┬────────┘ │
└───────────────────────────────────────────────┼─────────┘
                                                │
                                    ┌───────────▼──────────┐
                                    │   SQLite Database     │
                                    │  order_allocation.db  │
                                    └──────────────────────┘
```

---

## 2. Database Schema

### Core Tables

#### 1. **customers**
- Stores customer information and credit settings
- Fields: id, name, contact, email, address, status, credit_limit, credit_period_days
- Relationships: One-to-many with orders, payments; One-to-one with customer_metrics

#### 2. **inventory**
- Product stock information
- Fields: id, product_code (unique), product_name, category, size, available_quantity, reserved_quantity, unit
- Supports sizes: 45-110 (numeric) or XS, S, M, L, XL, XXL

#### 3. **orders**
- Customer orders
- Fields: id, customer_id, order_date, total_quantity, status (pending/allocated/fulfilled/cancelled), notes
- Relationships: Many-to-one with customers; One-to-many with order_items, allocations

#### 4. **order_items**
- Order line items
- Fields: id, order_id, inventory_id, requested_quantity, allocated_quantity
- Links orders to specific inventory items with quantities

#### 5. **payments**
- Payment history records
- Fields: id, customer_id, payment_date, amount, due_date, status (pending/paid/overdue/partial), payment_method, reference_number, notes
- Used for calculating customer performance metrics

#### 6. **customer_metrics**
- Calculated performance scores (one per customer)
- Fields: customer_id (unique), total_orders, total_order_value, payment_frequency_score (0-100), credit_period_score (0-100), performance_score (0-100), overall_score (weighted), on_time_payment_percentage, average_days_to_payment, overdue_count, total_payments, last_calculated

#### 7. **allocations**
- Allocation history records
- Fields: id, order_id, inventory_id, allocated_quantity, allocation_date, algorithm_version, notes
- Tracks what was allocated to which orders

### Database Relationships

```
customers (1) ──< (N) orders
customers (1) ──< (N) payments
customers (1) ──< (1) customer_metrics

orders (1) ──< (N) order_items
orders (1) ──< (N) allocations

inventory (1) ──< (N) order_items
inventory (1) ──< (N) allocations
```

---

## 3. Business Logic & Services

### 3.1 Metrics Service (`metrics_service.py`)

**Purpose**: Calculate customer performance scores for allocation decisions

**Key Methods:**

1. **`calculate_payment_frequency_score(customer_id, db)`**
   - Calculates score (0-100) based on on-time payment percentage
   - Formula: `(on_time_percentage * 0.7) + (days_score * 0.3)`
   - Penalizes late payments

2. **`calculate_credit_period_score(customer_id, db)`**
   - Measures adherence to credit terms
   - Formula: `100 - (overdue_percentage * 0.6) - (days_penalty)`
   - Decreases with overdue payments and days

3. **`calculate_performance_score(customer_id, db)`**
   - Overall customer performance
   - Based on: order count (30%), fulfillment rate (40%), order value (30%)

4. **`calculate_all_metrics(customer_id, db)`**
   - Calculates all metrics and stores in `customer_metrics` table
   - Returns `CustomerMetric` object with weighted overall_score

5. **`recalculate_all_metrics(db)`**
   - Bulk recalculation for all active customers
   - Used before allocation runs

**Weight Configuration** (from `config.py`):
- Performance: 30%
- Payment Frequency: 25%
- Credit Period: 25%
- Stock Availability: 20% (used in allocation, not metrics)

### 3.2 Allocation Service (`allocation_service.py`)

**Purpose**: Intelligently allocate orders to customers based on multiple criteria

**Allocation Algorithm:**

1. **Input**: List of pending order IDs (or all pending orders)

2. **Pre-processing**:
   - Optionally recalculates all customer metrics
   - Groups orders by customer
   - Aggregates inventory requirements

3. **For each inventory item**:
   - Calculate customer priorities (based on overall_score)
   - Normalize priorities to 0-100 scale
   - Allocate stock based on:
     - Priority-weighted distribution
     - Customer demand
     - Min/max constraints (5%-40% per customer)
   - Distribute remaining stock proportionally

4. **Allocation Constraints**:
   - Minimum allocation: 5% of available stock
   - Maximum allocation: 40% of available stock per customer
   - Cannot exceed customer demand
   - Cannot exceed available stock

5. **Post-processing**:
   - Creates allocation records
   - Updates order_item.allocated_quantity
   - Updates inventory (reserved_quantity, available_quantity)
   - Updates order status:
     - "allocated" if ≥95% fulfilled
     - "partially_allocated" if <95% but >0%
     - "pending" if 0% allocated

**Key Methods:**

- `allocate_orders(order_ids, db, recalculate_metrics)` - Main allocation function
- `_calculate_customer_priorities(customer_ids, db)` - Priority calculation
- `_allocate_inventory_to_customers(...)` - Core allocation logic
- `_process_order_allocation(order, db)` - Process individual order results

### 3.3 Export Service (`export_service.py`)

**Purpose**: Export allocation data to CSV and prepare print formats

**Features:**
- Detailed allocation CSV with all allocation records
- Summary CSV with order-level allocation results
- Print format data preparation (structured JSON)
- Automatic export after allocation runs
- Timestamped filenames

**Export Directory Structure:**
```
backend/exports/
├── csv/          # CSV export files
└── print/        # Print format files (future)
```

---

## 4. API Endpoints

### 4.1 Customers API (`/customers`)

- `POST /customers/` - Create customer (auto-calculates metrics)
- `GET /customers/` - List all customers (with pagination)
- `GET /customers/{id}` - Get customer details
- `PUT /customers/{id}` - Update customer (recalculates metrics if credit fields change)
- `DELETE /customers/{id}` - Delete customer

### 4.2 Inventory API (`/inventory`)

- `POST /inventory/` - Create inventory item
- `GET /inventory/` - List all inventory (with pagination)
- `GET /inventory/{id}` - Get inventory item
- `GET /inventory/code/{code}` - Get by product code
- `PUT /inventory/{id}` - Update inventory
- `DELETE /inventory/{id}` - Delete inventory

### 4.3 Orders API (`/orders`)

- `POST /orders/` - Create order with items
- `GET /orders/` - List orders (filters: status, customer_id)
- `GET /orders/{id}` - Get order with items
- `PUT /orders/{id}` - Update order (status, notes)
- `DELETE /orders/{id}` - Delete order (cascades to items)

### 4.4 Payments API (`/payments`)

- `POST /payments/` - Create payment record
- `GET /payments/` - List payments (filters: customer_id, status)
- `GET /payments/{id}` - Get payment details
- `PUT /payments/{id}` - Update payment
- `DELETE /payments/{id}` - Delete payment

### 4.5 Allocation API (`/allocation`)

- `POST /allocation/allocate` - Run allocation algorithm
  - Request: `{ order_ids?: number[], recalculate_metrics?: boolean }`
  - Response: List of `AllocationResult` objects
  - Automatically exports CSV after allocation
- `GET /allocation/history` - Get allocation history (filters: order_id, inventory_id)
- `GET /allocation/order/{order_id}` - Get allocations for specific order

### 4.6 Metrics API (`/metrics`)

- `GET /metrics/customer/{id}` - Get customer metrics
- `POST /metrics/customer/{id}/recalculate` - Recalculate metrics for customer
- `POST /metrics/recalculate-all` - Recalculate all customer metrics

### 4.7 Export API (`/export`)

- `GET /export/allocation/csv/{allocation_id}` - Download allocation CSV
- `GET /export/allocation/latest/csv` - Download most recent CSV
- `GET /export/allocation/list` - List all available CSV exports
- `GET /export/allocation/print/{allocation_id}` - Get print format data

### 4.8 Health & Root

- `GET /` - API information
- `GET /health` - Health check endpoint

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 5. Frontend Application

### 5.1 Page Structure

**Dashboard** (`/`)
- System overview with statistics
- Server status indicator
- Quick action links
- Pending orders alert

**Customers** (`/customers`)
- List view with search/filter
- Create/Edit/Delete customers
- Customer detail page (`/customers/[id]`)
- Import/Export CSV functionality

**Inventory** (`/inventory`)
- List view with search (code, name, category)
- Stock statistics
- Create/Edit/Delete items
- Item detail page (`/inventory/[id]`)
- Import/Export CSV

**Orders** (`/orders`)
- List view with status filter
- Create order page (`/orders/new`)
- Order detail page (`/orders/[id]`)
- Shows allocation status
- Import/Export CSV

**Payments** (`/payments`)
- List view with status/customer filters
- Payment statistics
- Create payment page (`/payments/new`)
- Payment detail page (`/payments/[id]`)
- Import/Export CSV

**Allocation** (`/allocation`)
- Run allocation interface
- View allocation results
- Allocation history
- Export allocation data

**Metrics** (`/metrics`)
- Customer performance dashboard
- Visual charts (Recharts)
- Top performers analysis
- Export metrics data
- Recalculate metrics button

### 5.2 Components

**Layout.tsx**
- Sidebar navigation
- Responsive design (mobile/desktop)
- Active route highlighting

**DataTable.tsx**
- Reusable table component
- Search, sort, pagination
- Custom column rendering

**ImportExport.tsx**
- CSV import/export functionality
- File upload with validation
- Import result display
- Template download
- Error handling

### 5.3 API Client (`lib/api.ts`)

Centralized API client using Axios:
- Request/response interceptors
- Error handling
- Type-safe API methods for all endpoints
- Environment-based API URL configuration

### 5.4 CSV Utilities (`lib/csv-utils.ts`)

- CSV parsing (PapaParse)
- CSV export generation
- Import validation
- Error reporting

### 5.5 Type Definitions (`types/index.ts`)

TypeScript interfaces for:
- Customer, Inventory, Order, OrderItem
- Payment, Allocation, CustomerMetric

---

## 6. Key Features

### 6.1 Intelligent Order Allocation

- **Multi-criteria decision making**: Combines customer performance, payment history, credit adherence, and stock availability
- **Fair distribution**: Min/max constraints prevent over-allocation to single customers
- **Automatic metrics**: Customer scores calculated automatically
- **Stock management**: Tracks available vs reserved quantities
- **Allocation history**: Complete audit trail

### 6.2 Customer Performance Tracking

- **Payment frequency scoring**: Based on on-time payment percentage
- **Credit period adherence**: Tracks overdue payments and days
- **Order performance**: Based on order count, fulfillment rate, value
- **Weighted overall score**: Combines all metrics with configurable weights
- **Automatic recalculation**: Updates when payments/orders change

### 6.3 Data Import/Export

- **CSV Import**: Bulk import for customers, inventory, orders, payments
- **CSV Export**: Export all data types
- **Import templates**: Downloadable templates with correct format
- **Validation**: Error checking and reporting
- **Automatic allocation export**: CSV generated after each allocation run

### 6.4 Inventory Management

- **Product tracking**: Product codes, names, categories, sizes
- **Stock levels**: Available and reserved quantities
- **Size support**: Numeric (45-110) and text (XS-XXL)
- **Unit tracking**: Pieces, kg, etc.

### 6.5 Order Management

- **Multi-item orders**: Orders can contain multiple inventory items
- **Status tracking**: pending → allocated/partially_allocated → fulfilled
- **Allocation tracking**: Shows requested vs allocated quantities
- **Customer linking**: Orders linked to customers

### 6.6 Payment Tracking

- **Payment history**: Complete payment records
- **Status management**: pending, paid, overdue, partial
- **Due date tracking**: Automatic status calculation
- **Metrics integration**: Payments affect customer scores

---

## 7. Configuration

### Backend Configuration (`backend/config.py`)

```python
# Allocation algorithm weights
performance_weight: 0.30          # 30%
payment_frequency_weight: 0.25    # 25%
credit_period_weight: 0.25       # 25%
stock_availability_weight: 0.20  # 20%

# Allocation constraints
min_allocation_percentage: 0.05  # 5% minimum
max_allocation_percentage: 0.40  # 40% maximum per customer

# Database
database_url: "sqlite:///./order_allocation.db"
```

### Frontend Configuration

- API URL: `NEXT_PUBLIC_API_URL` (default: http://localhost:8000)
- Port: 3001 (configured in `package.json`)

---

## 8. Data Flow

### Allocation Flow

```
1. User creates orders → Orders stored as "pending"
2. User triggers allocation → POST /allocation/allocate
3. System recalculates metrics (optional) → MetricsService
4. System groups orders by customer and inventory
5. For each inventory item:
   a. Calculate customer priorities
   b. Allocate stock based on priority and demand
   c. Apply min/max constraints
   d. Distribute remaining stock
6. Create allocation records
7. Update order items (allocated_quantity)
8. Update inventory (reserved/available)
9. Update order status
10. Export CSV automatically
11. Return allocation results
```

### Metrics Calculation Flow

```
1. Payment/Order created/updated
2. Trigger metrics recalculation (automatic or manual)
3. Calculate payment_frequency_score
4. Calculate credit_period_score
5. Calculate performance_score
6. Calculate weighted overall_score
7. Store in customer_metrics table
8. Metrics used in next allocation run
```

---

## 9. File Structure

```
clix-soa-main/
├── app/                          # Next.js App Router
│   ├── page.tsx                  # Dashboard
│   ├── layout.tsx                # Root layout
│   ├── customers/                # Customer pages
│   ├── inventory/                # Inventory pages
│   ├── orders/                   # Order pages
│   ├── payments/                 # Payment pages
│   ├── allocation/               # Allocation page
│   └── metrics/                  # Metrics page
├── components/                   # React components
│   ├── Layout.tsx                # Main layout with sidebar
│   ├── DataTable.tsx             # Reusable table
│   └── ImportExport.tsx          # Import/export component
├── lib/                          # Utilities
│   ├── api.ts                    # API client
│   └── csv-utils.ts              # CSV utilities
├── types/                        # TypeScript types
│   └── index.ts
├── backend/                      # Python backend
│   ├── app/
│   │   ├── api/                  # API endpoints
│   │   │   ├── customers.py
│   │   │   ├── inventory.py
│   │   │   ├── orders.py
│   │   │   ├── payments.py
│   │   │   ├── allocation.py
│   │   │   ├── metrics.py
│   │   │   └── export.py
│   │   ├── services/             # Business logic
│   │   │   ├── allocation_service.py
│   │   │   ├── metrics_service.py
│   │   │   └── export_service.py
│   │   ├── models.py             # Database models
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── database.py         # DB connection
│   │   └── main.py                # FastAPI app
│   ├── config.py                 # Configuration
│   ├── init_db.py                # Database initialization
│   ├── run.py                     # Server runner
│   ├── requirements.txt           # Python dependencies
│   └── exports/                   # Export directory
│       ├── csv/                   # CSV exports
│       └── print/                 # Print formats
├── package.json                   # Node.js dependencies
├── next.config.mjs                # Next.js config
├── tailwind.config.ts             # Tailwind config
└── tsconfig.json                  # TypeScript config
```

---

## 10. Strengths & Highlights

### ✅ **Well-Architected**
- Clean separation of concerns (API → Service → Data layers)
- Reusable components and services
- Type-safe with TypeScript and Pydantic

### ✅ **Intelligent Algorithm**
- Multi-criteria decision making
- Configurable weights and constraints
- Fair distribution logic

### ✅ **Complete Feature Set**
- Full CRUD operations
- Import/Export functionality
- Metrics and analytics
- Allocation automation

### ✅ **User-Friendly**
- Modern, responsive UI
- Clear navigation
- Real-time feedback
- Error handling

### ✅ **Offline Capable**
- SQLite database (no server required)
- File-based storage
- Easy backup (copy .db file)

### ✅ **Well-Documented**
- API documentation (Swagger/ReDoc)
- Code comments
- Setup guides
- README files

---

## 11. Potential Improvements

### 🔄 **Future Enhancements**

1. **Authentication & Authorization**
   - User login system
   - Role-based access control
   - Audit logging

2. **Database Migration**
   - Support for PostgreSQL/MySQL
   - Multi-user capability
   - Connection pooling

3. **Advanced Features**
   - Email notifications
   - SMS alerts
   - PDF report generation
   - Advanced analytics dashboard
   - Forecasting/prediction

4. **Performance**
   - Caching layer (Redis)
   - Database indexing optimization
   - Pagination improvements
   - Background job processing

5. **Testing**
   - Unit tests
   - Integration tests
   - E2E tests
   - Load testing

6. **Deployment**
   - Docker containerization
   - CI/CD pipeline
   - Production deployment guide
   - Environment configuration

---

## 12. Usage Scenarios

### Scenario 1: New Customer Onboarding
1. Create customer via UI or CSV import
2. System automatically calculates initial metrics
3. Customer can place orders
4. Orders allocated based on performance

### Scenario 2: Order Allocation
1. Multiple customers place orders
2. Inventory is limited
3. Run allocation algorithm
4. System distributes stock fairly based on:
   - Customer performance scores
   - Payment history
   - Credit adherence
   - Stock availability
5. CSV export generated automatically

### Scenario 3: Payment Updates
1. Record customer payment
2. System recalculates customer metrics
3. Future allocations reflect updated scores
4. Better-performing customers get priority

### Scenario 4: Inventory Management
1. Update stock levels
2. System tracks available vs reserved
3. Allocation prevents overallocation
4. Real-time stock visibility

---

## 13. Technical Metrics

- **Backend API Endpoints**: 30+
- **Database Tables**: 7
- **Frontend Pages**: 10+
- **Reusable Components**: 3
- **Services**: 3 (Metrics, Allocation, Export)
- **Lines of Code**: ~5,000+ (estimated)

---

## 14. Conclusion

CLIX SOA is a **production-ready, feature-complete order allocation system** that demonstrates:

- Modern full-stack development practices
- Intelligent business logic implementation
- User-friendly interface design
- Comprehensive data management
- Scalable architecture

The system is well-suited for:
- Small to medium businesses
- Offline/on-premise deployments
- Inventory distribution scenarios
- Customer relationship management
- Performance-based allocation needs

---

**Analysis Date**: 2024
**Project Version**: 1.0.0
**Status**: Production Ready

