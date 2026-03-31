@echo off
setlocal enabledelayedexpansion

color 0A
echo.
echo ========================================
echo 🏏 CRICKET MASTER - COMPLETE SETUP
echo ========================================
echo.

REM Step 1: Check Python
echo 📦 Step 1: Checking for Python 3.8+ (64-bit)...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found in PATH
    echo.
    echo Visit: https://www.python.org/downloads/windows/
    echo Choose: Windows x86-64 executable installer
    echo ✅ Check "Add Python to PATH"
    echo.
    pause
    start https://www.python.org/downloads/windows/
    exit /b 1
)

python -c "import struct; exit(0 if struct.calcsize('P')*8 == 64 else 1)"
if errorlevel 1 (
    echo ❌ ERROR: Python must be 64-bit, not 32-bit
    echo.
    echo Please uninstall 32-bit Python and install 64-bit Python from:
    echo https://www.python.org/downloads/windows/
    echo.
    pause
    exit /b 1
)

echo ✅ Python 64-bit found
echo.

REM Step 2: Remove old venv
echo 🗑️  Step 2: Cleaning old virtual environment...
if exist .venv (
    echo   Removing .venv folder...
    rmdir /s /q .venv
    echo ✅ Old environment removed
) else (
    echo ✅ No old environment found
)
echo.

REM Step 3: Create new venv
echo 🔨 Step 3: Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment created
echo.

REM Step 4: Activate venv
echo 🚀 Step 4: Activating virtual environment...
call .venv\Scripts\activate.bat
echo ✅ Virtual environment activated
echo.

REM Step 5: Upgrade pip
echo 📦 Step 5: Upgrading pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip upgraded
echo.

REM Step 6: Install dependencies
echo 📦 Step 6: Installing dependencies (2-5 minutes)...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed
echo.

REM Step 7: Verify
echo ✔️  Step 7: Verifying installation...
python -c "import streamlit; import pandas; import numpy; print('✅ All packages imported')"
if errorlevel 1 (
    echo ❌ Verification failed
    pause
    exit /b 1
)
echo ✅ Installation verified
echo.

REM Step 8: Launch
echo 🎬 Step 8: Launching Cricket Master...
echo.
echo ⏳ Opening http://localhost:8501
echo Press Ctrl+C to stop the app
echo.
python -m streamlit run app.py

pause
