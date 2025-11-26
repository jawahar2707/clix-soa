# Exports Directory

This directory contains exported files from the Order Allocation System.

## Structure

```
exports/
├── csv/          # CSV export files for allocations
└── print/        # Print format files (to be implemented)
```

## CSV Exports

CSV files are automatically generated after each allocation run. Files are named with:
- `allocation_orders_{order_ids}_{timestamp}.csv` - For specific orders
- `allocation_all_{timestamp}.csv` - For all orders
- `allocation_summary_{timestamp}.csv` - Summary of allocations

## File Naming

- Format: `allocation_{type}_{timestamp}.csv`
- Timestamp format: `YYYYMMDD_HHMMSS`
- Example: `allocation_orders_5_6_7_8_20250115_143022.csv`

## Accessing Exports

### Via API
- List all exports: `GET /export/allocation/list`
- Download latest: `GET /export/allocation/latest/csv`
- Download specific: `GET /export/allocation/csv/{allocation_id}`

### Via File System
Files are stored in: `backend/exports/csv/`

## Print Format

Print format files will be generated in `exports/print/` directory (to be implemented).

