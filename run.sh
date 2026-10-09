#!/usr/bin/env bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "========================================================"
echo "  Starting VeriText Turnitin AI Detector (EN / EL)"
echo "========================================================"

PYTHON_CMD="C:/Users/JohnJohn/AppData/Local/hermes/hermes-agent/venv/Scripts/python.exe"
if [ ! -f "$PYTHON_CMD" ]; then
    if command -v python3 &>/dev/null; then
        PYTHON_CMD="python3"
    else
        PYTHON_CMD="python"
    fi
fi

echo "Using Python: $PYTHON_CMD"
echo "Launching server at http://127.0.0.1:8000 ..."

# Attempt to open browser across platforms
if command -v xdg-open &>/dev/null; then
    xdg-open "http://127.0.0.1:8000" &
elif command -v open &>/dev/null; then
    open "http://127.0.0.1:8000" &
fi

"$PYTHON_CMD" -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
