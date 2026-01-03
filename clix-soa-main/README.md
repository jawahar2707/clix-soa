# CLIX SOA

A full-stack Service-Oriented Architecture (SOA) application for order allocation, inventory management, and customer relationship management.

## Tech Stack

**Frontend:**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Tailwind CSS** - Utility-first CSS framework

**Backend:**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Python 3.8 or higher** - [Download here](https://www.python.org/downloads/)
   - ⚠️ Make sure to check "Add Python to PATH" during installation
   - Or install from Microsoft Store (search for "Python 3.11")

2. **Node.js (LTS version)** - [Download here](https://nodejs.org/)
   - This includes npm (Node Package Manager)

## Quick Setup

### Automated Setup (Recommended)

1. Open PowerShell in the project root directory
2. Run the setup script:
   ```powershell
   .\setup.ps1
   ```

This will automatically:
- Check prerequisites (Python, Node.js)
- Install all dependencies
- Initialize the database

### Manual Setup

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for detailed manual setup instructions.

## Getting Started

### 1. Start the Backend Server

Open a terminal and run:

```bash
cd backend
python run.py
```

The API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 2. Start the Frontend Server

Open a **new** terminal and run:

```bash
npm install  # First time only
npm run dev
```

The frontend will be available at:
- **Application**: http://localhost:3001

## Project Structure

- `app/` - Next.js App Router pages and layouts
- `backend/` - Python FastAPI backend application
- `components/` - React components
- `lib/` - Utility functions and API clients
- `types/` - TypeScript type definitions

## Available Scripts

**Frontend:**
- `npm run dev` - Start development server (port 3001)
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

**Backend:**
- `python run.py` - Start FastAPI server (port 8000)
- `python init_db.py` - Initialize/reset database
- `python import_customers.py <csv_file>` - Import customers from CSV
- `python import_inventory.py <csv_file>` - Import inventory from CSV

## Features

- **Customer Management** - View and manage customer information
- **Inventory Management** - Track and manage inventory items
- **Order Processing** - Create and manage orders
- **Payment Tracking** - Monitor customer payments
- **Order Allocation** - Intelligent order allocation algorithm
- **Metrics & Analytics** - Business metrics and reporting
- **Data Import/Export** - CSV import and export functionality

## Documentation

- [SETUP_GUIDE.md](./SETUP_GUIDE.md) - Complete setup instructions
- [backend/QUICK_START.md](./backend/QUICK_START.md) - Quick start guide
- [backend/README.md](./backend/README.md) - Backend documentation
- [FRONTEND_README.md](./FRONTEND_README.md) - Frontend documentation

## Troubleshooting

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for troubleshooting tips and common issues.
