"""
Test suite for the Deepfake Detection System
"""

import pytest
import os
from pathlib import Path
import shutil
import json
from PIL import Image
import numpy as np
import torch
from datetime import datetime

from agents.base_agent import BaseAgent, BaseMessage
from agents.coordinator_agent import CoordinatorAgent
from agents.image_processor_agent import ImageProcessorAgent, DeepfakeDetectionModel
from agents.forensic_analyzer_agent import ForensicAnalyzerAgent
from agents.report_generator_agent import ReportGeneratorAgent

# Test data directory
TEST_DATA_DIR = Path("tests/test_data")
TEST_DATA_DIR.mkdir(exist_ok=True)

@pytest.fixture
def sample_image():
    """Create a sample test image"""
    image_path = TEST_DATA_DIR / "test_image.jpg"
    if not image_path.exists():
        # Create a simple test image
        img = Image.new('RGB', (224, 224), color='white')
        img.save(image_path)
    return image_path

@pytest.fixture
def test_agents():
    """Initialize test agents"""
    coordinator = CoordinatorAgent(
        name="test_coordinator",
        seed="test_seed_1",
        port=9000
    )
    
    image_processor = ImageProcessorAgent(
        name="test_processor",
        seed="test_seed_2",
        port=9001
    )
    
    forensic_analyzer = ForensicAnalyzerAgent(
        name="test_analyzer",
        seed="test_seed_3",
        port=9002
    )
    
    report_generator = ReportGeneratorAgent(
        name="test_generator",
        seed="test_seed_4",
        port=9003
    )
    
    return {
        "coordinator": coordinator,
        "image_processor": image_processor,
        "forensic_analyzer": forensic_analyzer,
        "report_generator": report_generator
    }

def test_base_agent():
    """Test base agent functionality"""
    agent = BaseAgent(
        name="test_agent",
        seed="test_seed",
        port=9999
    )
    
    assert agent.agent.name == "test_agent"
    assert agent.logger is not None

def test_deepfake_detection_model():
    """Test the deepfake detection model"""
    model = DeepfakeDetectionModel()
    
    # Test forward pass
    test_input = torch.randn(1, 3, 224, 224)
    output = model(test_input)
    
    assert output.shape == (1, 2)
    assert torch.is_tensor(output)

def test_image_processor(sample_image, test_agents):
    """Test image processor agent"""
    processor = test_agents["image_processor"]
    
    # Test image loading and preprocessing
    image = Image.open(sample_image)
    tensor_image = processor.transform(image).unsqueeze(0)
    
    assert tensor_image.shape == (1, 3, 224, 224)
    
    # Test face detection
    cv_image = np.array(image)
    faces = processor._detect_faces(cv_image)
    
    assert isinstance(faces, list)

def test_forensic_analyzer(sample_image, test_agents):
    """Test forensic analyzer agent"""
    analyzer = test_agents["forensic_analyzer"]
    
    # Test metadata extraction
    metadata = analyzer._extract_metadata(sample_image)
    
    assert isinstance(metadata, dict)
    assert "file_size" in metadata
    assert "file_name" in metadata
    
    # Test image hash calculation
    image = Image.open(sample_image)
    hashes = analyzer._calculate_image_hashes(sample_image)
    
    assert isinstance(hashes, dict)
    assert len(hashes) == 4  # Should have 4 different hash types

def test_report_generator(test_agents):
    """Test report generator agent"""
    generator = test_agents["report_generator"]
    
    # Test report generation
    test_data = {
        "analysis_result": {
            "confidence_score": 0.8,
            "prediction": "fake",
            "num_faces_detected": 1,
            "analysis_details": {
                "resolution": (224, 224),
                "color_analysis": {
                    "mean_r": 128.0,
                    "mean_g": 128.0,
                    "mean_b": 128.0,
                    "std_r": 10.0,
                    "std_g": 10.0,
                    "std_b": 10.0
                }
            }
        },
        "forensic_result": {
            "metadata": {},
            "forensic_score": 0.7,
            "anomalies": {
                "metadata": ["Test anomaly"],
                "ela": ["Test ELA anomaly"]
            }
        }
    }
    
    summary = generator._generate_report_summary(
        test_data["analysis_result"],
        test_data["forensic_result"]
    )
    
    assert isinstance(summary, dict)
    assert "verdict" in summary
    assert "confidence" in summary
    assert summary["verdict"] in ["LIKELY FAKE", "LIKELY GENUINE"]

def test_coordinator_workflow(sample_image, test_agents):
    """Test complete workflow coordination"""
    coordinator = test_agents["coordinator"]
    
    # Create test task
    task_id = f"test_{int(datetime.now().timestamp())}"
    test_message = BaseMessage(
        task_id=task_id,
        timestamp=datetime.now().isoformat(),
        sender="test",
        message_type="test",
        data={"image_path": str(sample_image)},
        status="pending"
    )
    
    # Test task storage
    coordinator._store_task(coordinator.agent.context, task_id, test_message.data)
    
    tasks = coordinator.agent.context.storage.get("tasks", {})
    assert task_id in tasks
    assert tasks[task_id]["status"] == "pending"

def test_cleanup():
    """Clean up test data"""
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)

if __name__ == "__main__":
    pytest.main([__file__])
