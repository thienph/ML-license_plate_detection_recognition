# Backend Service

This directory contains the source code for the backend service of License Plate Detection and Recognition.

## Project Structure

```
├── app/                   # Application code
│   ├── main.py            # FastAPI app entry point
│   ├── core/              # Core configurations
│   ├── models/            # Trained ML models
│   ├── routes/v1/         # API endpoints (versioned)
│   ├── schemas/           # Pydantic models
│   ├── services/          # Business logic
│   └── utils/             # Utility functions
├── deploy/                # Deployment script and configurations
├── tests/                 # Test cases (unit, integration, e2e)
├── scripts/               # Development scripts
└── .env                   # Environment configuration
```

## Technology Stack

- FastAPI 0.115.0
- Python 3.11
- Poetry - Dependency management
- Pydantic - Data validation and settings

### Setup & Development

#### On MacOS

```bash
# One-time setup
./scripts/setup.sh

# Start development server
./scripts/run_dev.sh

# Run tests and code quality checks
./scripts/run_tests.sh
./scripts/lint.sh
```

#### On Windows

```powershell
# One-time setup
.\scripts\setup.ps1

# Start development server
.\scripts\run_dev.ps1

# Run tests and code quality checks
.\scripts\run_tests.ps1
.\scripts\lint.ps1
```

### Model Management
Trained models are stored in the `app/models/` directory. Please copy your trained model files into this directory before starting the server.

### API Documentation
Once the development server is running:
- API Docs (Swagger): http://127.0.0.1:8000/api/v1/docs
- Health Check: http://127.0.0.1:8000/api/v1/health

## Dependency Management

### Poetry (Single Source of Truth)
We use Poetry exclusively for dependency management:

```powershell
# Install dependencies
poetry install

# Add new package
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Update dependencies
poetry update

# Generate lock file
poetry lock
```

## Deployment

### Docker Build & Run

```
docker build -t license-plate-api:latest .
```
