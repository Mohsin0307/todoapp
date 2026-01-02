#!/bin/bash
# Install backend dependencies in venv

echo "Installing backend dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed successfully!"
echo ""
echo "To activate venv and run server:"
echo "  source venv/Scripts/activate  # or venv\\Scripts\\activate"
echo "  python -m uvicorn main:app --reload --port 8000"
