"""
Service for license plate detection and recognition
"""

import cv2
import numpy as np
import easyocr
import re
from typing import List, Tuple, Optional
from pathlib import Path
from ultralytics import YOLO
import logging

from app.core.config import settings
from app.schemas.license_plate import LicensePlateCharactersRecognition

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LicensePlateService:
    """Service class for license plate detection and recognition"""

    def __init__(self):
        """Initialize the service with YOLO model and EasyOCR reader"""
        self.model = None
        self.reader = None
        self._load_model()
        self._load_ocr()

    def _load_model(self):
        """Load the YOLO model"""
        try:
            model_path = Path(settings.MODEL_PATH)
            if not model_path.exists():
                logger.error(f"Model file not found at {model_path}")
                raise FileNotFoundError(f"Model file not found at {model_path}")

            self.model = YOLO(str(model_path))
            logger.info(f"YOLO model loaded successfully from {model_path}")
        except Exception as e:
            logger.error(f"Error loading YOLO model: {str(e)}")
            raise

    def _load_ocr(self):
        """Load the EasyOCR reader"""
        try:
            self.reader = easyocr.Reader(settings.OCR_LANGUAGES, gpu=settings.OCR_GPU)
            logger.info("EasyOCR reader loaded successfully")
        except Exception as e:
            logger.error(f"Error loading EasyOCR: {str(e)}")
            raise

    def detect_license_plates(self, image: np.ndarray) -> List[dict]:
        """
        Detect license plates in an image using YOLO

        Args:
            image: Input image as numpy array

        Returns:
            List of detections with bounding boxes and confidence scores
        """
        try:
            results = self.model.predict(
                image,
                conf=settings.YOLO_CONF_THRESHOLD,
                iou=settings.YOLO_IOU_THRESHOLD,
                verbose=False,
            )

            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    # Get bounding box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = float(box.conf[0].cpu().numpy())

                    detections.append(
                        {
                            "bbox": [float(x1), float(y1), float(x2), float(y2)],
                            "confidence": confidence,
                        }
                    )

            return detections
        except Exception as e:
            logger.error(f"Error in license plate detection: {str(e)}")
            raise

    def preprocess_plate_image(self, plate_img: np.ndarray) -> np.ndarray:
        """
        Preprocess the cropped license plate image for better OCR results

        Args:
            plate_img: Cropped license plate image

        Returns:
            Preprocessed image
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

            # Apply bilateral filter to reduce noise while keeping edges sharp
            denoised = cv2.bilateralFilter(gray, 11, 17, 17)

            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )

            # Apply morphological operations to clean up
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            return morph
        except Exception as e:
            logger.error(f"Error in image preprocessing: {str(e)}")
            return plate_img

    def recognize_text(self, plate_img: np.ndarray) -> Tuple[str, float]:
        """
        Recognize text from a license plate image using EasyOCR

        Args:
            plate_img: Cropped and preprocessed license plate image

        Returns:
            Tuple of (recognized_text, confidence)
        """
        try:
            # Try OCR on preprocessed image
            preprocessed = self.preprocess_plate_image(plate_img)
            results = self.reader.readtext(preprocessed)

            if not results:
                # If no results, try on original image
                results = self.reader.readtext(plate_img)

            if not results:
                return "", 0.0

            # Combine all detected text and get average confidence
            text_parts = []
            confidences = []

            for bbox, text, conf in results:
                text_parts.append(text)
                confidences.append(conf)

            # Join all text parts
            full_text = "".join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

            # Clean and format the text
            cleaned_text = self.clean_plate_text(full_text)

            return cleaned_text, avg_confidence
        except Exception as e:
            logger.error(f"Error in text recognition: {str(e)}")
            return "", 0.0

    def clean_plate_text(self, text: str) -> str:
        """
        Clean and format the recognized license plate text

        Args:
            text: Raw OCR text

        Returns:
            Cleaned and formatted text
        """
        # Remove spaces and convert to uppercase
        text = text.replace(" ", "").upper()

        # Remove special characters except hyphens
        text = re.sub(r"[^A-Z0-9-]", "", text)

        # Common OCR corrections
        replacements = {
            "O": "0",
            "I": "1",
            "S": "5",
            "Z": "2",
            "B": "8",
        }

        # Apply replacements for numeric positions (typically after the first 2-3 characters)
        if len(text) > 3:
            # Keep first part (location code) as letters
            prefix = text[:2]
            # Convert remaining to numbers with corrections
            suffix = text[2:]
            for old, new in replacements.items():
                suffix = suffix.replace(old, new)
            text = prefix + suffix

        return text

    def process_image(self, image_bytes: bytes) -> List[LicensePlateCharactersRecognition]:
        """
        Process an image to detect and recognize license plates

        Args:
            image_bytes: Image file as bytes

        Returns:
            List of LicensePlateDetection objects
        """
        try:
            # Decode image
            nparr = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if image is None:
                raise ValueError("Failed to decode image")

            # Detect license plates
            detections = self.detect_license_plates(image)

            results = []
            for detection in detections:
                bbox = detection["bbox"]
                x1, y1, x2, y2 = map(int, bbox)

                # Crop the license plate region
                plate_img = image[y1:y2, x1:x2]

                if plate_img.size == 0:
                    continue

                # Recognize text
                plate_text, ocr_confidence = self.recognize_text(plate_img)

                if plate_text:
                    # Combine detection and OCR confidence
                    combined_confidence = (detection["confidence"] + ocr_confidence) / 2

                    results.append(
                        LicensePlateCharactersRecognition(
                            plate_number=plate_text,
                            confidence=combined_confidence,
                            bbox=bbox,
                        )
                    )
            print(f"Results: {results}")
            return results
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise

    def is_ready(self) -> Tuple[bool, bool]:
        """
        Check if the service is ready

        Returns:
            Tuple of (model_loaded, ocr_ready)
        """
        return self.model is not None, self.reader is not None


# Singleton instance
_service_instance: Optional[LicensePlateService] = None


def get_license_plate_service() -> LicensePlateService:
    """
    Get or create the singleton instance of LicensePlateService

    Returns:
        LicensePlateService instance
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = LicensePlateService()
    return _service_instance
