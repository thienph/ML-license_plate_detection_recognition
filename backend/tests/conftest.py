"""
Pytest configuration and fixtures for the test suite.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.main import app

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def test_client() -> TestClient:
    """Fixture for FastAPI test client."""
    return TestClient(app)
