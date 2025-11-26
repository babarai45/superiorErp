#!/bin/bash
# CampusGPT - Django Server Launcher (Linux/Mac)
# This script automatically starts the Django development server

echo ""
echo "========================================="
echo "  CampusGPT - Django Development Server"
echo "========================================="
echo ""

# Check if running from correct directory
if [ ! -f "manage.py" ]; then
    echo "Error: manage.py not found!"
    echo "Please run this from: E:\Specialization\django_Sep\superiorErp"
    exit 1
fi

# Check if virtual environment exists
if [ ! -f ".venv/bin/activate" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please create it with: python -m venv .venv"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Display information
echo ""
echo "✓ Virtual environment activated!"
echo ""
echo "Starting Django development server..."
echo ""
echo "========================================="
echo "  🚀 Server will start on:"
echo "  http://localhost:8000/"
echo "========================================="
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Start Django server
python manage.py runserver

