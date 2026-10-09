@echo off
title VeriText Turnitin AI & Similarity Detector
echo ========================================================
echo   Starting VeriText Turnitin AI Detector (EN / EL)
echo ========================================================
cd /d "%~dp0"

set "PYTHON_CMD=C:\Users\JohnJohn\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
if not exist "%PYTHON_CMD%" (
    set "PYTHON_CMD=python"
)

echo Using Python: %PYTHON_CMD%
echo Launching server at http://127.0.0.1:8000 ...

start "" "http://127.0.0.1:8000"

"%PYTHON_CMD%" -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
pause
