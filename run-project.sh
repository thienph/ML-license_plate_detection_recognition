#!/bin/bash
# Script to run the demo application for license plate detection and recognition

# Backend - Install dependencies and run the demo application
echo "[INFO] Backend - Setting up the environment..."

# Backend - Setup environment
cd backend
./scripts/setup.sh
if [ $? -ne 0 ]; then
    echo "[ERROR] Backend - Environment setup failed."
    exit 1
fi
echo "[SUCCESS] Backend - Environment setup completed!"
echo "[INFO] Backend - Starting backend service..."
# Backend - Start service in background
./scripts/run_dev.sh &
cd ..

# Health check to ensure the backend is running before opening the frontend
counter=0
while true; do
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/v1/health | grep -q "200"; then
        break
    fi
    echo "[INFO] Backend - Waiting for the backend service to start..."
    sleep 3
    counter=$((counter + 1))
    if [ $counter -ge 20 ]; then
        echo "[ERROR] Backend - Backend service failed to start within the expected time."
        exit 1
    fi
done

echo "[SUCCESS] Backend - Service started!"
echo "[INFO] You can now access the API doc at http://localhost:8000"

echo "[INFO] Frontend - Opening the demo page..."
# Open the html file for demo
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "./frontend/index.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    xdg-open "./frontend/index.html"
else
    echo "[WARN] Unable to automatically open browser. Please open ./frontend/index.html manually."
fi
