@echo off
echo 🏏 Cricket Master Launcher
echo.

REM Ensure venv activated
call .venv\Scripts\activate.bat

REM Check for 64-bit Python
python -c "import sys; sys.exit(0 if sys.maxsize > 2**32 else 1)"
if errorlevel 1 (
    echo ERROR: 64-bit Python is required to run this app.
    echo Please install Python 3.8+ 64-bit and recreate the virtual environment.
    pause
    exit /b 1
)

REM Install minimal deps
python -m pip install --no-cache-dir requests pandas==1.3.5 numpy==1.21.6 scikit-learn==1.0.2 cachetools pytz toml

REM Install streamlit with dependencies
python -m pip install streamlit==1.10.0

REM Launch app
echo.
echo 🚀 Launching app at http://localhost:8501
python -m streamlit run app.py --server.headless true

pause
