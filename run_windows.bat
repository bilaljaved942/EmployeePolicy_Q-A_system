@echo off
REM Quick Start Script for Employee Policy Q&A System (Windows)

echo.
echo ========================================
echo Employee Policy Q&A System - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/5] Initializing database...
python -c "from src.models import init_db; init_db()" >nul 2>&1
if errorlevel 1 (
    echo Warning: Database initialization failed. Make sure PostgreSQL is running.
    echo Please check your DATABASE_URL in .env file
) else (
    echo Database initialized successfully!
)

echo.
echo [5/5] Starting application...
echo.
echo ========================================
echo Application starting at:
echo http://localhost:8000
echo ========================================
echo.

uvicorn app:app --reload --host 0.0.0.0 --port 8000

pause
