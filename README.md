# Deepfake Detection System

A multi-agent system for detecting deepfake images using advanced AI and forensic analysis.

## 🚀 Quick Start

```bash
# 1. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install core dependencies
pip install setuptools wheel
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Start the web application
cd web_app
python app.py
```

Then open http://localhost:5000 in your browser.

## 🛠️ System Requirements

- Python 3.8 or higher
- 8GB RAM (minimum)
- 2GB free disk space
- Modern web browser (Chrome, Firefox, Safari)

## 🤖 System Architecture

### Agents

1. **Coordinator Agent** (Port 8000)
   - Manages workflow
   - Coordinates between agents
   - Handles task distribution

2. **Image Processor Agent** (Port 8001)
   - Deep learning-based detection
   - Face detection
   - Heatmap generation
   - Confidence scoring

3. **Forensic Analyzer Agent** (Port 8002)
   - Metadata analysis
   - Error Level Analysis (ELA)
   - Compression artifact analysis
   - Noise pattern analysis

4. **Report Generator Agent** (Port 8003)
   - PDF report generation
   - Visual evidence compilation
   - Findings summarization

### Web Interface

- Real-time progress monitoring
- WebSocket-based updates
- Drag-and-drop file upload
- Interactive results display

## 📁 Project Structure

```
deepfake-detection-system/
├── agents/                  # Agent implementations
│   ├── base_agent.py
│   ├── coordinator_agent.py
│   ├── image_processor_agent.py
│   ├── forensic_analyzer_agent.py
│   └── report_generator_agent.py
├── web_app/                 # Web interface
│   ├── app.py
│   └── templates/
│       └── index.html
├── models/                  # Model storage
├── uploads/                # Uploaded images
├── reports/                # Generated reports
└── config.py              # System configuration
```

## 🔍 Usage

1. **Upload Image**
   - Drag and drop or click to select
   - Supported formats: JPG, PNG, BMP
   - Max file size: 10MB

2. **Analysis Process**
   - Image processing (deepfake detection)
   - Forensic analysis
   - Report generation

3. **View Results**
   - Real-time progress updates
   - Confidence scores
   - Forensic findings
   - Download detailed PDF report

## 🔧 Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Change ports in config.py if needed
   WEB_CONFIG = {
       "port": 5000  # Change to available port
   }
   ```

2. **Memory Issues**
   - Close other applications
   - Reduce image size if needed
   - Ensure sufficient free RAM

3. **Model Loading Issues**
   ```bash
   # Verify model directory exists
   mkdir -p models
   ```

### Error Messages

- "Port already in use": Change port in config.py
- "Memory error": Free up system memory
- "Model not found": Check models directory

## 📊 Example Output

The system generates:
1. Deepfake confidence score (0-100%)
2. Highlighted suspicious areas
3. Forensic analysis report
4. Detailed PDF documentation

## 🔒 Security Notes

- All processing is done locally
- No data sent to external servers
- Reports stored locally in reports/
- Uploaded images stored in uploads/

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📝 License

MIT License - feel free to use and modify

## 🆘 Support

For issues and questions:
1. Check troubleshooting guide
2. Review error logs
3. Create GitHub issue

## 🔄 Updates

To update the system:
```bash
git pull
pip install -r requirements.txt
```

## 🏃‍♂️ Running in Production

For production deployment:
1. Use a production WSGI server (e.g., Gunicorn)
2. Set up proper security measures
3. Configure logging
4. Use environment variables for sensitive data

## 🧪 Testing

```bash
# Run tests
python -m pytest tests/
```

## 📈 Performance

- Average processing time: 5-10 seconds
- Memory usage: 2-4GB RAM
- CPU usage: 60-80% during analysis
