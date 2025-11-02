#!/bin/bash

# run_tests.sh - Test Runner
# Run this script to execute all tests

echo "[INFO] Running Tests..."
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


# Install dependencies including dev dependencies
echo "[INFO] Installing test dependencies..."
poetry install

if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi


# Run tests
echo "[INFO] Running tests..."
poetry run pytest -v

if [ $? -eq 0 ]; then
    echo ""
    echo "[SUCCESS] All tests passed!"
else
    echo ""
    echo "[ERROR] Some tests failed!"
    exit 1
fi
