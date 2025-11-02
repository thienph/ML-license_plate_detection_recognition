"""
Tests for the health check router.
"""

import pytest


class TestHealthRouter:
    def test_health_check(self, test_client):
        """Test health check endpoint"""
        response = test_client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "model_loaded" in data
        assert "ocr_ready" in data
