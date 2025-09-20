"""
Shared Message Models for 3-Agent Collaborative System
All agents use these standardized message formats
"""

from uagents import Model
from typing import List, Optional
from enum import Enum

class MessageType(str, Enum):
    """Types of messages in our system"""
    REQUEST = "request"
    DATA_COLLECTION = "data_collection" 
    ANALYSIS = "analysis"
    RECOMMENDATION = "recommendation"
    FINAL_DECISION = "final_decision"

class Priority(str, Enum):
    """Message priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

# === SHARED MESSAGE MODELS ===

class TaskRequest(Model):
    """Initial request to start a collaborative task"""
    task_id: str
    task_description: str
    user_input: str
    priority: Priority = Priority.MEDIUM
    timestamp: str
    requester: str

class DataCollection(Model):
    """Alice sends collected data to Bob"""
    task_id: str
    user_preferences: dict
    location_data: dict
    search_criteria: dict
    confidence_score: float
    timestamp: str
    sender: str = "Alice"

class AnalysisRequest(Model):
    """Bob requests additional data from Alice"""
    task_id: str
    requested_data: List[str]
    analysis_focus: str
    timestamp: str
    sender: str = "Bob"

class AnalysisResult(Model):
    """Bob sends analysis results to Charlie"""
    task_id: str
    analysis_summary: str
    recommendations: List[dict]
    confidence_scores: dict
    supporting_data: dict
    timestamp: str
    sender: str = "Bob"

class DecisionRequest(Model):
    """Charlie requests clarification or additional analysis"""
    task_id: str
    clarification_needed: str
    additional_criteria: dict
    timestamp: str
    sender: str = "Charlie"

class FinalDecision(Model):
    """Charlie's final decision broadcast to all"""
    task_id: str
    final_choice: dict
    decision_reasoning: str
    confidence_score: float
    all_participants: List[str]
    timestamp: str
    sender: str = "Charlie"

class StatusUpdate(Model):
    """General status updates between agents"""
    task_id: str
    status: str
    progress_percentage: int
    message: str
    timestamp: str
    sender: str

class ErrorMessage(Model):
    """Error handling between agents"""
    task_id: str
    error_type: str
    error_message: str
    affected_agent: str
    timestamp: str
    sender: str
