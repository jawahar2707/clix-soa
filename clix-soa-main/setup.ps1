# Comprehensive Setup Script for CLIX SOA Project
# This script checks prerequisites and sets up both frontend and backend

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CLIX SOA - Complete System Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$errors = @()
$warnings = @()

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

# Check Python
Write-Host "Checking Python installation..." -ForegroundColor Yellow
$pythonCmd = $null
$pythonCommands = @("python", "py", "python3")
foreach ($cmd in $pythonCommands) {
    if (Test-Command $cmd) {
        try {
            $version = & $cmd --version 2>&1
            if ($version -match "Python") {
                $pythonCmd = $cmd
                Write-Host "✓ Python found: $version" -ForegroundColor Green
                break
            }
        } catch {
            continue
        }
    }
}

if (-not $pythonCmd) {
    $errors += "Python is not installed"
    Write-Host "✗ Python not found" -ForegroundColor Red
    Write-Host "  Please install Python 3.8+ from:" -ForegroundColor Yellow
    Write-Host "  - Microsoft Store: Search for 'Python 3.11'" -ForegroundColor White
    Write-Host "  - Official site: https://www.python.org/downloads/" -ForegroundColor White
    Write-Host "  (Make sure to check 'Add Python to PATH' during installation)" -ForegroundColor White
} else {
    # Check Python version
    $version = & $pythonCmd --version 2>&1
    if ($version -match "Python (\d+)\.(\d+)") {
        $major = [int]$matches[1]
        $minor = [int]$matches[2]
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 8)) {
            $warnings += "Python version is below 3.8 (found $version)"
            Write-Host "⚠ Warning: Python 3.8+ recommended (found $version)" -ForegroundColor Yellow
        }
    }
}

# Check Node.js
Write-Host ""
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
if (Test-Command node) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
} else {
    $errors += "Node.js is not installed"
    Write-Host "✗ Node.js not found" -ForegroundColor Red
    Write-Host "  Please install Node.js from:" -ForegroundColor Yellow
    Write-Host "  - Official site: https://nodejs.org/" -ForegroundColor White
    Write-Host "  - Download LTS version (recommended)" -ForegroundColor White
}

# Check npm
Write-Host ""
Write-Host "Checking npm installation..." -ForegroundColor Yellow
if (Test-Command npm) {
    $npmVersion = npm --version
    Write-Host "✓ npm found: $npmVersion" -ForegroundColor Green
} else {
    if (-not $errors.Contains("Node.js is not installed")) {
        $errors += "npm is not installed"
        Write-Host "✗ npm not found" -ForegroundColor Red
    }
}

# If prerequisites are missing, show installation guide
if ($errors.Count -gt 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "MISSING PREREQUISITES" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    foreach ($error in $errors) {
        Write-Host "✗ $error" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Please install the missing prerequisites and run this script again." -ForegroundColor Yellow
    Write-Host ""
    
    $openPython = Read-Host "Would you like to open Python download page? (Y/N)"
    if ($openPython -eq "Y" -or $openPython -eq "y") {
        Start-Process "https://www.python.org/downloads/"
    }
    
    $openNode = Read-Host "Would you like to open Node.js download page? (Y/N)"
    if ($openNode -eq "Y" -or $openNode -eq "y") {
        Start-Process "https://nodejs.org/"
    }
    
    exit 1
}

# Show warnings
if ($warnings.Count -gt 0) {
    Write-Host ""
    Write-Host "Warnings:" -ForegroundColor Yellow
    foreach ($warning in $warnings) {
        Write-Host "⚠ $warning" -ForegroundColor Yellow
    }
    Write-Host ""
}

# Setup Backend
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Backend (Python)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$backendPath = Join-Path $PSScriptRoot "backend"
if (-not (Test-Path $backendPath)) {
    Write-Host "✗ Backend directory not found at: $backendPath" -ForegroundColor Red
    exit 1
}

Set-Location $backendPath
Write-Host "Working directory: $backendPath" -ForegroundColor Cyan

# Install Python dependencies
Write-Host ""
Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
try {
    & $pythonCmd -m pip install --upgrade pip
    & $pythonCmd -m pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "✗ Error installing Python dependencies" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error installing Python dependencies: $_" -ForegroundColor Red
    exit 1
}

# Initialize database
Write-Host ""
Write-Host "Initializing database..." -ForegroundColor Yellow
try {
    & $pythonCmd init_db.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Database initialized successfully!" -ForegroundColor Green
    } else {
        Write-Host "✗ Error initializing database" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error initializing database: $_" -ForegroundColor Red
    exit 1
}

# Setup Frontend
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Setting up Frontend (Node.js)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$frontendPath = $PSScriptRoot
Set-Location $frontendPath
Write-Host "Working directory: $frontendPath" -ForegroundColor Cyan

# Install Node.js dependencies
Write-Host ""
Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
try {
    npm install
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Node.js dependencies installed successfully!" -ForegroundColor Green
    } else {
        Write-Host "✗ Error installing Node.js dependencies" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "✗ Error installing Node.js dependencies: $_" -ForegroundColor Red
    exit 1
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Start the backend server:" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Cyan
Write-Host "   python run.py" -ForegroundColor Cyan
Write-Host "   (API will be available at http://localhost:8000)" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Start the frontend server (in a new terminal):" -ForegroundColor White
Write-Host "   npm run dev" -ForegroundColor Cyan
Write-Host "   (Frontend will be available at http://localhost:3001)" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Access the application:" -ForegroundColor White
Write-Host "   - Frontend: http://localhost:3001" -ForegroundColor Cyan
Write-Host "   - API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Note: You may need to import data (customers, inventory) separately." -ForegroundColor Yellow
Write-Host "See backend/QUICK_START.md for data import instructions." -ForegroundColor Yellow
Write-Host ""

