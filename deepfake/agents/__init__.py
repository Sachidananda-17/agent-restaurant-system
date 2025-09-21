"""
Agent module initialization
"""

from .base_agent import BaseAgent, BaseMessage
from .coordinator_agent import CoordinatorAgent
from .image_processor_agent import ImageProcessorAgent, DeepfakeDetectionModel
from .forensic_analyzer_agent import ForensicAnalyzerAgent
from .report_generator_agent import ReportGeneratorAgent

__all__ = [
    'BaseAgent',
    'BaseMessage',
    'CoordinatorAgent',
    'ImageProcessorAgent',
    'DeepfakeDetectionModel',
    'ForensicAnalyzerAgent',
    'ReportGeneratorAgent'
]
