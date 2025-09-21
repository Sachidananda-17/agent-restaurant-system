"""
Example of how models integrate with uAgents flow
"""

from uagents import Agent, Context, Model
from pathlib import Path
import torch
import asyncio

# Message Models
class ImageRequest(Model):
    task_id: str
    image_path: str

class AnalysisResult(Model):
    task_id: str
    confidence_score: float
    is_fake: bool
    analysis_details: dict

class ModelAgent(Agent):
    def __init__(self, name: str, seed: str, port: int):
        super().__init__(name=name, seed=seed, port=port)
        self.model = None
        self.model_ready = asyncio.Event()

    async def setup_model(self):
        """Setup model asynchronously"""
        # This runs in background while agent handles other tasks
        try:
            # Load model weights
            weights_path = Path("models/xception_weights.pth")
            if weights_path.exists():
                self.model = torch.load(weights_path)
                self.model.eval()
                self.model_ready.set()
                print(f"✅ {self.name}: Model loaded successfully")
            else:
                print(f"❌ {self.name}: Model weights not found")
        except Exception as e:
            print(f"❌ {self.name}: Error loading model: {e}")

    @agent.on_event("startup")
    async def startup(self, ctx: Context):
        """Initialize model on startup"""
        print(f"🚀 {self.name}: Starting up...")
        # Start model setup in background
        asyncio.create_task(self.setup_model())

    @agent.on_message(model=ImageRequest)
    async def process_image(self, ctx: Context, sender: str, msg: ImageRequest):
        """Process image request"""
        # Wait for model to be ready
        await self.model_ready.wait()
        
        try:
            # Process image
            result = await self._analyze_image(msg.image_path)
            
            # Send result back
            await ctx.send(sender, AnalysisResult(
                task_id=msg.task_id,
                confidence_score=result['confidence'],
                is_fake=result['is_fake'],
                analysis_details=result['details']
            ))
        except Exception as e:
            print(f"❌ {self.name}: Error processing image: {e}")

# Usage Example:
async def main():
    # Create model agent
    model_agent = ModelAgent(
        name="deepfake_detector",
        seed="model_seed_2024",
        port=8001
    )

    # Start agent
    await model_agent.run()

if __name__ == "__main__":
    asyncio.run(main())
