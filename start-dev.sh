#!/bin/bash

# IELTS Writing Feedback AI - Development Server Startup Script

echo "🚀 Starting IELTS Writing Feedback AI Development Servers"
echo "=================================================="

# Check if backend dependencies are installed
if [ ! -d "backend/.venv" ]; then
    echo "❌ Backend not set up. Please run 'python setup.py' first"
    exit 1
fi

# Check if frontend dependencies are installed  
if [ ! -d "frontend/node_modules" ]; then
    echo "❌ Frontend not set up. Please run 'python setup.py' first"
    exit 1
fi

# Function to kill background processes on exit
cleanup() {
    echo "🛑 Stopping development servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal trap for cleanup
trap cleanup SIGINT SIGTERM

# Start backend server
echo "🔧 Starting Backend (FastAPI)..."
cd backend
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend server
echo "🎨 Starting Frontend (React + Vite)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Development servers started!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for background processes
wait
