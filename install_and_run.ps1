# 🏏 CRICKET MASTER - COMPLETE SETUP SCRIPT
# Installs Python 3.12, creates virtual environment, installs dependencies, and runs the app

Write-Host "🏏 Cricket Master - Complete Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check and install Python 3.12 if not found
Write-Host "📦 Step 1: Checking for Python 3.12..." -ForegroundColor Yellow
$pythonFound = $false
try {
    $pythonVersion = & python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
    
    # Check if 64-bit
    $is64bit = & python -c "import struct; import sys; sys.exit(0 if struct.calcsize('P')*8 == 64 else 1)"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Using 64-bit Python" -ForegroundColor Green
        $pythonFound = $true
    } else {
        Write-Host "⚠️  Python is 32-bit, need to install 64-bit version" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Python not found or not in PATH" -ForegroundColor Red
}

if (-not $pythonFound) {
    Write-Host ""
    Write-Host "📥 Installing Python 3.12 64-bit..." -ForegroundColor Yellow
    Write-Host "Visit: https://www.python.org/downloads/windows/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Installation steps:" -ForegroundColor Yellow
    Write-Host "  1. Click 'Windows installer (64-bit)'" -ForegroundColor Gray
    Write-Host "  2. ✅ Check 'Add Python to PATH'" -ForegroundColor Gray
    Write-Host "  3. Click 'Install Now'" -ForegroundColor Gray
    Write-Host "  4. Wait for completion" -ForegroundColor Gray
    Write-Host "  5. Click 'Disable path length limit' (optional)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "After installing Python, re-run this script." -ForegroundColor Cyan
    Read-Host "Press Enter to open Python download page"
    Start-Process "https://www.python.org/downloads/windows/"
    exit
}

# Step 2: Remove old virtual environment
Write-Host ""
Write-Host "🗑️  Step 2: Cleaning old virtual environment..." -ForegroundColor Yellow
$venvPath = ".\.venv"
if (Test-Path $venvPath) {
    Write-Host "  Removing $venvPath..." -ForegroundColor Gray
    Remove-Item -Recurse -Force $venvPath -ErrorAction SilentlyContinue
    Write-Host "✅ Removed old environment" -ForegroundColor Green
} else {
    Write-Host "✅ No old environment to remove" -ForegroundColor Green
}

# Step 3: Create new virtual environment
Write-Host ""
Write-Host "🔨 Step 3: Creating new virtual environment..." -ForegroundColor Yellow
& python -m venv .venv
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Step 4: Activate virtual environment
Write-Host ""
Write-Host "🚀 Step 4: Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green

# Step 5: Upgrade pip
Write-Host ""
Write-Host "📦 Step 5: Upgrading pip..." -ForegroundColor Yellow
& python -m pip install --upgrade pip --quiet
Write-Host "✅ pip upgraded" -ForegroundColor Green

# Step 6: Install dependencies
Write-Host ""
Write-Host "📦 Step 6: Installing project dependencies..." -ForegroundColor Yellow
Write-Host "  This may take 2-5 minutes..." -ForegroundColor Gray
& python -m pip install -r requirements.txt
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Step 7: Verify installation
Write-Host ""
Write-Host "✔️  Step 7: Verifying installation..." -ForegroundColor Yellow
& python -c "import streamlit; import pandas; import numpy; print('✅ All packages imported successfully')" 
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Installation verified" -ForegroundColor Green
} else {
    Write-Host "❌ Verification failed" -ForegroundColor Red
    exit 1
}

# Step 8: Launch app
Write-Host ""
Write-Host "🎬 Step 8: Launching Cricket Master app..." -ForegroundColor Yellow
Write-Host "⏳ This will open in your browser at http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the app" -ForegroundColor Yellow
Write-Host ""

& python -m streamlit run app.py
