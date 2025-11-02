"""
Core configuration module
"""

from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_TITLE: str = "License Plate Recognition API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for detecting and recognizing Vietnamese license plates"

    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:5173",
        "null",  # Allow file:// protocol (opening HTML directly)
        "*",  # Allow all origins for development
    ]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Model Paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MODEL_PATH: str = str(BASE_DIR / "models" / "lp_detection.pt")

    # Model Settings
    YOLO_CONF_THRESHOLD: float = 0.25
    YOLO_IOU_THRESHOLD: float = 0.45

    # OCR Settings
    OCR_LANGUAGES: List[str] = ["en"]
    OCR_GPU: bool = False

    # Image Processing
    MAX_IMAGE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".bmp"}

    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
