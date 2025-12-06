@echo off
echo Starting DeepAgents Research Assistant...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing/updating dependencies...
where uv >nul 2>&1 && (
    uv pip install -r requirements.txt --quiet
) || (
    echo uv not found, using pip...
    pip install -r requirements.txt --quiet
)
echo.

REM Check for .env file
if not exist ".env" (
    echo Warning: .env file not found!
    echo Please copy .env.example to .env and add your API key.
    echo.
    pause
    exit /b 1
)

REM Run Streamlit on port 8502 (in case 8501 is already in use)
echo Starting Streamlit application on http://localhost:8502
echo.
streamlit run app.py --server.port 8502

pause
