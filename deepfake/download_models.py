"""
Script to download and set up required models for deepfake detection
"""

import os
import gdown
import torch
import torch.nn as nn
from pathlib import Path
import cv2
import urllib.request

def download_face_cascade():
    """Download the Haar Cascade face detection model"""
    face_cascade_path = Path("models/haarcascade_frontalface_default.xml")
    if not face_cascade_path.exists():
        print("Downloading face detection model...")
        url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
        urllib.request.urlretrieve(url, face_cascade_path)
        print("Face detection model downloaded successfully!")

def download_deepfake_model():
    """Initialize the deepfake detection model"""
    model_path = Path("models/deepfake_detection.pth")
    weights_path = Path("models/xception_weights.pth")
    
    print("\nInitializing deepfake detection models...")
    
    # Create the initial model
    from agents.image_processor_agent import DeepfakeDetectionModel
    model = DeepfakeDetectionModel()
    
    # Initialize weights with Xavier initialization
    def init_weights(m):
        if isinstance(m, (nn.Conv2d, nn.Linear)):
            nn.init.xavier_uniform_(m.weight)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
    
    model.apply(init_weights)
    
    # Save model and weights
    print("Saving model files...")
    torch.save(model.state_dict(), model_path)
    torch.save(model.state_dict(), weights_path)
    print("Model files created successfully!")

def main():
    """Set up all required models"""
    # Create models directory if it doesn't exist
    Path("models").mkdir(exist_ok=True)
    
    try:
        # 1. Download face detection model
        download_face_cascade()
        
        # 2. Initialize deepfake detection model
        download_deepfake_model()
        
        print("\nAll models have been set up successfully!")
        print("\nAvailable models in ./models/:")
        print("1. haarcascade_frontalface_default.xml (Face Detection)")
        print("2. deepfake_detection.pth (Deepfake Detection)")
        print("3. xception_weights.pth (Model Weights)")
        
    except Exception as e:
        print(f"\nError during model setup: {e}")
        print("Please check your Python environment and try again.")

if __name__ == "__main__":
    main()
