"""
Pydantic schemas for request and response models
"""

from pydantic import BaseModel, Field
from typing import Optional, List



class LicensePlateCharactersRecognition(BaseModel):
    """Schema for recognized characters on a license plate"""
    plate_number: str = Field(..., description="Recognized license plate number")
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Recognition confidence score"
    )
    bbox: List[float] = Field(
        ..., description="Bounding box coordinates [x1, y1, x2, y2]"
    )



class RecognitionResponse(BaseModel):
    """Schema for license plate recognition response"""

    success: bool = Field(..., description="Whether the recognition was successful")
    message: str = Field(..., description="Status message")
    detections: List[LicensePlateCharactersRecognition] = Field(
        default_factory=list, description="List of recognized license plates"
    )
    processing_time: float = Field(..., description="Processing time in seconds")


class ErrorResponse(BaseModel):
    """Schema for error responses"""

    success: bool = Field(default=False, description="Always False for errors")
    message: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error")


class HealthResponse(BaseModel):
    """Schema for health check response"""

    status: str = Field(..., description="Service status")
    model_loaded: bool = Field(..., description="Whether the YOLO model is loaded")
    ocr_ready: bool = Field(..., description="Whether OCR is ready")
