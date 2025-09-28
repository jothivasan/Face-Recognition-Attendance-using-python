@echo off
echo Starting Face Recognition Attendance System...
echo.
echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Starting application...
python main.py

if %errorlevel% neq 0 (
    echo.
    echo Error: Application failed to start
    echo Make sure all dependencies are installed:
    echo pip install -r requirements.txt
    echo.
    pause
)