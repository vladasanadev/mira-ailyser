#!/bin/bash

# Mira AI CV Analyzer - Development Startup Script
echo "🚀 Starting Mira AI CV Analyzer Development Environment"
echo "=================================================="

# Check if .env exists in backend
if [ ! -f "backend/.env" ]; then
    echo "❌ Error: backend/.env file not found"
    echo "Please create backend/.env with your Weaviate and OpenAI credentials"
    echo ""
    echo "Required environment variables:"
    echo "WEAVIATE_URL=your_weaviate_cluster_url"
    echo "WEAVIATE_API_KEY=your_weaviate_api_key"
    echo "OPEN_AI_API=your_openai_api_key"
    exit 1
fi

# Check if Python dependencies are installed
echo "📦 Checking Python dependencies..."
cd backend
if ! python -c "import flask, weaviate, pypdf" 2>/dev/null; then
    echo "🔧 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Start backend server in background
echo "🐍 Starting Python Flask API server on port 5000..."
python api_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

cd ..

# Check if Node dependencies are installed
echo "📦 Checking Node.js dependencies..."
if [ ! -d "node_modules" ]; then
    echo "🔧 Installing Node.js dependencies..."
    npm install
fi

# Start frontend server
echo "⚡ Starting Next.js frontend server..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting up!"
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "🔌 Backend API: http://localhost:5000"
echo ""
echo "📝 To test the API:"
echo "   curl http://localhost:5000/health"
echo ""
echo "🛑 To stop both servers: Press Ctrl+C"
echo ""

# Function to cleanup when script is terminated
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set trap to cleanup on script termination
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 