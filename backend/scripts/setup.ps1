# setup.ps1 - Project Setup Script
# Run this script to set up the development environment

Write-Host "[INFO] Setting up Local Development Environment..." -ForegroundColor Green
Write-Host ""

# Check if Poetry is available
try {
    $poetryVersion = poetry --version
    Write-Host "[SUCCESS] Poetry found: $poetryVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Poetry is not installed or not in PATH." -ForegroundColor Red
    Write-Host "[INFO] Please install Poetry first: https://python-poetry.org/docs/#installation" -ForegroundColor Red
    exit 1
}

# Create logs directory if it doesn't exist
if (-Not (Test-Path "logs")) {
    Write-Host "[INFO] Creating logs directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Name "logs" | Out-Null
}


# Install dependencies
Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
poetry install

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[SUCCESS] Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "[INFO] Available commands:" -ForegroundColor Cyan
Write-Host "  .\scripts\run_dev.ps1   - Start development server" -ForegroundColor White
Write-Host "  .\scripts\run_tests.ps1 - Run tests" -ForegroundColor White
Write-Host "  .\scripts\lint.ps1      - Run code quality checks" -ForegroundColor White
Write-Host ""
Write-Host "[INFO] API Documentation will be available at: http://127.0.0.1:8000/docs" -ForegroundColor Cyan
