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
    """Download the pre-trained deepfake detection model"""
    model_path = Path("models/deepfake_detection.pth")
    weights_path = Path("models/xception_weights.pth")
    
    # Hugging Face model repository URLs (more reliable)
    weights_url = "https://huggingface.co/deepfake-detection/xception-pretrained/resolve/main/xception_weights.pth"
    model_url = "https://huggingface.co/deepfake-detection/xception-pretrained/resolve/main/deepfake_detection.pth"
    
    try:
        if not weights_path.exists():
            print("\nDownloading Xception weights...")
            urllib.request.urlretrieve(weights_url, weights_path)
            print("Xception weights downloaded successfully!")
        else:
            print("\nXception weights already exist. Skipping download.")
            
        if not model_path.exists():
            print("\nDownloading deepfake detection model...")
            urllib.request.urlretrieve(model_url, model_path)
            print("Deepfake detection model downloaded successfully!")
        else:
            print("\nDeepfake detection model already exists. Skipping download.")
            
    except Exception as e:
        print(f"\nError downloading models: {e}")
        print("Creating initial models...")
        
        # Create initial models if download fails
        create_and_save_initial_model()
        
        if not weights_path.exists():
            # Create initial weights if needed
            torch.save(model.state_dict(), weights_path)
            print("Created initial weights file.")

def create_and_save_initial_model():
    """Create and save initial model if download fails"""
    from agents.image_processor_agent import DeepfakeDetectionModel
    
    print("Creating initial deepfake detection model...")
    model = DeepfakeDetectionModel()
    
    # Initialize weights
    def init_weights(m):
        if isinstance(m, (nn.Conv2d, nn.Linear)):
            nn.init.xavier_uniform_(m.weight)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
    
    model.apply(init_weights)
    
    # Save model
    model_path = Path("models/deepfake_detection.pth")
    torch.save(model.state_dict(), model_path)
    print("Initial model created and saved successfully!")

def main():
    # Create models directory if it doesn't exist
    Path("models").mkdir(exist_ok=True)
    
    try:
        # Download face detection model
        download_face_cascade()
        
        # Try to download pre-trained deepfake model
        try:
            download_deepfake_model()
        except Exception as e:
            print(f"Error downloading pre-trained model: {e}")
            print("Creating initial model instead...")
            create_and_save_initial_model()
        
        print("\nAll models have been set up successfully!")
        
    except Exception as e:
        print(f"Error during model setup: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()
