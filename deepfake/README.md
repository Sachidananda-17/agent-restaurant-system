# Automated Deepfake Detection System

A multi-agent system for detecting and analyzing potential deepfake images using deep learning and forensic analysis.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 (recommended) or later
- Git
- macOS, Linux, or Windows

### One-Step Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/agent-restaurant-system.git
cd agent-restaurant-system/deepfake

# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

### Manual Setup (if the setup script doesn't work)

1. Create and activate virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install PyTorch and dependencies:
   ```bash
   pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
   pip install numpy==1.24.3
   pip install -e .
   ```

3. Create necessary directories:
   ```bash
   mkdir -p models uploads outputs reports logs
   ```

4. Download and initialize models:
   ```bash
   python download_models.py
   ```

### Running the System

1. Activate virtual environment (if not already activated):
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Start the web application:
   ```bash
   cd web_app
   python app.py
   ```

3. Open your browser and go to:
   - http://localhost:5000 (or http://localhost:5001 if port 5000 is in use)

## 📁 Project Structure

```
deepfake/
├── agents/                 # Multi-agent system components
│   ├── base_agent.py      # Base agent class
│   ├── coordinator_agent.py    # Orchestrates analysis workflow
│   ├── image_processor_agent.py    # Handles deepfake detection
│   ├── forensic_analyzer_agent.py  # Performs forensic analysis
│   └── report_generator_agent.py   # Generates analysis reports
├── web_app/               # Web interface
│   ├── app.py            # Flask application
│   ├── templates/        # HTML templates
│   └── static/           # CSS, JS, and other static files
├── models/               # AI models and weights
├── uploads/              # Temporary storage for uploaded images
├── outputs/              # Analysis outputs and visualizations
├── reports/              # Generated PDF reports
├── logs/                 # System logs
├── setup.py             # Package configuration
├── setup.sh             # Automated setup script
└── download_models.py    # Model download and initialization
```

## 🔍 System Components

1. **Web Interface**
   - Upload images for analysis
   - Real-time progress tracking
   - Download detailed PDF reports

2. **Agent System**
   - Coordinator Agent (Port 8000)
   - Image Processor Agent (Port 8001)
   - Forensic Analyzer Agent (Port 8002)
   - Report Generator Agent (Port 8003)

3. **Analysis Features**
   - Deep learning-based deepfake detection
   - Face detection and analysis
   - Error Level Analysis (ELA)
   - Metadata analysis
   - Compression pattern analysis
   - Noise pattern analysis

## 📊 Analysis Report

The system generates comprehensive PDF reports including:
- Executive Summary
- Technical Analysis
- Forensic Analysis
- Visual Analysis with heatmaps
- Metadata Analysis
- Recommendations

## 🔧 Troubleshooting

1. **Port in Use**
   - The system will automatically try the next available port
   - Default: 5000, Fallback: 5001

2. **Model Download Issues**
   - Check internet connection
   - Ensure enough disk space
   - Try running `python download_models.py` manually

3. **Import Errors**
   - Ensure you're in the virtual environment
   - Try reinstalling dependencies: `pip install -e .`

4. **Memory Issues**
   - Reduce image size before upload
   - Close other memory-intensive applications

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.