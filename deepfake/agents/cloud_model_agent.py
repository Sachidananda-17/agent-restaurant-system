"""
Agent that uses cloud storage for model integration
"""

from uagents import Agent, Context, Model
import requests
from pathlib import Path
import torch
import asyncio
import os
from typing import Optional

class ModelRequest(Model):
    """Request for model prediction"""
    image_url: str
    task_id: str

class ModelResponse(Model):
    """Response from model prediction"""
    task_id: str
    result: dict
    confidence: float
    status: str

class CloudModelAgent(Agent):
    """Agent that handles model inference using cloud storage"""
    
    def __init__(self, name: str, seed: str, port: int):
        super().__init__(name=name, seed=seed, port=port)
        self.api_endpoint = os.getenv("MODEL_API_ENDPOINT")
        self.api_key = os.getenv("MODEL_API_KEY")

    @agent.on_message(model=ModelRequest)
    async def handle_prediction(self, ctx: Context, sender: str, msg: ModelRequest):
        """Handle prediction request"""
        try:
            # Instead of loading model locally, make API call
            result = await self._get_prediction(msg.image_url)
            
            await ctx.send(sender, ModelResponse(
                task_id=msg.task_id,
                result=result,
                confidence=result.get('confidence', 0.0),
                status='success'
            ))
        except Exception as e:
            await ctx.send(sender, ModelResponse(
                task_id=msg.task_id,
                result={},
                confidence=0.0,
                status=f'error: {str(e)}'
            ))

    async def _get_prediction(self, image_url: str) -> dict:
        """Get prediction from cloud API"""
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'image_url': image_url,
            'model_type': 'deepfake_detection'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.api_endpoint,
                headers=headers,
                json=data
            ) as response:
                return await response.json()

# Example usage in coordinator agent:
@agent.on_message(model=ImageAnalysisRequest)
async def handle_image(self, ctx: Context, sender: str, msg: ImageAnalysisRequest):
    # 1. Upload image to cloud storage
    image_url = await self._upload_to_cloud(msg.image_path)
    
    # 2. Send request to model agent
    await ctx.send(
        "model_agent_address",
        ModelRequest(
            image_url=image_url,
            task_id=msg.task_id
        )
    )
