#!/bin/bash

# Start Emergency Response AI System
# This script starts both the backend API server and frontend web server

echo "🚀 Starting Emergency Response AI System..."

# Kill any existing servers on ports 8000 and 3000
echo "Stopping any existing servers..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

# Start backend server
echo "Starting backend API server on port 8000..."
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend server
echo "Starting frontend web server on port 3000..."
cd ../frontend
python3 -m http.server 3000 &
FRONTEND_PID=$!

# Wait a bit for frontend to start
sleep 2

echo ""
echo "✅ Emergency Response AI System is running!"
echo ""
echo "🔧 Backend API:  http://localhost:8000"
echo "🌐 Frontend UI:  http://localhost:3000/demo.html"
echo ""
echo "📊 API Status:   http://localhost:8000/health"
echo "🧪 Demo Mode:    Active (safe for testing)"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "✅ All servers stopped"
    exit 0
}

# Set trap to cleanup on script termination
trap cleanup INT TERM

# Keep script running
wait
