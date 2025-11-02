"""
Health Check API Endpoint - Version 1
"""

from fastapi import APIRouter, HTTPException, status
import logging

from app.schemas.license_plate import HealthResponse
from app.services.license_plate_service import get_license_plate_service

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check if the service and models are ready",
)
async def health_check():
    """
    Health check endpoint to verify service status, including ML models.
    """
    try:
        service = get_license_plate_service()
        model_loaded, ocr_ready = service.is_ready()

        if model_loaded and ocr_ready:
            return HealthResponse(
                status="healthy", model_loaded=model_loaded, ocr_ready=ocr_ready
            )
        else:
            # Still return 200 OK but with a degraded status
            return HealthResponse(
                status="degraded", model_loaded=model_loaded, ocr_ready=ocr_ready
            )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service is not available",
        )
