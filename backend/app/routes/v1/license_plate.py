"""
License Plate Recognition API Endpoints - Version 1
"""

from fastapi import APIRouter, File, UploadFile, HTTPException, status
from pathlib import Path
import time
import logging

from app.schemas.license_plate import (
    RecognitionResponse,
    ErrorResponse,
    HealthResponse,
    LicensePlateCharactersRecognition,
)
from app.services.license_plate_service import get_license_plate_service
from app.core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)



@router.post(
    "/recognize",
    response_model=RecognitionResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Recognize License Plate",
    description="Upload an image to detect and recognize license plates",
)
async def recognize_license_plate(
    file: UploadFile = File(..., description="Image file containing license plate")
):
    """
    Receives an image file, performs license plate detection and recognition.

    The API will:
    1. Validate the uploaded file
    2. Detect license plates using YOLOv11
    3. Recognize characters using EasyOCR
    4. Return all detected license plates with confidence scores
    """
    start_time = time.time()

    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}",
            )

        # Read file content
        contents = await file.read()

        # Validate file size
        if len(contents) > settings.MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {settings.MAX_IMAGE_SIZE / (1024*1024)}MB",
            )

        # Get service instance
        service = get_license_plate_service()

        # Process image
        detections = service.process_image(contents)

        processing_time = time.time() - start_time

        if not detections:
            return RecognitionResponse(
                success=True,
                message="No license plates detected in the image",
                detections=[],
                processing_time=processing_time,
            )

        return RecognitionResponse(
            success=True,
            message=f"Successfully detected {len(detections)} license plate(s)",
            detections=detections,
            processing_time=processing_time,
        )

    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the image",
        )
