"""
Configuration settings for the Deepfake Detection System
"""

import os
from pathlib import Path

# Base directories
BASE_DIR = Path(__file__).resolve().parent
MODELS_DIR = BASE_DIR / "models"
UPLOADS_DIR = BASE_DIR / "uploads"
REPORTS_DIR = BASE_DIR / "reports"

# Create directories if they don't exist
for directory in [MODELS_DIR, UPLOADS_DIR, REPORTS_DIR]:
    directory.mkdir(exist_ok=True)

# Model configurations
MODEL_CONFIG = {
    "face_detection": {
        "model_path": MODELS_DIR / "face_detection.pth",
        "confidence_threshold": 0.8,
    },
    "deepfake_detection": {
        "model_path": MODELS_DIR / "deepfake_detection.pth",
        "input_size": (224, 224),
        "confidence_threshold": 0.7,
    }
}

# Agent configurations
AGENT_CONFIG = {
    "coordinator": {
        "name": "coordinator_agent",
        "seed": "coordinator_seed_2024",
        "port": 8000,
    },
    "image_processor": {
        "name": "image_processor_agent",
        "seed": "image_processor_seed_2024",
        "port": 8001,
    },
    "forensic_analyzer": {
        "name": "forensic_analyzer_agent",
        "seed": "forensic_analyzer_seed_2024",
        "port": 8002,
    },
    "report_generator": {
        "name": "report_generator_agent",
        "seed": "report_generator_seed_2024",
        "port": 8003,
    }
}

# Web application settings
WEB_CONFIG = {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": False,
    "allowed_extensions": {".jpg", ".jpeg", ".png", ".bmp"},
    "max_file_size": 10 * 1024 * 1024,  # 10MB
}

# Report generation settings
REPORT_CONFIG = {
    "template": "default",
    "company_name": "Deepfake Detection System",
    "logo_path": BASE_DIR / "web_app/static/images/logo.png",
    "font_path": BASE_DIR / "web_app/static/fonts/",
}
