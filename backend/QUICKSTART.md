# Quick Start Guide

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Initialize Database

```bash
python init_db.py
```

This creates the SQLite database file `order_allocation.db` in the backend directory.

## Step 3: (Optional) Load Sample Data

To test the system with sample data:

```bash
python sample_data.py
```

This creates:
- 4 sample customers
- 5 inventory items
- 4 orders
- 7 payment records
- Calculates customer metrics

## Step 4: Start the Server

```bash
python run.py
```

Or on Windows, double-click `start.bat`

The server will start on `http://localhost:8000`

## Step 5: Access API Documentation

Open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Testing the Allocation System

### 1. Check Customer Metrics

```bash
GET http://localhost:8000/metrics/customer/1
```

### 2. Allocate Orders

```bash
POST http://localhost:8000/allocation/allocate
Content-Type: application/json

{
  "order_ids": [1, 2, 3, 4],
  "recalculate_metrics": true
}
```

### 3. View Allocation Results

```bash
GET http://localhost:8000/allocation/history
```

## Example Workflow

1. **Create a Customer**
   ```json
   POST /customers/
   {
     "name": "Test Customer",
     "contact": "1234567890",
     "credit_limit": 100000,
     "credit_period_days": 30
   }
   ```

2. **Add Inventory**
   ```json
   POST /inventory/
   {
     "product_code": "TEST-001",
     "product_name": "Test Product",
     "available_quantity": 1000,
     "unit": "pieces"
   }
   ```

3. **Create an Order**
   ```json
   POST /orders/
   {
     "customer_id": 1,
     "items": [
       {
         "inventory_id": 1,
         "requested_quantity": 500
       }
     ]
   }
   ```

4. **Record a Payment**
   ```json
   POST /payments/
   {
     "customer_id": 1,
     "payment_date": "2024-01-15T10:00:00",
     "amount": 50000,
     "due_date": "2024-01-10T10:00:00"
   }
   ```

5. **Allocate Orders**
   ```json
   POST /allocation/allocate
   {
     "recalculate_metrics": true
   }
   ```

## Understanding the Allocation Algorithm

The system allocates orders based on:

1. **Customer Performance (30%)**
   - Total order history
   - Order fulfillment rate
   - Customer loyalty

2. **Payment Frequency (25%)**
   - On-time payment percentage
   - Average days to payment

3. **Credit Period Adherence (25%)**
   - Adherence to credit terms
   - Overdue payment frequency

4. **Stock Availability (20%)**
   - Available quantity
   - Demand vs supply

The algorithm:
- Calculates a priority score for each customer
- Distributes available stock proportionally based on priority
- Ensures minimum 5% and maximum 40% allocation per customer
- Creates allocation records for tracking

## Next Steps

- Customize allocation weights in `config.py`
- Add more customers, inventory, and orders
- Review allocation history and customer metrics
- Integrate with your existing ERP system

