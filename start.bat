@echo off
REM AI Hiring Agent - Full Stack Startup Script (Windows)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║          AI HIRING AGENT - STARTUP SCRIPT                 ║
echo ║                    (Windows)                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Set project directory
setlocal enabledelayedexpansion
set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo [*] Project Directory: %PROJECT_DIR%
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo [*] Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/Update dependencies
echo [*] Installing dependencies...
pip install -q -r requirements.txt

REM Check .env file
echo [*] Checking .env configuration...
if not exist ".env" (
    echo [!] ERROR: .env file not found!
    echo Please create .env file with:
    echo   GROQ_API_KEY=your_actual_key
    pause
    exit /b 1
)

findstr /M "GROQ_API_KEY" .env > nul
if errorlevel 1 (
    echo [!] ERROR: GROQ_API_KEY not found in .env!
    echo Please add GROQ_API_KEY=your_actual_key to .env
    pause
    exit /b 1
)

echo [✓] .env configured
echo.

REM Run tests
echo [*] Running tests...
python test_context_engineering.py > nul 2>&1
if errorlevel 1 (
    echo [!] Tests failed
    python test_context_engineering.py
    pause
    exit /b 1
)

echo [✓] All tests passed
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║              STARTUP OPTIONS                              ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Option 1: Run backend and frontend together
echo Option 2: Run backend only (you run frontend separately)
echo Option 3: Run frontend only (assumes backend running)
echo.

set /p option="Choose option (1, 2, or 3): "

if "%option%"=="1" (
    echo.
    echo [*] Starting backend on port 8000...
    start "AI Hiring Agent Backend" python backend/main.py
    
    timeout /t 3 /nobreak
    
    echo [✓] Backend started
    echo.
    echo [*] Starting frontend on port 8501...
    timeout /t 2 /nobreak
    streamlit run frontend/app.py
    
) else if "%option%"=="2" (
    echo.
    echo [*] Starting backend on port 8000...
    python backend/main.py
    
) else if "%option%"=="3" (
    echo.
    echo [*] Starting frontend on port 8501...
    echo [!] Make sure backend is running on port 8000
    streamlit run frontend/app.py
    
) else (
    echo [!] Invalid option
    pause
    exit /b 1
)

echo.
echo [✓] Done!
pause
