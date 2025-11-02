#!/bin/bash

# setup.sh - Project Setup Script
# Run this script to set up the development environment

echo "[INFO] Setting up Local Development Environment..."
echo ""

# Check if Poetry is available
if ! command -v poetry &> /dev/null
then
    echo "[ERROR] Poetry is not installed or not in PATH."
    echo "[INFO] Please install Poetry first: https://python-poetry.org/docs/#installation"
    exit 1
fi

POETRY_VERSION=$(poetry --version)
echo "[SUCCESS] Poetry found: $POETRY_VERSION"


# Create logs directory if it doesn't exist
if [ ! -d "logs" ]; then
    echo "[INFO] Creating logs directory..."
    mkdir -p logs
fi


# Install dependencies
echo "[INFO] Installing dependencies..."
poetry install

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "[SUCCESS] Setup completed successfully!"
echo ""
echo "[INFO] Available commands:"
echo "  ./scripts/run_dev.sh   - Start development server"
echo "  ./scripts/run_tests.sh - Run tests"
echo "  ./scripts/lint.sh      - Run code quality checks"
echo ""
echo "[INFO] API Documentation will be available at: http://127.0.0.1:8000/docs"
