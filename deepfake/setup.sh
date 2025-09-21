#!/bin/bash

echo "🚀 Setting up Deepfake Detection System..."

# Create and activate virtual environment
echo "📦 Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install PyTorch and torchvision first
echo "🔥 Installing PyTorch and torchvision..."
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Install core dependencies
echo "📚 Installing core dependencies..."
pip install numpy==1.24.3
pip install opencv-python
pip install pillow
pip install fpdf
pip install flask flask-socketio python-socketio python-engineio eventlet
pip install uagents==0.22.8

# Install the project
echo "🔧 Installing project..."
pip install -e .

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p models uploads outputs reports logs

# Download models
echo "🤖 Downloading models..."

# Download face detection model
echo "Downloading face detection model..."
wget -O models/haarcascade_frontalface_default.xml https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml

# Initialize deepfake detection model
echo "Initializing deepfake detection model..."
python - << 'END_PYTHON'
import torch
import torch.nn as nn
import torch.nn.init as init
import os

class DeepfakeDetectionModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 128, 3, padding=1)
        self.conv3 = nn.Conv2d(128, 256, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(256 * 28 * 28, 512)
        self.fc2 = nn.Linear(512, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = x.view(-1, 256 * 28 * 28)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Create model
model = DeepfakeDetectionModel()

# Initialize weights using Xavier initialization
def init_weights(m):
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
        init.xavier_uniform_(m.weight)
        if m.bias is not None:
            init.zeros_(m.bias)

model.apply(init_weights)

# Save model
os.makedirs('models', exist_ok=True)
torch.save(model.state_dict(), 'models/deepfake_detection.pth')
print("Deepfake detection model initialized and saved!")
END_PYTHON

echo "✅ Setup complete! You can now run the system with:"
echo "source venv/bin/activate"
echo "cd web_app"
echo "python app.py"