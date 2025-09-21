"""
Agent that uses lightweight models suitable for Agentverse
"""

from uagents import Agent, Context, Model
import onnxruntime as ort
import numpy as np
from PIL import Image
import cv2

class LightweightRequest(Model):
    """Request for lightweight model prediction"""
    image_path: str
    task_id: str

class LightweightResponse(Model):
    """Response from lightweight model"""
    task_id: str
    prediction: dict
    status: str

class LightweightModelAgent(Agent):
    """Agent using lightweight ONNX models"""
    
    def __init__(self, name: str, seed: str, port: int):
        super().__init__(name=name, seed=seed, port=port)
        self.model = None
        
    @agent.on_event("startup")
    async def startup(self, ctx: Context):
        """Load lightweight ONNX model on startup"""
        try:
            # Load optimized ONNX model (much smaller than PyTorch)
            self.model = ort.InferenceSession("models/lightweight_model.onnx")
            print(f"✅ {self.name}: Lightweight model loaded")
        except Exception as e:
            print(f"❌ {self.name}: Error loading model: {e}")

    @agent.on_message(model=LightweightRequest)
    async def handle_prediction(self, ctx: Context, sender: str, msg: LightweightRequest):
        """Handle prediction with lightweight model"""
        try:
            # Process image
            image = Image.open(msg.image_path)
            image = image.resize((224, 224))
            input_data = np.array(image).astype(np.float32)
            input_data = input_data.transpose(2, 0, 1)
            input_data = input_data / 255.0
            input_data = input_data[np.newaxis, :]

            # Run inference
            outputs = self.model.run(None, {"input": input_data})
            prediction = outputs[0][0]

            await ctx.send(sender, LightweightResponse(
                task_id=msg.task_id,
                prediction={
                    "is_fake": bool(prediction[0] > 0.5),
                    "confidence": float(prediction[0])
                },
                status="success"
            ))
        except Exception as e:
            await ctx.send(sender, LightweightResponse(
                task_id=msg.task_id,
                prediction={},
                status=f"error: {str(e)}"
            ))
