# Export Features Documentation

## Overview

The Order Allocation System automatically generates CSV exports for every allocation run. Print format functionality is prepared for future implementation.

## CSV Export Features

### Automatic CSV Generation

Every time you run an allocation, the system automatically:
1. **Saves allocation records** to the database
2. **Generates detailed CSV file** with all allocation details
3. **Generates summary CSV file** with order-level summary
4. **Saves files** to `backend/exports/csv/` directory

### CSV File Types

#### 1. Detailed Allocation CSV
- **Filename**: `allocation_orders_{order_ids}_{timestamp}.csv`
- **Contains**: Complete allocation details including:
  - Allocation ID and Date
  - Order and Customer Information
  - Product Details (Code, Name, Category, Size)
  - Requested vs Allocated Quantities
  - Allocation Percentage
  - Algorithm Version
  - Order Status

#### 2. Summary CSV
- **Filename**: `allocation_summary_{timestamp}.csv`
- **Contains**: Order-level summary including:
  - Order ID and Customer Name
  - Total Requested and Allocated
  - Allocation Percentage
  - Status and Item Count
  - Messages

### File Naming Convention

- Format: `allocation_{type}_{identifiers}_{YYYYMMDD_HHMMSS}.csv`
- Example: `allocation_orders_5_6_7_8_20250115_143022.csv`
- Timestamp ensures unique filenames

### Accessing CSV Files

#### Via API Endpoints

1. **List All Exports**
   ```
   GET /export/allocation/list
   ```
   Returns list of all available CSV files

2. **Download Latest CSV**
   ```
   GET /export/allocation/latest/csv
   ```
   Downloads the most recent allocation CSV

3. **Download Specific CSV**
   ```
   GET /export/allocation/csv/{allocation_id}
   ```
   Downloads CSV for specific allocation

#### Via Frontend

- **Allocation Page**: "Download CSV" button appears after allocation
- **Allocation History**: Export button available
- Files are automatically generated and ready to download

#### Via File System

- Location: `backend/exports/csv/`
- Files are stored locally on the server
- Can be accessed directly from the file system

## Print Format (To Be Implemented)

### Structure Prepared

The system includes a `prepare_print_format_data()` function that:
- Groups allocations by order
- Structures data for print formatting
- Includes customer and product details
- Ready for print template implementation

### Future Implementation

Print format will include:
- **Print Template**: Professional allocation report format
- **PDF Generation**: Convert print format to PDF
- **Print Preview**: View before printing
- **Custom Templates**: Support for different print formats

### Print Format Data Structure

```python
{
    'allocation_date': '2025-01-15 14:30:22',
    'orders': [
        {
            'order_id': 5,
            'order_date': '2025-01-10',
            'customer_name': 'Customer Name',
            'items': [
                {
                    'product_code': 'ABC-123',
                    'product_name': 'Product Name',
                    'requested': 100,
                    'allocated': 75,
                    'unit': 'PCS'
                }
            ]
        }
    ],
    'summary': {
        'total_requested': 1000,
        'total_allocated': 750
    }
}
```

## Implementation Details

### Export Service

Located in: `backend/app/services/export_service.py`

Key functions:
- `export_allocation_to_csv()` - Detailed CSV export
- `export_allocation_summary_to_csv()` - Summary CSV export
- `prepare_print_format_data()` - Print format data preparation

### Automatic Export Trigger

The export is automatically triggered in:
- `backend/app/api/allocation.py` - `allocate_orders()` endpoint
- Runs after successful allocation
- Does not fail allocation if export fails (logs warning)

### Export Directory Structure

```
backend/
└── exports/
    ├── csv/          # CSV files (auto-generated)
    ├── print/        # Print files (future)
    └── README.md     # Documentation
```

## Usage Examples

### Running Allocation with Auto-Export

1. **Run Allocation** via API or Frontend
2. **CSV Files Generated** automatically
3. **Download CSV** from frontend or API
4. **Files Saved** in `exports/csv/` directory

### Programmatic Access

```python
from app.services.export_service import ExportService

# Export allocation results
csv_path = ExportService.export_allocation_to_csv(
    allocation_results=results,
    order_ids=[5, 6, 7, 8],
    db=db
)
```

## File Management

### Storage
- Files stored in `backend/exports/csv/`
- No automatic cleanup (manual management)
- Files named with timestamps for uniqueness

### Git Ignore
- CSV files are excluded from git (see `.gitignore`)
- Directory structure is preserved
- Only export files are ignored

## Future Enhancements

1. **Print Format Implementation**
   - PDF generation
   - Print templates
   - Print preview

2. **File Management**
   - Automatic cleanup of old files
   - File retention policies
   - Archive functionality

3. **Additional Formats**
   - Excel export
   - JSON export
   - XML export

4. **Email Integration**
   - Email CSV to users
   - Scheduled reports

## Notes

- CSV files are UTF-8 encoded
- Includes headers for easy import
- Compatible with Excel and other spreadsheet software
- Print format structure ready for implementation

