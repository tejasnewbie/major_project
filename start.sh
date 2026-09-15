#!/bin/bash

echo "=========================================="
echo "   Council of Frontiers - Quick Start"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Setup backend
if [ ! -d "backend/venv" ]; then
    echo "Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

echo ""
echo -e "${BLUE}[1/3] Starting Backend...${NC}"
echo "    API will be available at http://localhost:8000"
echo ""

cd backend
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

cd ..

# Start backend in background
(cd backend && source venv/bin/activate && uvicorn app.main:app --reload) &
BACKEND_PID=$!

sleep 3

echo -e "${BLUE}[2/3] Building Docker Sandbox...${NC}"
echo "    Required for code execution"
echo ""

cd docker-sandbox
docker build -t council-sandbox . 2>/dev/null || echo "Docker image already exists or Docker not running"
cd ..

sleep 2

echo ""
echo -e "${BLUE}[3/3] Starting Frontend...${NC}"
echo "    App will open at http://localhost:3000"
echo ""

# Start frontend in background
(cd frontend && npm install && npm start) &
FRONTEND_PID=$!

echo ""
echo "=========================================="
echo -e "${GREEN}All services starting...${NC}"
echo "  - Backend:  http://localhost:8000"
echo "  - Frontend: http://localhost:3000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=========================================="
echo ""

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
