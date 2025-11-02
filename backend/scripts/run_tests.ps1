# run_tests.ps1 - Test Runner
# Run this script to execute all tests

Write-Host "[INFO] Running Tests..." -ForegroundColor Green
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


# Install dependencies including dev dependencies
Write-Host "[INFO] Installing test dependencies..." -ForegroundColor Yellow
poetry install

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to install dependencies" -ForegroundColor Red
    exit 1
}


# Run tests
Write-Host "[INFO] Running tests..." -ForegroundColor Green
poetry run pytest -v

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[SUCCESS] All tests passed!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[ERROR] Some tests failed!" -ForegroundColor Red
    exit 1
}
