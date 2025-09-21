"""
Web Application for Deepfake Detection System
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_socketio import SocketIO, emit
import os
from datetime import datetime
import time
from pathlib import Path
import threading
import logging
from typing import Dict, Any
import json
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from config import WEB_CONFIG
from agents.coordinator_agent import CoordinatorAgent
from agents.image_processor_agent import ImageProcessorAgent
from agents.forensic_analyzer_agent import ForensicAnalyzerAgent
from agents.report_generator_agent import ReportGeneratorAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = WEB_CONFIG['max_file_size']
socketio = SocketIO(app, cors_allowed_origins="*")

# Create required directories
UPLOAD_DIR = Path("uploads")
REPORT_DIR = Path("reports")
for directory in [UPLOAD_DIR, REPORT_DIR]:
    directory.mkdir(exist_ok=True)

# Initialize agents
coordinator = CoordinatorAgent(
    name="coordinator_agent",
    seed="coordinator_seed_2024",
    port=8000
)

image_processor = ImageProcessorAgent(
    name="image_processor_agent",
    seed="image_processor_seed_2024",
    port=8001
)

forensic_analyzer = ForensicAnalyzerAgent(
    name="forensic_analyzer_agent",
    seed="forensic_analyzer_seed_2024",
    port=8002
)

report_generator = ReportGeneratorAgent(
    name="report_generator_agent",
    seed="report_generator_seed_2024",
    port=8003
)

# Global state
analysis_tasks = {}

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return Path(filename).suffix.lower() in WEB_CONFIG['allowed_extensions']

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                'error': f'Invalid file type. Allowed types: {", ".join(WEB_CONFIG["allowed_extensions"])}'
            }), 400
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{file.filename}"
        filepath = UPLOAD_DIR / filename
        
        # Save file
        file.save(str(filepath))
        
        # Generate task ID
        task_id = f"task_{timestamp}"
        
        # Initialize task tracking
        analysis_tasks[task_id] = {
            'status': 'uploaded',
            'filename': filename,
            'filepath': str(filepath),
            'timestamp': datetime.now().isoformat(),
            'progress': 0
        }
        
        # Start analysis
        threading.Thread(
            target=start_analysis,
            args=(task_id, str(filepath)),
            daemon=True
        ).start()
        
        return jsonify({
            'success': True,
            'task_id': task_id,
            'message': 'File uploaded successfully'
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/status/<task_id>')
def get_status(task_id: str):
    """Get task status"""
    if task_id not in analysis_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    return jsonify(analysis_tasks[task_id])

@app.route('/report/<task_id>')
def get_report(task_id: str):
    """Download analysis report"""
    if task_id not in analysis_tasks:
        return jsonify({'error': 'Task not found'}), 404
    
    task = analysis_tasks[task_id]
    if task['status'] != 'completed':
        return jsonify({'error': 'Report not ready'}), 400
    
    report_path = task.get('report_path')
    if not report_path or not Path(report_path).exists():
        return jsonify({'error': 'Report file not found'}), 404
    
    return send_file(
        report_path,
        as_attachment=True,
        download_name=f"deepfake_analysis_{task_id}.pdf"
    )

def start_analysis(task_id: str, filepath: str):
    """Start the analysis workflow"""
    try:
        print(f"\n🔍 Starting analysis for task {task_id}")
        print(f"📁 Processing file: {filepath}")
        
        # Update task status
        analysis_tasks[task_id].update({
            'status': 'processing',
            'stages': {
                'image_processing': False,
                'forensic_analysis': False,
                'report_generation': False
            }
        })
        print("✅ Task initialized")
        
        # Log task data
        print("\n📊 Current task data:")
        print(json.dumps(analysis_tasks[task_id], indent=2))
        
        emit_status_update(task_id)
        print("✅ Initial status update sent")
        
        # Start image processing
        print("\n🖼️ Starting Image Processing")
        analysis_tasks[task_id]['current_stage'] = 'image_processing'
        emit_status_update(task_id)
        try:
            result = image_processor._analyze_image(Path(filepath))
            print("✅ Image processing complete")
            print("Results:", json.dumps(result, indent=2))
            analysis_tasks[task_id]['stages']['image_processing'] = True
            analysis_tasks[task_id]['image_results'] = result
        except Exception as e:
            print(f"❌ Image processing failed: {str(e)}")
            raise
        
        # Start forensic analysis
        print("\n🔍 Starting Forensic Analysis")
        analysis_tasks[task_id]['current_stage'] = 'forensic_analysis'
        emit_status_update(task_id)
        try:
            metadata = forensic_analyzer._analyze_forensics(Path(filepath))
            print("✅ Forensic analysis complete")
            print("Results:", json.dumps(metadata, indent=2))
            analysis_tasks[task_id]['stages']['forensic_analysis'] = True
            analysis_tasks[task_id]['forensic_results'] = metadata
        except Exception as e:
            print(f"❌ Forensic analysis failed: {str(e)}")
            raise
        
        # Generate report
        print("\n📄 Starting Report Generation")
        analysis_tasks[task_id]['current_stage'] = 'report_generation'
        emit_status_update(task_id)
        try:
            report_path = report_generator._generate_report(
                task_id,
                analysis_tasks[task_id]['image_results'],
                analysis_tasks[task_id]['forensic_results'],
                filepath
            )
            print("✅ Report generation complete")
            print(f"Report saved to: {report_path}")
            analysis_tasks[task_id]['stages']['report_generation'] = True
            analysis_tasks[task_id]['report_path'] = report_path
        except Exception as e:
            print(f"❌ Report generation failed: {str(e)}")
            raise
        
        # Update final status
        analysis_tasks[task_id]['status'] = 'completed'
        analysis_tasks[task_id]['progress'] = 100
        emit_status_update(task_id)
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}")
        analysis_tasks[task_id]['status'] = 'error'
        analysis_tasks[task_id]['error'] = str(e)
        emit_status_update(task_id)

def emit_status_update(task_id: str):
    """Emit status update through WebSocket"""
    socketio.emit(
        'status_update',
        {
            'task_id': task_id,
            'data': analysis_tasks[task_id]
        }
    )

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'data': 'Connected to Deepfake Detection System'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info("Client disconnected")

if __name__ == '__main__':
    print("\n🔍 Starting Deepfake Detection System")
    print("=" * 50)
    
    # Get the project root directory and check for models
    PROJECT_ROOT = Path(__file__).parent.parent
    if not (
        (PROJECT_ROOT / "models/deepfake_detection.pth").exists() and 
        (PROJECT_ROOT / "models/xception_weights.pth").exists()
    ):
        print("⚠️  Models not found! Please run 'python download_models.py' first")
        print("=" * 50)
    
    port = WEB_CONFIG.get('port', 5000)
    print("System Components:")
    print(f"📊 Web Interface: http://localhost:{port}")
    print("   (If this port is in use, we'll try the next available port)")
    print("🤖 Agent Services:")
    print("   - Coordinator Agent: Port 8000 (internal)")
    print("   - Image Processor: Port 8001 (internal)")
    print("   - Forensic Analyzer: Port 8002 (internal)")
    print("   - Report Generator: Port 8003 (internal)")
    print("\n⚠️  Note: Only use the Web Interface URL to access the system")
    print("🛑 Press Ctrl+C to stop")
    print()
    
    try:
        # First try the configured port
        port = WEB_CONFIG.get('port', 5000)
        try:
            socketio.run(
                app,
                host=WEB_CONFIG['host'],
                port=port,
                debug=WEB_CONFIG['debug'],
                allow_unsafe_werkzeug=True
            )
        except OSError:
            # If port is in use, try the next available port
            print(f"Port {port} is in use, trying port {port + 1}")
            socketio.run(
                app,
                host=WEB_CONFIG['host'],
                port=port + 1,
                debug=WEB_CONFIG['debug'],
                allow_unsafe_werkzeug=True
            )
    except Exception as e:
        print(f"Error starting server: {e}")
        raise
