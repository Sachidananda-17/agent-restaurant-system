"""
Coordinator Agent - Manages the workflow and communication between agents
"""

from datetime import datetime
import asyncio
from typing import Dict, Any
from uagents import Context, Model

from .base_agent import (
    BaseAgent, BaseMessage, TaskRequest, 
    AnalysisResult, ForensicResult, ReportResult
)

class WorkflowStatus(Model):
    """Workflow status update message"""
    task_id: str
    status: str
    progress: float
    current_stage: str
    stages_completed: Dict[str, bool]
    timestamp: str

class CoordinatorAgent(BaseAgent):
    """
    Coordinator Agent that manages the workflow between other agents
    """
    
    def __init__(self, name: str, seed: str, port: int):
        """Initialize the Coordinator Agent"""
        super().__init__(name, seed, port)
        self._register_coordinator_handlers()

    def _register_coordinator_handlers(self):
        """Register coordinator-specific message handlers"""
        
        @self.agent.on_message(model=TaskRequest)
        async def handle_task_request(ctx: Context, sender: str, msg: TaskRequest):
            """Handle incoming task requests"""
            try:
                self.logger.info(f"Received task request: {msg.task_id}")
                
                # Store task information
                self._store_task(ctx, msg.task_id, {
                    "image_path": msg.image_path,
                    "request_type": msg.request_type,
                    "stages": {
                        "image_processing": False,
                        "forensic_analysis": False,
                        "report_generation": False
                    }
                })

                # Start parallel processing
                await self._initiate_parallel_processing(ctx, msg)
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

        @self.agent.on_message(model=AnalysisResult)
        async def handle_analysis_result(ctx: Context, sender: str, msg: AnalysisResult):
            """Handle image processing results"""
            try:
                self.logger.info(f"Received analysis result for task: {msg.task_id}")
                
                # Update task status
                tasks = ctx.storage.get("tasks", {})
                if msg.task_id in tasks:
                    tasks[msg.task_id]["analysis_result"] = msg.data
                    tasks[msg.task_id]["stages"]["image_processing"] = True
                    ctx.storage.set("tasks", tasks)
                
                # Check if we can generate the report
                await self._check_and_generate_report(ctx, msg.task_id)
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

        @self.agent.on_message(model=ForensicResult)
        async def handle_forensic_result(ctx: Context, sender: str, msg: ForensicResult):
            """Handle forensic analysis results"""
            try:
                self.logger.info(f"Received forensic result for task: {msg.task_id}")
                
                # Update task status
                tasks = ctx.storage.get("tasks", {})
                if msg.task_id in tasks:
                    tasks[msg.task_id]["forensic_result"] = msg.data
                    tasks[msg.task_id]["stages"]["forensic_analysis"] = True
                    ctx.storage.set("tasks", tasks)
                
                # Check if we can generate the report
                await self._check_and_generate_report(ctx, msg.task_id)
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

        @self.agent.on_message(model=ReportResult)
        async def handle_report_result(ctx: Context, sender: str, msg: ReportResult):
            """Handle report generation results"""
            try:
                self.logger.info(f"Received report result for task: {msg.task_id}")
                
                # Update task status
                tasks = ctx.storage.get("tasks", {})
                if msg.task_id in tasks:
                    tasks[msg.task_id]["report_result"] = msg.data
                    tasks[msg.task_id]["stages"]["report_generation"] = True
                    tasks[msg.task_id]["status"] = "completed"
                    ctx.storage.set("tasks", tasks)
                
                # Send completion notification
                await self._send_completion_notification(ctx, msg.task_id)
                
            except Exception as e:
                await self.handle_error(ctx, msg.task_id, e)

    async def _initiate_parallel_processing(self, ctx: Context, msg: TaskRequest):
        """Initiate parallel processing of the image"""
        # Send request to Image Processor Agent
        await ctx.send(
            "image_processor_agent",
            TaskRequest(
                task_id=msg.task_id,
                timestamp=datetime.now().isoformat(),
                sender=self.agent.name,
                message_type="process_image",
                data={"image_path": msg.image_path},
                image_path=msg.image_path
            )
        )
        
        # Send request to Forensic Analyzer Agent
        await ctx.send(
            "forensic_analyzer_agent",
            TaskRequest(
                task_id=msg.task_id,
                timestamp=datetime.now().isoformat(),
                sender=self.agent.name,
                message_type="analyze_forensics",
                data={"image_path": msg.image_path},
                image_path=msg.image_path
            )
        )

    async def _check_and_generate_report(self, ctx: Context, task_id: str):
        """Check if all analyses are complete and generate report"""
        tasks = ctx.storage.get("tasks", {})
        if task_id not in tasks:
            return
        
        task = tasks[task_id]
        if (task["stages"]["image_processing"] and 
            task["stages"]["forensic_analysis"] and 
            not task["stages"]["report_generation"]):
            
            # Send report generation request
            await ctx.send(
                "report_generator_agent",
                TaskRequest(
                    task_id=task_id,
                    timestamp=datetime.now().isoformat(),
                    sender=self.agent.name,
                    message_type="generate_report",
                    data={
                        "analysis_result": task["analysis_result"],
                        "forensic_result": task["forensic_result"]
                    },
                    image_path=task["image_path"]
                )
            )

    async def _send_completion_notification(self, ctx: Context, task_id: str):
        """Send completion notification to web interface"""
        tasks = ctx.storage.get("tasks", {})
        if task_id not in tasks:
            return
        
        task = tasks[task_id]
        await ctx.send(
            "web_interface",
            WorkflowStatus(
                task_id=task_id,
                status="completed",
                progress=1.0,
                current_stage="completed",
                stages_completed=task["stages"],
                timestamp=datetime.now().isoformat()
            )
        )

    async def _send_status_update(self, ctx: Context, task_id: str):
        """Send status update to web interface"""
        tasks = ctx.storage.get("tasks", {})
        if task_id not in tasks:
            return
        
        task = tasks[task_id]
        completed_stages = sum(1 for stage in task["stages"].values() if stage)
        total_stages = len(task["stages"])
        
        current_stage = "waiting"
        if not task["stages"]["image_processing"]:
            current_stage = "image_processing"
        elif not task["stages"]["forensic_analysis"]:
            current_stage = "forensic_analysis"
        elif not task["stages"]["report_generation"]:
            current_stage = "report_generation"
        
        await ctx.send(
            "web_interface",
            WorkflowStatus(
                task_id=task_id,
                status="in_progress",
                progress=completed_stages / total_stages,
                current_stage=current_stage,
                stages_completed=task["stages"],
                timestamp=datetime.now().isoformat()
            )
        )
