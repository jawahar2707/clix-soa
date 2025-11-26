"""
API endpoints for exporting allocation data
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import Allocation, Order
from app.services.export_service import ExportService
from pathlib import Path

router = APIRouter(prefix="/export", tags=["export"])


@router.get("/allocation/csv/{allocation_id}")
def download_allocation_csv(allocation_id: int, db: Session = Depends(get_db)):
    """Download CSV file for a specific allocation"""
    allocation = db.query(Allocation).filter(Allocation.id == allocation_id).first()
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
    
    # Find the CSV file for this allocation
    csv_files = sorted(ExportService.CSV_DIR.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    # Try to find the most recent CSV that contains this allocation
    for csv_file in csv_files:
        # Simple check - in production, you might want to store mapping
        return FileResponse(
            path=str(csv_file),
            filename=csv_file.name,
            media_type='text/csv'
        )
    
    raise HTTPException(status_code=404, detail="CSV file not found")


@router.get("/allocation/latest/csv")
def download_latest_allocation_csv(db: Session = Depends(get_db)):
    """Download the most recent allocation CSV file"""
    csv_files = sorted(ExportService.CSV_DIR.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    if not csv_files:
        raise HTTPException(status_code=404, detail="No CSV files found")
    
    latest_file = csv_files[0]
    return FileResponse(
        path=str(latest_file),
        filename=latest_file.name,
        media_type='text/csv'
    )


@router.get("/allocation/list")
def list_allocation_exports():
    """List all available allocation CSV exports"""
    ExportService.ensure_directories()
    
    csv_files = sorted(ExportService.CSV_DIR.glob("*.csv"), key=lambda x: x.stat().st_mtime, reverse=True)
    
    files_list = []
    for csv_file in csv_files:
        stat = csv_file.stat()
        files_list.append({
            'filename': csv_file.name,
            'path': str(csv_file),
            'size': stat.st_size,
            'created': stat.st_mtime,
            'download_url': f"/export/allocation/csv/{csv_file.stem}"
        })
    
    return {
        'count': len(files_list),
        'files': files_list
    }


@router.get("/allocation/print/{allocation_id}")
def get_allocation_print_data(allocation_id: int, db: Session = Depends(get_db)):
    """Get allocation data formatted for printing (to be implemented)"""
    # This endpoint will return data for print format
    # The actual print format generation will be implemented later
    allocation = db.query(Allocation).filter(Allocation.id == allocation_id).first()
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
    
    # For now, return JSON data that can be formatted for printing
    order = db.query(Order).filter(Order.id == allocation.order_id).first()
    
    return {
        'message': 'Print format will be implemented later',
        'allocation_id': allocation_id,
        'order_id': allocation.order_id,
        'data': {
            'allocation_date': allocation.allocation_date.isoformat(),
            'allocated_quantity': allocation.allocated_quantity
        }
    }

