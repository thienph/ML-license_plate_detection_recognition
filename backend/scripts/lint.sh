#!/bin/bash

# lint.sh - Code Quality Checker
# Run this script to check code quality and format code

echo "[INFO] Running Code Quality Checks..."
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

# Install dependencies
echo "[INFO] Installing dependencies..."
poetry install

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

# Format code with Black
echo "[INFO] Formatting code with Black..."
poetry run black .

# Check code with Ruff
echo "[INFO] Linting code with Ruff..."
poetry run ruff check .
poetry run black . --check

# Type checking with MyPy
echo "[INFO] Type checking with MyPy..."
poetry run mypy app/

echo ""
echo "[SUCCESS] Code quality check completed!"
