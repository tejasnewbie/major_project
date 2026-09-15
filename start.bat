@echo off
echo ==========================================
echo    Council of Frontiers - Quick Start
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "backend\venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)

echo.
echo [1/3] Starting Backend...
echo     API will be available at http://localhost:8000
echo.

start "Council Backend" cmd /k "cd backend && venv\Scripts\activate && pip install -r requirements.txt && uvicorn app.main:app --reload"

timeout /t 3 >nul

echo [2/3] Building Docker Sandbox...
echo     Required for code execution
echo.

cd docker-sandbox
docker build -t council-sandbox . 2>nul || echo Docker image already exists or Docker not running
cd ..

timeout /t 2 >nul

echo [3/3] Starting Frontend...
echo     App will open at http://localhost:3000
echo.

start "Council Frontend" cmd /k "cd frontend && npm install && npm start"

echo.
echo ==========================================
echo    All services starting...
echo    - Backend: http://localhost:8000
echo    - Frontend: http://localhost:3000
echo    - API Docs: http://localhost:8000/docs
echo ==========================================
echo.
pause
