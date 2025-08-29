@echo off
echo 🚀 LinkedIn Post Generator - Quick Start
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting the application...
echo 📖 API Documentation: http://localhost:8000/docs
echo 🌐 Web Interface: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py

pause
