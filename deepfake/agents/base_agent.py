"""
Base Agent class for the Deepfake Detection System
"""

from uagents import Agent, Context, Model
from typing import Optional, Dict, Any
import logging
import json
from datetime import datetime
from pathlib import Path

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

class BaseMessage(Model):
    """Base message model for agent communication"""
    task_id: str
    timestamp: str
    sender: str
    message_type: str
    data: Dict[str, Any]
    status: str = "pending"
    error: Optional[str] = None

class TaskRequest(BaseMessage):
    """Initial task request message"""
    image_path: str
    request_type: str = "analysis"

class AnalysisResult(BaseMessage):
    """Analysis result message"""
    confidence_score: float
    analysis_details: Dict[str, Any]
    processing_time: float

class ForensicResult(BaseMessage):
    """Forensic analysis result message"""
    metadata: Dict[str, Any]
    forensic_score: float
    anomalies: Dict[str, Any]

class ReportRequest(BaseMessage):
    """Report generation request message"""
    analysis_results: Dict[str, Any]
    forensic_results: Dict[str, Any]
    output_path: str

class ReportResult(BaseMessage):
    """Report generation result message"""
    report_path: str
    report_summary: Dict[str, Any]

class BaseAgent:
    """Base agent class with common functionality"""
    
    def __init__(self, name: str, seed: str, port: int):
        """Initialize the agent with basic configuration"""
        # Configure agent with minimal network interaction
        self.agent = Agent(
            name=name,
            seed=seed,
            port=port,
            endpoint=None  # Disable external endpoints for local development
        )
        self.logger = self._setup_logger()
        self._register_handlers()

    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the agent"""
        logger = logging.getLogger(self.agent.name)
        logger.setLevel(logging.INFO)
        
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(str(LOGS_DIR / f"{self.agent.name}.log"))
        
        # Create formatters
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
        
        return logger

    def _register_handlers(self):
        """Register message handlers for the agent"""
        
        @self.agent.on_event("startup")
        async def startup(ctx: Context):
            """Handle agent startup"""
            self.logger.info(f"Agent {self.agent.name} starting up...")
            ctx.storage.set("tasks", {})

        @self.agent.on_event("shutdown")
        async def shutdown(ctx: Context):
            """Handle agent shutdown"""
            self.logger.info(f"Agent {self.agent.name} shutting down...")
            # Cleanup code here

        @self.agent.on_interval(period=300.0)
        async def cleanup_old_tasks(ctx: Context):
            """Clean up old completed tasks periodically"""
            try:
                tasks = ctx.storage.get("tasks") or {}
                current_time = datetime.now()
                
                # Remove tasks older than 1 hour
                tasks = {
                    task_id: task_data 
                    for task_id, task_data in tasks.items()
                    if (current_time - datetime.fromisoformat(task_data["timestamp"])).total_seconds() < 3600
                }
                
                ctx.storage.set("tasks", tasks)
            except Exception as e:
                self.logger.error(f"Error cleaning up tasks: {e}")

    def _store_task(self, ctx: Context, task_id: str, data: Dict[str, Any]):
        """Store task data in agent storage"""
        tasks = ctx.storage.get("tasks") or {}
        tasks[task_id] = {
            "timestamp": datetime.now().isoformat(),
            "data": data,
            "status": "pending"
        }
        ctx.storage.set("tasks", tasks)

    def _update_task_status(self, ctx: Context, task_id: str, status: str, result: Optional[Dict] = None):
        """Update task status and result"""
        tasks = ctx.storage.get("tasks") or {}
        if task_id in tasks:
            tasks[task_id]["status"] = status
            if result:
                tasks[task_id]["result"] = result
            ctx.storage.set("tasks", tasks)

    def _format_error_message(self, task_id: str, error_msg: str) -> BaseMessage:
        """Format error message"""
        return BaseMessage(
            task_id=task_id,
            timestamp=datetime.now().isoformat(),
            sender=self.agent.name,
            message_type="error",
            data={},
            status="error",
            error=error_msg
        )

    async def handle_error(self, ctx: Context, task_id: str, error: Exception):
        """Handle and log errors"""
        error_msg = f"Error in {self.agent.name}: {str(error)}"
        self.logger.error(error_msg)
        self._update_task_status(ctx, task_id, "error")
        return self._format_error_message(task_id, error_msg)

    def run(self):
        """Run the agent"""
        self.agent.run()
