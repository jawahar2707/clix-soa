# Frontend - Order Allocation System

## Overview

A modern, user-friendly web interface for the Order Allocation System built with Next.js 14, React, and Tailwind CSS.

## Features

### ✅ Complete Import/Export Functionality

**All pages support:**
- **CSV Import**: Upload CSV files to bulk import data
- **CSV Export**: Download data as CSV files
- **Import Templates**: Download templates for correct CSV format
- **Error Handling**: Detailed import results with error reporting

### 📊 Pages & Features

1. **Dashboard** (`/`)
   - System overview with statistics
   - Quick actions
   - Server status indicator
   - Pending orders alert

2. **Customers** (`/customers`)
   - View all customers
   - Search and filter
   - Import/Export CSV
   - Create, edit, delete customers
   - Customer details view

3. **Inventory** (`/inventory`)
   - View all inventory items
   - Search by code, name, category
   - Import/Export CSV
   - Stock statistics
   - Create, edit, delete items
   - Size support (45-110, XS-XXL)

4. **Orders** (`/orders`)
   - View all orders
   - Filter by status
   - Search functionality
   - Import/Export CSV
   - Create new orders
   - Order details and allocation status

5. **Payments** (`/payments`)
   - View payment history
   - Filter by status
   - Payment statistics
   - Import/Export CSV
   - Create, edit payments
   - Track payment performance

6. **Allocation** (`/allocation`)
   - Run allocation algorithm
   - View allocation results
   - Allocation history
   - Export allocation data
   - Real-time allocation status

7. **Metrics** (`/metrics`)
   - Customer performance scores
   - Visual charts and graphs
   - Export metrics data
   - Recalculate metrics
   - Top performers analysis

## Import/Export Features

### Import Capabilities

- **Customers**: Import from CSV with fields: Name, Contact, Email, Address, Credit Limit, Credit Period
- **Inventory**: Import products with: Product Code, Name, Category, Size, Quantity, Unit
- **Payments**: Import payment records with: Customer ID, Payment Date, Amount, Due Date, Status
- **Orders**: Import orders (with customer and items)

### Export Capabilities

- **Customers**: Export all customer data
- **Inventory**: Export all inventory items with quantities
- **Orders**: Export order details and status
- **Payments**: Export payment history
- **Allocations**: Export allocation history
- **Metrics**: Export customer performance metrics

### Import Templates

Each import feature includes a downloadable template showing the correct CSV format.

## UI Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean, intuitive design with Tailwind CSS
- **Search & Filter**: Advanced search on all list pages
- **Sortable Tables**: Click column headers to sort
- **Pagination**: Large datasets are paginated
- **Real-time Updates**: Data refreshes after operations
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during operations

## Getting Started

### Prerequisites

- Node.js 18+ installed
- Backend server running on http://localhost:8000

### Installation

```bash
# Install dependencies (if not already installed)
npm install
```

### Running the Frontend

```bash
# Development mode
npm run dev

# Production build
npm run build
npm start
```

The frontend will be available at: **http://localhost:3001**

### Environment Variables

Create a `.env.local` file (optional):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage Guide

### Importing Data

1. Navigate to any page (Customers, Inventory, Payments, etc.)
2. Click **"Import CSV"** button
3. Select your CSV file
4. Review import results
5. Data is automatically imported

### Exporting Data

1. Navigate to any page
2. Click **"Export CSV"** button
3. CSV file downloads automatically

### Creating Records

- Click **"Add"** or **"Create"** buttons
- Fill in the form
- Submit to create

### Running Allocations

1. Go to **Allocation** page
2. Configure settings (optional)
3. Click **"Allocate Orders"**
4. View results and history

## File Structure

```
app/
├── page.tsx              # Dashboard
├── layout.tsx            # Root layout
├── customers/
│   ├── page.tsx          # Customers list
│   ├── [id]/page.tsx     # Customer details
│   └── new/page.tsx      # Create customer
├── inventory/
│   ├── page.tsx          # Inventory list
│   ├── [id]/page.tsx     # Item details
│   └── new/page.tsx      # Create item
├── orders/
│   ├── page.tsx          # Orders list
│   ├── [id]/page.tsx     # Order details
│   └── new/page.tsx      # Create order
├── payments/
│   ├── page.tsx          # Payments list
│   ├── [id]/page.tsx     # Payment details
│   └── new/page.tsx      # Create payment
├── allocation/
│   └── page.tsx          # Allocation interface
└── metrics/
    └── page.tsx          # Customer metrics

components/
├── Layout.tsx            # Main layout with sidebar
├── ImportExport.tsx      # Reusable import/export component
└── DataTable.tsx         # Reusable data table component

lib/
├── api.ts                # API client functions
└── csv-utils.ts         # CSV import/export utilities
```

## API Integration

The frontend connects to the backend API at `http://localhost:8000` by default.

All API calls are handled through:
- `lib/api.ts` - Centralized API client
- Axios for HTTP requests
- Automatic error handling

## Styling

- **Framework**: Tailwind CSS
- **Icons**: Lucide React
- **Charts**: Recharts
- **Responsive**: Mobile-first design

## Key Components

### ImportExport Component

Reusable component for import/export functionality:
- File upload
- CSV parsing
- Progress indicators
- Error reporting
- Template download

### DataTable Component

Reusable table component with:
- Search functionality
- Sorting
- Pagination
- Custom rendering
- Row actions

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Troubleshooting

### API Connection Issues
- Ensure backend server is running on port 8000
- Check `NEXT_PUBLIC_API_URL` in environment variables
- Verify CORS settings in backend

### Import Errors
- Check CSV format matches template
- Ensure required fields are present
- Verify data types (numbers, dates, etc.)

### Build Errors
- Run `npm install` to ensure dependencies are installed
- Clear `.next` folder and rebuild
- Check Node.js version (18+)

## Next Steps

1. Start the backend: `cd backend && python run.py`
2. Start the frontend: `npm run dev`
3. Open browser: http://localhost:3001
4. Begin using the system!

## Support

For issues or questions:
- Check backend logs
- Check browser console
- Review API documentation at http://localhost:8000/docs
