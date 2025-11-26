# Mock Data for Testing

## Overview

This directory contains scripts to create and delete mock data for testing the Order Allocation System.

## Created Mock Data

### Orders (4 orders created)
- **Order #5**: SIVALAYAM PRINTING AND PACKING - 3 items, 225 total quantity
- **Order #6**: SPICTEX COTTON MILLS PVT LTD - 2 items, 350 total quantity  
- **Order #7**: VIJAYVELAVAN SPINNING MILLS PVT LTD - 3 items, 180 total quantity
- **Order #8**: V.S TEX - 1 item, 300 total quantity

### Payments (9 payments created)
- **Customer 1** (SIVALAYAM): 3 payments (excellent payer - on-time)
- **Customer 2** (SPICTEX): 2 payments (good payer)
- **Customer 3** (VIJAYVELAVAN): 3 payments (average payer - some delays)
- **Customer 4** (V.S TEX): 1 payment (new customer)

### Customer Metrics
- Metrics calculated for all 4 customers with orders/payments
- Includes performance scores, payment frequency, credit period adherence

## Usage

### Create Mock Data
```bash
cd backend
python create_mock_data.py
```

This will:
1. Create 4 sales orders with various items
2. Create payment history for customers
3. Calculate customer metrics automatically

### Delete Mock Data
```bash
cd backend
python delete_mock_data.py
```

This will:
1. Delete the 4 mock orders and their items
2. Delete customer metrics (payments are kept by default)
3. Clean up the database for finalization

## Notes

- Mock data uses existing customers and inventory from your imported data
- Orders are created with status "pending" - ready for allocation
- Payment history establishes different customer performance profiles
- Metrics are automatically calculated based on orders and payments
- You can modify the scripts to create different scenarios

## When to Delete

Delete the mock data when:
- You're ready to finalize the project
- You want to start with a clean database
- You need to test with production data only

## Customization

You can modify `create_mock_data.py` to:
- Create more/fewer orders
- Use different customers
- Create different payment scenarios
- Adjust order quantities and dates

