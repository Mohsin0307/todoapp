#!/bin/bash
# Setup and Run Script for Phase III AI Chatbot Backend

echo "=================================="
echo "Phase III AI Chatbot - Backend Setup"
echo "=================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Creating new venv..."
    python -m venv venv
    echo "✅ Created venv"
fi

# Activate venv
echo "Activating virtual environment..."
source venv/Scripts/activate || source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo "=================================="
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  WARNING: .env file not found!"
    echo ""
    echo "To enable Claude AI:"
    echo "1. Copy .env.example to .env:"
    echo "   cp .env.example .env"
    echo ""
    echo "2. Add your Anthropic API key:"
    echo "   ANTHROPIC_API_KEY=sk-ant-api03-your-key-here"
    echo ""
    echo "3. Get key from: https://console.anthropic.com/settings/keys"
    echo ""
    echo "Press Ctrl+C to stop and configure, or wait 5 seconds to start anyway..."
    sleep 5
fi

echo ""
echo "Starting FastAPI server on port 8000..."
echo ""
echo "=================================="
echo "Server will start in 2 seconds..."
echo "Press Ctrl+C to cancel"
echo "=================================="
sleep 2

echo ""
python -m uvicorn main:app --reload --port 8000
