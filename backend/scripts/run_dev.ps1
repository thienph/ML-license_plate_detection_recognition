# run_dev.ps1 - Development Server Launcher
# Run this script to start the FastAPI development server

Write-Host "[INFO] Starting API Development Server..." -ForegroundColor Green
Write-Host ""


# Check if Poetry is available
try {
    $poetryVersion = poetry --version
    Write-Host "[SUCCESS] Poetry found: $poetryVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Poetry is not installed or not in PATH." -ForegroundColor Red
    Write-Host "[INFO] Please install Poetry first." -ForegroundColor Red
    exit 1
}


# Install dependencies if needed
Write-Host "[INFO] Checking dependencies..." -ForegroundColor Yellow
poetry install

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

# Start the development server
Write-Host "[INFO] Starting development server..." -ForegroundColor Green
Write-Host "[INFO] Server will be available at: http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host "[INFO] API docs will be available at: http://127.0.0.1:8000/api/v1/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "[INFO] Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

poetry run uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
