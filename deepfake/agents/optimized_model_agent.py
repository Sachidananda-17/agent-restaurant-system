"""
Optimized Model Agent for uAgents - No cloud dependencies
"""

from uagents import Agent, Context, Model
import cv2
import numpy as np
from pathlib import Path
import json

class ImageRequest(Model):
    """Request for image analysis"""
    image_path: str
    task_id: str

class ImageResponse(Model):
    """Response with analysis results"""
    task_id: str
    results: dict
    status: str

class OptimizedModelAgent(Agent):
    """Agent that uses optimized local processing"""
    
    def __init__(self, name: str, seed: str, port: int):
        super().__init__(name=name, seed=seed, port=port)
        # Use OpenCV's built-in face detector
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
    @agent.on_message(model=ImageRequest)
    async def analyze_image(self, ctx: Context, sender: str, msg: ImageRequest):
        """Analyze image for potential deepfake indicators"""
        try:
            # Load image
            image = cv2.imread(msg.image_path)
            
            # 1. Face Detection
            faces = self._detect_faces(image)
            
            # 2. Basic Image Analysis
            analysis = self._analyze_image_properties(image)
            
            # 3. Metadata Analysis
            metadata = self._extract_metadata(msg.image_path)
            
            # 4. Combine Results
            results = {
                "faces_detected": len(faces),
                "face_locations": faces,
                "image_analysis": analysis,
                "metadata": metadata,
                "confidence_score": self._calculate_confidence(analysis, metadata)
            }
            
            await ctx.send(sender, ImageResponse(
                task_id=msg.task_id,
                results=results,
                status="success"
            ))
            
        except Exception as e:
            await ctx.send(sender, ImageResponse(
                task_id=msg.task_id,
                results={},
                status=f"error: {str(e)}"
            ))

    def _detect_faces(self, image):
        """Detect faces in image"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=5,
            minSize=(30, 30)
        )
        return faces.tolist()

    def _analyze_image_properties(self, image):
        """Analyze basic image properties"""
        # 1. Check image quality
        quality_score = cv2.Laplacian(image, cv2.CV_64F).var()
        
        # 2. Check color distribution
        color_means = image.mean(axis=(0, 1))
        color_stds = image.std(axis=(0, 1))
        
        # 3. Check noise levels
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        noise_level = np.std(gray)
        
        # 4. Check compression artifacts
        edges = cv2.Canny(image, 100, 200)
        artifact_score = np.mean(edges)
        
        return {
            "quality_score": float(quality_score),
            "color_distribution": {
                "means": color_means.tolist(),
                "stds": color_stds.tolist()
            },
            "noise_level": float(noise_level),
            "artifact_score": float(artifact_score)
        }

    def _extract_metadata(self, image_path):
        """Extract image metadata"""
        # Get basic file info
        path = Path(image_path)
        stats = path.stat()
        
        return {
            "file_size": stats.st_size,
            "creation_time": stats.st_ctime,
            "modification_time": stats.st_mtime,
            "file_extension": path.suffix
        }

    def _calculate_confidence(self, analysis, metadata):
        """Calculate confidence score based on analysis"""
        # Combine multiple factors for confidence score
        confidence = 0.0
        
        # 1. Image quality factor (0-0.25)
        quality_factor = min(analysis["quality_score"] / 1000.0, 0.25)
        confidence += quality_factor
        
        # 2. Noise level factor (0-0.25)
        noise_factor = min(analysis["noise_level"] / 100.0, 0.25)
        confidence += noise_factor
        
        # 3. Artifact factor (0-0.25)
        artifact_factor = min(analysis["artifact_score"] / 100.0, 0.25)
        confidence += artifact_factor
        
        # 4. Metadata factor (0-0.25)
        if metadata["file_size"] > 100000:  # If file size > 100KB
            confidence += 0.25
        
        return min(confidence, 1.0)  # Ensure max confidence is 1.0
