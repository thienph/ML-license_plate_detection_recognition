#!/bin/bash

# run_dev.sh - Development Server Launcher
# Run this script to start the FastAPI development server

echo "[INFO] Starting API Development Server..."
echo ""


# Check if Poetry is available
if ! command -v poetry &> /dev/null
then
    echo "[ERROR] Poetry is not installed or not in PATH."
    echo "[INFO] Please install Poetry first."
    exit 1
fi

POETRY_VERSION=$(poetry --version)
echo "[SUCCESS] Poetry found: $POETRY_VERSION"


# Install dependencies if needed
echo "[INFO] Checking dependencies..."
poetry install

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

# Start the development server
echo "[INFO] Starting development server..."
echo "[INFO] Server will be available at: http://127.0.0.1:8000"
echo "[INFO] API docs will be available at: http://127.0.0.1:8000/api/v1/docs"
echo ""
echo "[INFO] Press Ctrl+C to stop the server"
echo ""

poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
