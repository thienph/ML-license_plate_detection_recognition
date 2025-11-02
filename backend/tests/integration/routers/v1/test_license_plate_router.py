"""
Tests for the license plate router.
"""

import pytest


class TestLicensePlateRouter:
    def test_recognize_endpoint(self, test_client):
        """Test recognize endpoint with a real image file"""
        with open("tests/data/xemay5.jpg", "rb") as img_file:
            response = test_client.post(
                "/api/v1/license-plate/recognize",
                files={"file": ("xemay5.jpg", img_file, "image/jpeg")},
            )
        assert response.status_code == 200
        data = response.json()
        assert "detections" in data
        results = data["detections"]
        assert isinstance(results, list)
        for result in results:
            assert "plate_number" in result
            assert "confidence" in result
            assert "bbox" in result
