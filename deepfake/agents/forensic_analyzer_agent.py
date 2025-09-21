"""
Forensic Analyzer Agent - Performs metadata and forensic analysis
"""

import exifread
import imagehash
from PIL import Image
import os
from datetime import datetime
import time
from pathlib import Path
from typing import Dict, Any, List, Tuple
import json
import numpy as np
from collections import defaultdict
import cv2

from uagents import Context
from .base_agent import BaseAgent, TaskRequest, ForensicResult

class ForensicAnalyzerAgent(BaseAgent):
    """
    Agent responsible for forensic analysis of images
    """
    
    def __init__(self, name: str, seed: str, port: int):
        """Initialize the Forensic Analyzer Agent"""
        super().__init__(name, seed, port)
        self._register_forensic_analyzer_handlers()
        self.known_camera_models = self._load_camera_models()
        self.error_level_analysis_threshold = 40

    def _load_camera_models(self) -> Dict[str, Dict[str, Any]]:
        """Load database of known camera models and their characteristics"""
        camera_db_path = Path("data/camera_models.json")
        if camera_db_path.exists():
            with open(camera_db_path, 'r') as f:
                return json.load(f)
        return {}

    def _register_forensic_analyzer_handlers(self):
        """Register forensic analyzer specific message handlers"""
        
        @self.agent.on_message(model=TaskRequest)
        async def analyze_forensics(ctx: Context, sender: str, msg: TaskRequest):
            """Perform forensic analysis on the image"""
            try:
                start_time = time.time()
                
                # Analyze image
                image_path = Path(msg.image_path)
                if not image_path.exists():
                    raise FileNotFoundError(f"Image not found: {image_path}")
                
                # Perform analysis
                result = await self._analyze_forensics(image_path)
                
                # Calculate processing time
                processing_time = time.time() - start_time
                
                # Send results
                await ctx.send(
                    sender,
                    ForensicResult(
                        task_id=msg.task_id,
                        timestamp=datetime.now().isoformat(),
                        sender=self.agent.name,
                        message_type="forensic_result",
                        data=result,
                        metadata=result["metadata"],
                        forensic_score=result["forensic_score"],
                        anomalies=result["anomalies"],
                        status="completed"
                    )
                )
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

    def _analyze_forensics(self, image_path: Path) -> Dict[str, Any]:
        """Perform comprehensive forensic analysis"""
        # Extract metadata
        metadata = self._extract_metadata(image_path)
        
        # Calculate image hashes
        hashes = self._calculate_image_hashes(image_path)
        
        # Perform Error Level Analysis (ELA)
        ela_results = self._perform_ela(image_path)
        
        # Check metadata consistency
        consistency_check = self._check_metadata_consistency(metadata)
        
        # Analyze compression artifacts
        compression_analysis = self._analyze_compression(image_path)
        
        # Calculate noise patterns
        noise_analysis = self._analyze_noise_patterns(image_path)
        
        # Combine all analyses
        anomalies = self._detect_anomalies(
            metadata, ela_results, compression_analysis, noise_analysis
        )
        
        # Calculate overall forensic score
        forensic_score = self._calculate_forensic_score(
            consistency_check["score"],
            ela_results["score"],
            compression_analysis["score"],
            noise_analysis["score"]
        )
        
        return {
            "metadata": metadata,
            "image_hashes": hashes,
            "ela_analysis": ela_results,
            "compression_analysis": compression_analysis,
            "noise_analysis": noise_analysis,
            "metadata_consistency": consistency_check,
            "forensic_score": forensic_score,
            "anomalies": anomalies
        }

    def _extract_metadata(self, image_path: Path) -> Dict[str, Any]:
        """Extract and analyze image metadata"""
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        
        # Convert tags to dictionary
        metadata = {}
        for tag, value in tags.items():
            if tag not in ('JPEGThumbnail', 'TIFFThumbnail'):
                metadata[tag] = str(value)
        
        # Add file information
        file_stats = os.stat(image_path)
        metadata.update({
            "file_size": file_stats.st_size,
            "creation_time": datetime.fromtimestamp(file_stats.st_ctime).isoformat(),
            "modification_time": datetime.fromtimestamp(file_stats.st_mtime).isoformat(),
            "file_name": image_path.name,
            "file_extension": image_path.suffix.lower()
        })
        
        return metadata

    def _calculate_image_hashes(self, image_path: Path) -> Dict[str, str]:
        """Calculate various image hashes"""
        image = Image.open(image_path)
        return {
            "average_hash": str(imagehash.average_hash(image)),
            "perceptual_hash": str(imagehash.phash(image)),
            "difference_hash": str(imagehash.dhash(image)),
            "wavelet_hash": str(imagehash.whash(image))
        }

    def _perform_ela(self, image_path: Path) -> Dict[str, Any]:
        """Perform Error Level Analysis"""
        # Load image
        image = Image.open(image_path)
        
        # Save with specific quality
        temp_path = image_path.parent / f"temp_ela_{image_path.name}"
        image.save(temp_path, 'JPEG', quality=95)
        
        # Load compressed image
        compressed = Image.open(temp_path)
        
        # Calculate difference
        ela_image = Image.new('RGB', image.size, (0, 0, 0))
        for x in range(image.size[0]):
            for y in range(image.size[1]):
                orig_pixel = image.getpixel((x, y))
                compressed_pixel = compressed.getpixel((x, y))
                diff = tuple(abs(a - b) for a, b in zip(orig_pixel, compressed_pixel))
                ela_image.putpixel((x, y), diff)
        
        # Clean up
        temp_path.unlink()
        
        # Analyze ELA results
        ela_array = np.array(ela_image)
        ela_mean = float(ela_array.mean())
        ela_std = float(ela_array.std())
        
        # Calculate score based on ELA statistics
        score = 1.0 - min(1.0, ela_std / self.error_level_analysis_threshold)
        
        return {
            "mean_error": ela_mean,
            "std_error": ela_std,
            "score": score,
            "analysis": "Potential manipulation" if score < 0.5 else "No obvious manipulation"
        }

    def _check_metadata_consistency(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Check consistency of metadata"""
        inconsistencies = []
        score = 1.0
        
        # Check camera model consistency
        if 'Image Make' in metadata and 'Image Model' in metadata:
            camera_id = f"{metadata['Image Make']}_{metadata['Image Model']}"
            if camera_id in self.known_camera_models:
                expected_params = self.known_camera_models[camera_id]
                # Check various parameters against expected values
                for param, expected in expected_params.items():
                    if param in metadata and metadata[param] != expected:
                        inconsistencies.append(f"Unexpected {param} for camera model")
                        score -= 0.1
        
        # Check timestamp consistency
        if 'EXIF DateTimeOriginal' in metadata and 'EXIF DateTimeDigitized' in metadata:
            if metadata['EXIF DateTimeOriginal'] > metadata['EXIF DateTimeDigitized']:
                inconsistencies.append("Original timestamp after digitized timestamp")
                score -= 0.2
        
        # Check software consistency
        if 'Image Software' in metadata:
            software = metadata['Image Software'].lower()
            if 'photoshop' in software or 'gimp' in software:
                inconsistencies.append("Image edited with photo editing software")
                score -= 0.15
        
        return {
            "score": max(0.0, score),
            "inconsistencies": inconsistencies,
            "analysis": "Consistent" if score > 0.7 else "Suspicious"
        }

    def _analyze_compression(self, image_path: Path) -> Dict[str, Any]:
        """Analyze compression artifacts"""
        image = Image.open(image_path)
        image_array = np.array(image)
        
        # Calculate DCT coefficients
        def get_dct_coefficients(block):
            return np.abs(np.fft.fft2(block))
        
        # Analyze blocks
        block_size = 8
        height, width = image_array.shape[:2]
        coefficients = []
        
        for i in range(0, height - block_size, block_size):
            for j in range(0, width - block_size, block_size):
                block = image_array[i:i+block_size, j:j+block_size]
                if len(block.shape) == 3:  # Color image
                    block = block.mean(axis=2)  # Convert to grayscale
                coeffs = get_dct_coefficients(block)
                coefficients.append(coeffs)
        
        # Analyze coefficient distribution
        coefficients = np.array(coefficients)
        mean_coeffs = coefficients.mean(axis=0)
        std_coeffs = coefficients.std(axis=0)
        
        # Calculate compression score
        compression_score = 1.0 - (std_coeffs.mean() / mean_coeffs.mean())
        
        return {
            "score": float(compression_score),
            "mean_coefficients": float(mean_coeffs.mean()),
            "std_coefficients": float(std_coeffs.mean()),
            "analysis": "Heavy compression" if compression_score < 0.5 else "Normal compression"
        }

    def _analyze_noise_patterns(self, image_path: Path) -> Dict[str, Any]:
        """Analyze noise patterns in the image"""
        image = Image.open(image_path)
        image_array = np.array(image)
        
        # Extract noise
        def extract_noise(channel):
            blurred = cv2.GaussianBlur(channel, (0, 0), 3)
            noise = channel - blurred
            return noise
        
        # Process each channel
        noise_patterns = []
        if len(image_array.shape) == 3:  # Color image
            for channel in range(3):
                noise = extract_noise(image_array[:, :, channel])
                noise_patterns.append(noise)
        else:  # Grayscale image
            noise = extract_noise(image_array)
            noise_patterns.append(noise)
        
        # Analyze noise statistics
        noise_stats = []
        for noise in noise_patterns:
            stats = {
                "mean": float(np.mean(noise)),
                "std": float(np.std(noise)),
                "skewness": float(np.mean((noise - np.mean(noise))**3)),
                "kurtosis": float(np.mean((noise - np.mean(noise))**4))
            }
            noise_stats.append(stats)
        
        # Calculate noise consistency score
        consistency_scores = []
        for stats in noise_stats:
            # Check if noise statistics are within expected ranges
            if abs(stats["mean"]) < 0.1 and 0.1 < stats["std"] < 10:
                consistency_scores.append(1.0)
            else:
                consistency_scores.append(0.0)
        
        noise_score = sum(consistency_scores) / len(consistency_scores)
        
        return {
            "score": noise_score,
            "channel_statistics": noise_stats,
            "analysis": "Consistent noise" if noise_score > 0.7 else "Suspicious noise patterns"
        }

    def _detect_anomalies(
        self,
        metadata: Dict[str, Any],
        ela_results: Dict[str, Any],
        compression_analysis: Dict[str, Any],
        noise_analysis: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """Detect and categorize anomalies"""
        anomalies = defaultdict(list)
        
        # Metadata anomalies
        if 'Image Software' in metadata:
            if 'photoshop' in metadata['Image Software'].lower():
                anomalies["metadata"].append("Edited with Photoshop")
        
        # ELA anomalies
        if ela_results["score"] < 0.5:
            anomalies["ela"].append(
                f"High error levels detected (score: {ela_results['score']:.2f})"
            )
        
        # Compression anomalies
        if compression_analysis["score"] < 0.5:
            anomalies["compression"].append(
                f"Unusual compression patterns (score: {compression_analysis['score']:.2f})"
            )
        
        # Noise anomalies
        if noise_analysis["score"] < 0.7:
            anomalies["noise"].append(
                f"Inconsistent noise patterns (score: {noise_analysis['score']:.2f})"
            )
        
        return dict(anomalies)

    def _calculate_forensic_score(
        self,
        metadata_score: float,
        ela_score: float,
        compression_score: float,
        noise_score: float
    ) -> float:
        """Calculate overall forensic score"""
        weights = {
            "metadata": 0.3,
            "ela": 0.3,
            "compression": 0.2,
            "noise": 0.2
        }
        
        weighted_score = (
            metadata_score * weights["metadata"] +
            ela_score * weights["ela"] +
            compression_score * weights["compression"] +
            noise_score * weights["noise"]
        )
        
        return float(weighted_score)
