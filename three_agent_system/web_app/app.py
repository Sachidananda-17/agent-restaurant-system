"""
Flask Web Application for 3-Agent Restaurant Recommendation System
Real-time dashboard showing Alice, Bob, Charlie intercommunication
"""

from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import json
import asyncio
import threading
import time
from datetime import datetime
from uagents import Agent, Context, Model
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# === MESSAGE MODELS ===
class DataCollection(Model):
    task_id: str
    user_preferences: dict
    location_data: dict
    search_criteria: dict
    confidence_score: float
    timestamp: str
    sender: str = "Alice"

class AnalysisResult(Model):
    task_id: str
    analysis_summary: str
    recommendations: list
    confidence_scores: dict
    supporting_data: dict
    timestamp: str
    sender: str = "Bob"

class FinalDecision(Model):
    task_id: str
    final_choice: dict
    decision_reasoning: str
    confidence_score: float
    all_participants: list
    timestamp: str
    sender: str = "Charlie"

class UserRequest(Model):
    task_id: str
    user_request: str
    preferences: dict
    location: str
    timestamp: str

# Your deployed agent addresses
DEPLOYED_AGENTS = {
    "alice": "agent1qv7cp9rmuln4ay27sxr7wfe5027er9xm3kx3fweckk55avl5xwhuv2rwqs3",
    "bob": "agent1qfktux3y85zl4lajwh5shm7paputfddyrevdqq3stn7n65mgz9yxzf0sknu",
    "charlie": "agent1q28h0anmn790wka6r7ws23jnt62546yza07q9cr7y9t988dzn7hy7se8khy"
}

# Global data storage
dashboard_data = {
    "active_workflows": {},
    "completed_workflows": [],
    "statistics": {
        "total_workflows": 0,
        "completed_workflows": 0,
        "alice_messages": 0,
        "bob_analyses": 0,
        "charlie_decisions": 0,
        "total_processing_time": 0.0,
        "average_processing_time": 0.0
    },
    "agent_status": {
        "alice": {"online": True, "last_seen": datetime.now().isoformat()},
        "bob": {"online": True, "last_seen": datetime.now().isoformat()},
        "charlie": {"online": True, "last_seen": datetime.now().isoformat()}
    }
}

# Create web monitoring agent
web_monitor = Agent(
    name="web_dashboard_monitor",
    seed="web_monitor_2024"
)

@web_monitor.on_event("startup")
async def web_monitor_startup(ctx: Context):
    """Web monitor starts up"""
    ctx.logger.info("🌐 Web Dashboard Monitor starting...")
    emit_to_dashboard("system", "Web Dashboard Monitor connected to Agentverse")

@web_monitor.on_message(model=DataCollection)
async def handle_alice_response(ctx: Context, sender: str, msg: DataCollection):
    """Handle Alice's response"""
    task_id = msg.task_id
    
    response_data = {
        "agent": "alice",
        "task_id": task_id,
        "confidence": msg.confidence_score,
        "preferences": msg.user_preferences,
        "location": msg.location_data,
        "timestamp": msg.timestamp
    }
    
    dashboard_data["statistics"]["alice_messages"] += 1
    dashboard_data["agent_status"]["alice"]["last_seen"] = datetime.now().isoformat()
    
    if task_id in dashboard_data["active_workflows"]:
        dashboard_data["active_workflows"][task_id]["alice_response"] = response_data
        dashboard_data["active_workflows"][task_id]["status"] = "alice_completed"
    
    emit_to_dashboard("alice_response", response_data)
    ctx.logger.info(f"Alice response received: {task_id}")

@web_monitor.on_message(model=AnalysisResult)
async def handle_bob_response(ctx: Context, sender: str, msg: AnalysisResult):
    """Handle Bob's response"""
    task_id = msg.task_id
    
    response_data = {
        "agent": "bob",
        "task_id": task_id,
        "analysis_summary": msg.analysis_summary,
        "recommendations": msg.recommendations,
        "confidence_scores": msg.confidence_scores,
        "processing_time": msg.supporting_data.get("processing_time_seconds", 0),
        "timestamp": msg.timestamp
    }
    
    dashboard_data["statistics"]["bob_analyses"] += 1
    dashboard_data["agent_status"]["bob"]["last_seen"] = datetime.now().isoformat()
    
    if task_id in dashboard_data["active_workflows"]:
        dashboard_data["active_workflows"][task_id]["bob_response"] = response_data
        dashboard_data["active_workflows"][task_id]["status"] = "bob_completed"
    
    emit_to_dashboard("bob_response", response_data)
    ctx.logger.info(f"Bob response received: {task_id}")

