# Script to run the demo application for license plate detection and recognition

# Backend - Install dependencies and run the demo application
Write-Host "[INFO] Backend - Setting up the environment..." -ForegroundColor Green

# Backend - Setup environment
Set-Location backend
.\scripts\setup.ps1
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Backend - Environment setup failed." -ForegroundColor Red
    exit 1
}
Write-Host "[SUCCESS] Backend - Environment setup completed!" -ForegroundColor Green
Write-Host "[INFO] Backend - Starting backend service..." -ForegroundColor Green
# Backend - Start service in background
Start-Process powershell -ArgumentList "-NoProfile -ExecutionPolicy Bypass -Command `".\scripts\run_dev.ps1`"" -NoNewWindow
Set-Location ..

# Health check to ensure the backend is running before opening the frontend
$counter = 0
while ( $true ) {
    try {
        Invoke-RestMethod -Uri "http://localhost:8000/api/v1/health" -Method Get -ErrorAction Stop
        break
    } catch {
        Write-Host "[INFO] Backend - Waiting for the backend service to start..." -ForegroundColor Yellow
        Start-Sleep -Seconds 3
    }
    $counter++
    if ($counter -ge 20) {
        Write-Host "[ERROR] Backend - Backend service failed to start within the expected time." -ForegroundColor Red
        exit 1
    }
}

Write-Host "[SUCCESS] Backend - Service started!" -ForegroundColor Green
Write-Host "[INFO] You can now access the API doc at http://localhost:8000" -ForegroundColor Green

Write-Host "[INFO] Frontend - Opening the demo page..." -ForegroundColor Green
# Open the html file for demo
Start-Process ".\frontend\index.html"
