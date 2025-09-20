"""
Image Processor Agent - Handles image analysis and deepfake detection
"""

import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
from datetime import datetime
import time
from pathlib import Path
from typing import Tuple, Dict, Any

from uagents import Context
from .base_agent import BaseAgent, TaskRequest, AnalysisResult

class DeepfakeDetectionModel(nn.Module):
    """Simple CNN model for deepfake detection"""
    def __init__(self):
        super(DeepfakeDetectionModel, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, 3)
        self.conv2 = nn.Conv2d(32, 64, 3)
        self.conv3 = nn.Conv2d(64, 128, 3)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(128 * 26 * 26, 512)
        self.fc2 = nn.Linear(512, 2)
        self.dropout = nn.Dropout(0.5)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 128 * 26 * 26)
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x

class ImageProcessorAgent(BaseAgent):
    """
    Agent responsible for image processing and deepfake detection
    """
    
    def __init__(self, name: str, seed: str, port: int):
        """Initialize the Image Processor Agent"""
        super().__init__(name, seed, port)
        self.model = self._load_model()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                              std=[0.229, 0.224, 0.225])
        ])
        self._register_image_processor_handlers()

    def _load_model(self) -> nn.Module:
        """Load the deepfake detection model"""
        model = DeepfakeDetectionModel()
        model_path = Path("models/deepfake_detection.pth")
        
        if model_path.exists():
            model.load_state_dict(torch.load(model_path))
        else:
            self.logger.warning("Model file not found. Using untrained model.")
        
        model.eval()
        return model

    def _register_image_processor_handlers(self):
        """Register image processor specific message handlers"""
        
        @self.agent.on_message(model=TaskRequest)
        async def process_image(ctx: Context, sender: str, msg: TaskRequest):
            """Process the image and detect deepfakes"""
            try:
                start_time = time.time()
                
                # Process image
                image_path = Path(msg.image_path)
                if not image_path.exists():
                    raise FileNotFoundError(f"Image not found: {image_path}")
                
                # Perform analysis
                result = await self._analyze_image(image_path)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Send results
                await ctx.send(
                    sender,
                    AnalysisResult(
                        task_id=msg.task_id,
                        timestamp=datetime.now().isoformat(),
                        sender=self.agent.name,
                        message_type="analysis_result",
                        data=result,
                        confidence_score=result["confidence_score"],
                        analysis_details=result,
                        processing_time=processing_time,
                        status="completed"
                    )
                )
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

    async def _analyze_image(self, image_path: Path) -> Dict[str, Any]:
        """Perform comprehensive image analysis"""
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        cv_image = cv2.imread(str(image_path))
        
        # Detect faces
        faces = self._detect_faces(cv_image)
        
        # Generate heatmap
        heatmap = self._generate_heatmap(cv_image)
        
        # Perform deepfake detection
        tensor_image = self.transform(image).unsqueeze(0)
        with torch.no_grad():
            output = self.model(tensor_image)
            probabilities = torch.softmax(output, dim=1)
            confidence_score = float(probabilities[0][1])  # Probability of being fake
        
        # Save visualization results
        output_path = Path("outputs") / image_path.name
        output_path.parent.mkdir(exist_ok=True)
        self._save_visualization(cv_image, faces, heatmap, output_path)
        
        return {
            "confidence_score": confidence_score,
            "num_faces_detected": len(faces),
            "face_locations": faces,
            "heatmap_path": str(output_path),
            "prediction": "fake" if confidence_score > 0.5 else "real",
            "analysis_details": {
                "resolution": image.size,
                "aspect_ratio": image.size[0] / image.size[1],
                "color_analysis": self._analyze_color_distribution(image),
            }
        }

    def _detect_faces(self, image: np.ndarray) -> list:
        """Detect faces in the image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        return faces.tolist()

    def _generate_heatmap(self, image: np.ndarray) -> np.ndarray:
        """Generate activation heatmap"""
        # Convert to grayscale and normalize
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        normalized = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(normalized, (15, 15), 0)
        
        # Create heatmap
        heatmap = cv2.applyColorMap(blurred, cv2.COLORMAP_JET)
        return heatmap

    def _analyze_color_distribution(self, image: Image.Image) -> Dict[str, float]:
        """Analyze color distribution in the image"""
        # Convert to numpy array
        np_image = np.array(image)
        
        # Calculate color statistics
        means = np_image.mean(axis=(0, 1))
        stds = np_image.std(axis=(0, 1))
        
        return {
            "mean_r": float(means[0]),
            "mean_g": float(means[1]),
            "mean_b": float(means[2]),
            "std_r": float(stds[0]),
            "std_g": float(stds[1]),
            "std_b": float(stds[2])
        }

    def _save_visualization(
        self, 
        image: np.ndarray, 
        faces: list, 
        heatmap: np.ndarray, 
        output_path: Path
    ):
        """Save visualization with faces and heatmap"""
        # Draw faces
        result = image.copy()
        for (x, y, w, h) in faces:
            cv2.rectangle(result, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Combine with heatmap
        alpha = 0.3
        overlay = cv2.addWeighted(result, 1-alpha, heatmap, alpha, 0)
        
        # Save result
        cv2.imwrite(str(output_path), overlay)
