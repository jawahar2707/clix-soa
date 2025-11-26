# PowerShell script to setup Python and import data
# Run this script as Administrator for best results

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Order Allocation System - Setup & Import" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking for Python installation..." -ForegroundColor Yellow
$pythonPath = $null

# Try different Python commands
$pythonCommands = @("python", "py", "python3")
foreach ($cmd in $pythonCommands) {
    try {
        $result = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $result -match "Python") {
            $pythonPath = $cmd
            Write-Host "Found Python: $cmd" -ForegroundColor Green
            break
        }
    } catch {
        continue
    }
}

# If Python not found, try to find it in common locations
if (-not $pythonPath) {
    Write-Host "Python not found in PATH. Searching common locations..." -ForegroundColor Yellow
    
    $commonPaths = @(
        "$env:LOCALAPPDATA\Programs\Python",
        "C:\Program Files\Python*",
        "C:\Python*",
        "$env:ProgramFiles\Python*"
    )
    
    foreach ($pathPattern in $commonPaths) {
        $paths = Get-ChildItem -Path $pathPattern -ErrorAction SilentlyContinue -Directory
        foreach ($path in $paths) {
            $pythonExe = Join-Path $path.FullName "python.exe"
            if (Test-Path $pythonExe) {
                $pythonPath = $pythonExe
                Write-Host "Found Python at: $pythonExe" -ForegroundColor Green
                break
            }
        }
        if ($pythonPath) { break }
    }
}

# If still not found, provide installation instructions
if (-not $pythonPath) {
    Write-Host ""
    Write-Host "Python is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Python 3.8 or higher:" -ForegroundColor Yellow
    Write-Host "1. Download from: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "2. During installation, CHECK 'Add Python to PATH'" -ForegroundColor White
    Write-Host "3. Restart this terminal after installation" -ForegroundColor White
    Write-Host "4. Run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "Or install via Microsoft Store:" -ForegroundColor Yellow
    Write-Host "   Search for 'Python' in Microsoft Store and install" -ForegroundColor White
    Write-Host ""
    
    $install = Read-Host "Would you like to open the Python download page? (Y/N)"
    if ($install -eq "Y" -or $install -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }
    
    exit 1
}

# Check Python version
Write-Host ""
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $version = & $pythonPath --version 2>&1
    Write-Host "Python version: $version" -ForegroundColor Green
    
    # Extract version number
    if ($version -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            Write-Host "Warning: Python 3.8 or higher is recommended" -ForegroundColor Yellow
        }
    }
} catch {
    Write-Host "Could not determine Python version" -ForegroundColor Yellow
}

# Navigate to backend directory
$backendPath = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path $backendPath)) {
    $backendPath = $PSScriptRoot
}

Set-Location $backendPath
Write-Host ""
Write-Host "Working directory: $backendPath" -ForegroundColor Cyan

# Install dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    & $pythonPath -m pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error installing dependencies. Trying with --user flag..." -ForegroundColor Yellow
        & $pythonPath -m pip install --user -r requirements.txt
    }
    Write-Host "Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error installing dependencies: $_" -ForegroundColor Red
    exit 1
}

# Initialize database
Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
try {
    & $pythonPath init_db.py
    Write-Host "Database initialized!" -ForegroundColor Green
} catch {
    Write-Host "Error initializing database: $_" -ForegroundColor Red
    exit 1
}

# Import customers
Write-Host ""
Write-Host "Importing customers..." -ForegroundColor Yellow
$customerCsv = "C:\Users\Hxtreme\Downloads\Customers(Download)(L).csv"
if (Test-Path $customerCsv) {
    try {
        & $pythonPath import_customers.py $customerCsv
        Write-Host "Customers imported!" -ForegroundColor Green
    } catch {
        Write-Host "Error importing customers: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Customer CSV file not found at: $customerCsv" -ForegroundColor Yellow
    Write-Host "Please update the path in the script or import manually" -ForegroundColor Yellow
}

# Import inventory
Write-Host ""
Write-Host "Importing inventory items..." -ForegroundColor Yellow
$inventoryCsv = "C:\Users\Hxtreme\Downloads\Items (7).csv"
if (Test-Path $inventoryCsv) {
    try {
        & $pythonPath import_inventory.py $inventoryCsv
        Write-Host "Inventory imported!" -ForegroundColor Green
    } catch {
        Write-Host "Error importing inventory: $_" -ForegroundColor Red
    }
} else {
    Write-Host "Inventory CSV file not found at: $inventoryCsv" -ForegroundColor Yellow
    Write-Host "Please update the path in the script or import manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setup and Import Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Start the server: python run.py" -ForegroundColor White
Write-Host "2. Open browser: http://localhost:8000/docs" -ForegroundColor White
Write-Host "3. Verify imported data" -ForegroundColor White
Write-Host ""

