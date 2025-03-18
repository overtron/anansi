@echo off
REM Run both the backend and frontend in development mode

REM Check if OpenAI API key is provided
if "%~1"=="" (
    echo Error: OpenAI API key is required
    echo Usage: run_dev.bat YOUR_OPENAI_API_KEY
    exit /b 1
)

REM Set OpenAI API key
set OPENAI_API_KEY=%~1

REM Check if backend dependencies are installed
echo Checking backend dependencies...
cd backend
if not exist "requirements.txt" (
    echo Error: Backend requirements.txt not found
    exit /b 1
)

REM Check if virtual environment exists, if not create one
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        exit /b 1
    )
)

REM Activate virtual environment and install dependencies
echo Installing backend dependencies...
call venv\Scripts\activate
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install backend dependencies
    exit /b 1
)

REM Start the backend
echo Starting backend server...
start cmd /k "venv\Scripts\activate && python run.py"
cd ..

REM Wait for backend to start
echo Waiting for backend to start...
timeout /t 5 /nobreak > nul

REM Check if frontend dependencies are installed
echo Checking frontend dependencies...
cd frontend
if not exist "node_modules" (
    echo Installing frontend dependencies...
    call npm install
    if errorlevel 1 (
        echo Error: Failed to install frontend dependencies
        exit /b 1
    )
)

REM Start the frontend
echo Starting frontend development server...
start cmd /k "npm start"
cd ..

REM Wait for frontend to start
echo Waiting for frontend to start...
timeout /t 10 /nobreak > nul

echo.
echo Development environment is running!
echo - Backend: http://localhost:8000
echo - Frontend: http://localhost:3000
echo.
echo Close the command windows to stop the servers

REM Keep this window open
pause