@web_monitor.on_message(model=FinalDecision)
async def handle_charlie_response(ctx: Context, sender: str, msg: FinalDecision):
    """Handle Charlie's response"""
    task_id = msg.task_id
    
    response_data = {
        "agent": "charlie",
        "task_id": task_id,
        "final_choice": msg.final_choice,
        "decision_reasoning": msg.decision_reasoning,
        "confidence_score": msg.confidence_score,
        "timestamp": msg.timestamp
    }
    
    dashboard_data["statistics"]["charlie_decisions"] += 1
    dashboard_data["agent_status"]["charlie"]["last_seen"] = datetime.now().isoformat()
    
    # Complete the workflow
    if task_id in dashboard_data["active_workflows"]:
        workflow = dashboard_data["active_workflows"][task_id]
        workflow["charlie_response"] = response_data
        workflow["status"] = "completed"
        workflow["end_time"] = datetime.now()
        
        # Calculate processing time
        if "start_time" in workflow:
            processing_time = (workflow["end_time"] - workflow["start_time"]).total_seconds()
            workflow["processing_time"] = processing_time
            
            dashboard_data["statistics"]["total_processing_time"] += processing_time
            dashboard_data["statistics"]["completed_workflows"] += 1
            
            # Calculate average
            if dashboard_data["statistics"]["completed_workflows"] > 0:
                dashboard_data["statistics"]["average_processing_time"] = (
                    dashboard_data["statistics"]["total_processing_time"] / 
                    dashboard_data["statistics"]["completed_workflows"]
                )
        
        # Move to completed workflows
        dashboard_data["completed_workflows"].append(workflow)
        del dashboard_data["active_workflows"][task_id]
    
    emit_to_dashboard("charlie_response", response_data)
    emit_to_dashboard("workflow_completed", {"task_id": task_id, "processing_time": processing_time})
    ctx.logger.info(f"Charlie response received and workflow completed: {task_id}")

def emit_to_dashboard(event, data):
    """Emit data to connected dashboard clients"""
    try:
        socketio.emit(event, data)
    except Exception as e:
        logging.error(f"Failed to emit to dashboard: {e}")

def run_agent_monitor():
    """Run the agent monitor in a separate thread"""
    try:
        asyncio.run(web_monitor.run())
    except Exception as e:
        logging.error(f"Agent monitor error: {e}")

# Routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html', 
                         agents=DEPLOYED_AGENTS, 
                         initial_data=dashboard_data)

@app.route('/api/status')
def get_status():
    """Get current system status"""
    return jsonify({
        "agents": DEPLOYED_AGENTS,
        "statistics": dashboard_data["statistics"],
        "agent_status": dashboard_data["agent_status"],
        "active_workflows": len(dashboard_data["active_workflows"])
    })

@app.route('/api/send_request', methods=['POST'])
def send_request():
    """Send a test request to Alice"""
    try:
        data = request.json
        user_request = data.get('request', 'Find a good restaurant')
        preferences = data.get('preferences', {})
        location = data.get('location', 'downtown')
        
        task_id = f"web_{int(time.time())}"
        
        # Create workflow tracking
        dashboard_data["active_workflows"][task_id] = {
            "task_id": task_id,
            "start_time": datetime.now(),
            "user_request": user_request,
            "preferences": preferences,
            "location": location,
            "status": "initiated"
        }
        
        dashboard_data["statistics"]["total_workflows"] += 1
        
        # In a real implementation, this would send to Alice via uAgents
        # For now, we'll simulate the response
        emit_to_dashboard("new_request", {
            "task_id": task_id,
            "request": user_request,
            "preferences": preferences,
            "location": location
        })
        
        return jsonify({"success": True, "task_id": task_id})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/workflows')
def get_workflows():
    """Get workflow history"""
    return jsonify({
        "active": list(dashboard_data["active_workflows"].values()),
        "completed": dashboard_data["completed_workflows"][-10:]  # Last 10
    })

# Socket.IO events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'data': 'Connected to 3-Agent Dashboard'})
    emit('initial_data', dashboard_data)

@socketio.on('request_update')
def handle_request_update():
    """Send current data to client"""
    emit('data_update', dashboard_data)

@socketio.on('trigger_test')
def handle_trigger_test(data):
    """Handle test request from client"""
    user_request = data.get('request', 'Find a good restaurant for dinner')
    preferences = data.get('preferences', {'cuisine': 'any', 'price': '$$'})
    location = data.get('location', 'downtown')
    
    # Simulate sending request
    emit_to_dashboard('system', f"Test request initiated: {user_request}")

if __name__ == '__main__':
    # Start agent monitor in background thread
    monitor_thread = threading.Thread(target=run_agent_monitor, daemon=True)
    monitor_thread.start()
    
    print("🌐 Starting 3-Agent Dashboard Web Application")
    print("📊 Real-time monitoring of Alice, Bob, Charlie")
    print("🚀 Access dashboard at: http://localhost:5000")
    print()
    
    # Run Flask app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
