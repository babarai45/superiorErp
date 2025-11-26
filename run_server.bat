@echo off
pause
REM If server stops, keep window open

python manage.py runserver
REM Start Django server

echo.
echo Press CTRL+C to stop the server
echo.
echo =========================================
echo   http://localhost:8000/
echo   🚀 Server will start on:
echo =========================================
echo.
echo Starting Django development server...
echo.
echo ✓ Virtual environment activated!
echo.
REM Display information

call .venv\Scripts\activate.bat
echo Activating virtual environment...
REM Activate virtual environment

)
    exit /b 1
    pause
    echo Please create it with: python -m venv .venv
    echo Error: Virtual environment not found!
if not exist ".venv\Scripts\activate.bat" (
REM Check if virtual environment exists

)
    exit /b 1
    pause
    echo Please run this from: E:\Specialization\django_Sep\superiorErp
    echo Error: manage.py not found!
if not exist "manage.py" (
REM Check if running from correct directory

echo.
echo =========================================
echo   CampusGPT - Django Development Server
echo =========================================
echo.

REM This batch file automatically starts the Django development server
REM CampusGPT - Django Server Launcher

