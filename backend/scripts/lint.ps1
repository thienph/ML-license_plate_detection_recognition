# lint.ps1 - Code Quality Checker
# Run this script to check code quality and format code

Write-Host "[INFO] Running Code Quality Checks..." -ForegroundColor Green
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


# Install dependencies
Write-Host "[INFO] Installing dependencies..." -ForegroundColor Yellow
poetry install

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}


# Format code with Black
Write-Host "[INFO] Formatting code with Black..." -ForegroundColor Cyan
poetry run black .

# Check code with Ruff
Write-Host "[INFO] Linting code with Ruff..." -ForegroundColor Cyan
poetry run ruff check .
poetry run black . --check

# Type checking with MyPy
Write-Host "[INFO] Type checking with MyPy..." -ForegroundColor Cyan
poetry run mypy app/

Write-Host ""
Write-Host "[SUCCESS] Code quality check completed!" -ForegroundColor Green
