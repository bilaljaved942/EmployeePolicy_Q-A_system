#!/bin/bash
# Quick Start Script for Employee Policy Q&A System (Mac/Linux)

echo ""
echo "========================================"
echo "Employee Policy Q&A System - Quick Start"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.10+ from https://www.python.org/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created!"
else
    echo "Virtual environment already exists"
fi

echo ""
echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo ""
echo "[3/5] Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[4/5] Initializing database..."
python -c "from src.models import init_db; init_db()" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Warning: Database initialization failed. Make sure PostgreSQL is running."
    echo "Please check your DATABASE_URL in .env file"
else
    echo "Database initialized successfully!"
fi

echo ""
echo "[5/5] Starting application..."
echo ""
echo "========================================"
echo "Application starting at:"
echo "http://localhost:8000"
echo "========================================"
echo ""

uvicorn app:app --reload --host 0.0.0.0 --port 8000
