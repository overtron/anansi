#!/bin/bash
# Run both the backend and frontend in development mode

# Check if OpenAI API key is provided
if [ -z "$1" ]; then
    echo "Error: OpenAI API key is required"
    echo "Usage: ./run_dev.sh YOUR_OPENAI_API_KEY"
    exit 1
fi

# Set OpenAI API key
export OPENAI_API_KEY="$1"

# Function to kill background processes on exit
cleanup() {
    echo "Stopping all processes..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap to call cleanup function on exit
trap cleanup EXIT INT TERM

# Check if backend dependencies are installed
echo "Checking backend dependencies..."
cd backend
if [ ! -f "requirements.txt" ]; then
    echo "Error: Backend requirements.txt not found"
    exit 1
fi

# Check if virtual environment exists, if not create one
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment and install dependencies
echo "Installing backend dependencies..."
source venv/bin/activate || source venv/Scripts/activate
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install backend dependencies"
    exit 1
fi

# Start the backend
echo "Starting backend server..."
python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Check if backend started successfully
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Error: Backend failed to start"
    exit 1
fi

# Check if frontend dependencies are installed
echo "Checking frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install frontend dependencies"
        exit 1
    fi
fi

# Start the frontend
echo "Starting frontend development server..."
npm start &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 10

# Check if frontend started successfully
if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Error: Frontend failed to start"
    exit 1
fi

echo ""
echo "Development environment is running!"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to press Ctrl+C
wait
