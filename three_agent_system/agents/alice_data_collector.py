"""
Alice - Data Collector & Problem Identifier Agent
Role: Collects user preferences, location data, and search criteria
Collaborates with Bob (Analyzer) and Charlie (Decision Maker)
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from uagents import Agent, Context
import datetime
import json
import random

# Import our shared models and config
from config.message_models import *
from config.agent_config import AGENTS, SAMPLE_RESTAURANT_DATA

# === ALICE AGENT SETUP ===
alice = Agent(
    name=AGENTS["alice"]["name"],
    seed=AGENTS["alice"]["seed"], 
    port=AGENTS["alice"]["port"],
    endpoint=[AGENTS["alice"]["endpoint"]]
)

# Store addresses of Bob and Charlie (will get from running agents)
BOB_ADDRESS = ""    # Will be populated when Bob starts
CHARLIE_ADDRESS = "" # Will be populated when Charlie starts

# Alice's working memory for tasks
alice_memory = {
    "current_tasks": {},
    "completed_tasks": [],
    "team_addresses": {}
}

@alice.on_event("startup")
async def alice_startup(ctx: Context):
    """Alice introduces herself and her capabilities"""
    ctx.logger.info("🔍 Alice Data Collector Agent Starting...")
    ctx.logger.info(f"📍 Alice Address: {alice.address}")
    ctx.logger.info("🎯 Role: Data Collection & Problem Identification")
    ctx.logger.info("🤝 Looking for Bob (Analyzer) and Charlie (Coordinator)...")
    ctx.logger.info("📋 Capabilities:")
    ctx.logger.info("   • User preference analysis")  
    ctx.logger.info("   • Location data processing")
    ctx.logger.info("   • Search criteria optimization")
    ctx.logger.info("🚀 Alice is ready for collaborative tasks!")

# === TASK INITIATION ===
@alice.on_interval(period=30.0)  # Start a new task every 30 seconds for demo
async def initiate_collaboration_task(ctx: Context):
    """Alice initiates a collaborative restaurant recommendation task"""
    
    # Simulate different user requests
    sample_requests = [
        "Find me a romantic restaurant for date night",
        "I want family-friendly pizza place nearby", 
        "Looking for authentic sushi with good ratings",
        "Need a budget-friendly lunch spot downtown",
        "Find upscale French restaurant for business dinner"
    ]
    
    task_id = f"task_{datetime.datetime.now().strftime('%H%M%S')}"
    user_request = random.choice(sample_requests)
    
    ctx.logger.info(f"🎯 Alice initiating new task: {task_id}")
    ctx.logger.info(f"📝 User Request: {user_request}")
    
    # Alice collects and processes user data
    collected_data = collect_user_data(user_request)
    
    alice_memory["current_tasks"][task_id] = {
        "status": "data_collected",
        "user_request": user_request,
        "collected_data": collected_data,
        "start_time": datetime.datetime.now().isoformat()
    }
    
    # Send data to Bob for analysis
    if BOB_ADDRESS:
        data_message = DataCollection(
            task_id=task_id,
            user_preferences=collected_data["preferences"],
            location_data=collected_data["location"],
            search_criteria=collected_data["criteria"],
            confidence_score=collected_data["confidence"],
            timestamp=datetime.datetime.now().isoformat(),
            sender="Alice"
        )
        
        try:
            await ctx.send(BOB_ADDRESS, data_message)
            ctx.logger.info(f"📤 Data sent to Bob for analysis: {task_id}")
        except Exception as e:
            ctx.logger.error(f"❌ Failed to send data to Bob: {str(e)}")
    else:
        ctx.logger.warning("⚠️ Bob's address not yet known - saving data for later")

def collect_user_data(user_request: str) -> dict:
    """Simulate Alice's data collection capabilities"""
    
    # Alice analyzes the request and extracts preferences
    preferences = {}
    location = {}
    criteria = {}
    
    # Simple keyword analysis (in real system, this would be much more sophisticated)
    request_lower = user_request.lower()
    
    # Cuisine preferences
    if "pizza" in request_lower:
        preferences["cuisine"] = "Italian"
        preferences["specific"] = "pizza"
    elif "sushi" in request_lower:
        preferences["cuisine"] = "Japanese" 
        preferences["specific"] = "sushi"
    elif "french" in request_lower:
        preferences["cuisine"] = "French"
    elif "burger" in request_lower:
        preferences["cuisine"] = "American"
        preferences["specific"] = "burgers"
    else:
        preferences["cuisine"] = "any"
    
    # Budget analysis
    if "budget" in request_lower or "cheap" in request_lower:
        preferences["price_range"] = "$"
    elif "upscale" in request_lower or "business" in request_lower:
        preferences["price_range"] = "$$$+"
    else:
        preferences["price_range"] = "$$"
    
    # Occasion analysis
    if "romantic" in request_lower or "date" in request_lower:
        preferences["occasion"] = "romantic"
    elif "family" in request_lower:
        preferences["occasion"] = "family"
    elif "business" in request_lower:
        preferences["occasion"] = "business"
    else:
        preferences["occasion"] = "casual"
    
    # Location preferences
    if "downtown" in request_lower:
        location["area"] = "Downtown"
    elif "nearby" in request_lower:
        location["area"] = "within_2_miles"
    else:
        location["area"] = "city_wide"
    
    # Search criteria
    criteria["sort_by"] = "rating"
    criteria["min_rating"] = 3.5
    criteria["max_results"] = 5
    
    confidence = calculate_confidence(preferences, location, criteria)
    
    return {
        "preferences": preferences,
        "location": location, 
        "criteria": criteria,
        "confidence": confidence
    }

def calculate_confidence(preferences: dict, location: dict, criteria: dict) -> float:
    """Calculate Alice's confidence in her data collection"""
    confidence = 0.5  # Base confidence
    
    # More specific preferences = higher confidence
    if preferences.get("cuisine") != "any":
        confidence += 0.2
    if "specific" in preferences:
        confidence += 0.15
    if "occasion" in preferences:
        confidence += 0.1
    
    # Location specificity adds confidence
    if location.get("area") != "city_wide":
        confidence += 0.1
        
    return min(confidence, 1.0)

# === COLLABORATION HANDLERS ===

@alice.on_message(model=AnalysisRequest)
async def handle_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """Bob requests additional data from Alice"""
    ctx.logger.info(f"📨 Analysis request from Bob for task: {msg.task_id}")
    ctx.logger.info(f"🔍 Requested data: {msg.requested_data}")
    
    # Alice gathers additional data as requested
    additional_data = {}
    for data_type in msg.requested_data:
        if data_type == "user_reviews":
            additional_data[data_type] = get_user_reviews_data()
        elif data_type == "location_details":
            additional_data[data_type] = get_location_details()
        elif data_type == "pricing_info":
            additional_data[data_type] = get_pricing_details()
    
    # Send back enhanced data collection
    enhanced_data = DataCollection(
        task_id=msg.task_id,
        user_preferences=alice_memory["current_tasks"][msg.task_id]["collected_data"]["preferences"],
        location_data=alice_memory["current_tasks"][msg.task_id]["collected_data"]["location"],
        search_criteria={**alice_memory["current_tasks"][msg.task_id]["collected_data"]["criteria"], 
                        "additional_data": additional_data},
        confidence_score=0.9,  # Higher confidence with additional data
        timestamp=datetime.datetime.now().isoformat(),
        sender="Alice"
    )
    
    try:
        await ctx.send(sender, enhanced_data)
        ctx.logger.info(f"📤 Enhanced data sent to Bob: {msg.task_id}")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send enhanced data: {str(e)}")

def get_user_reviews_data():
    """Simulate gathering user review data"""
    return {
        "review_sentiment": "positive",
        "common_complaints": ["slow_service", "noise_level"],
        "popular_features": ["atmosphere", "food_quality"]
    }

def get_location_details():
    """Simulate gathering location details"""
    return {
        "parking": "street_parking_available",
        "accessibility": "wheelchair_accessible", 
        "nearby_attractions": ["shopping_center", "movie_theater"]
    }

def get_pricing_details():
    """Simulate gathering pricing information"""
    return {
        "average_cost_per_person": 25,
        "happy_hour": "3-6 PM",
        "specials": ["lunch_combo", "weekend_brunch"]
    }

@alice.on_message(model=FinalDecision) 
async def handle_final_decision(ctx: Context, sender: str, msg: FinalDecision):
    """Receive final decision from Charlie"""
    ctx.logger.info(f"🎉 Final decision received for task: {msg.task_id}")
    ctx.logger.info(f"👑 Charlie's choice: {msg.final_choice['name']}")
    ctx.logger.info(f"💭 Reasoning: {msg.decision_reasoning}")
    ctx.logger.info(f"📊 Confidence: {msg.confidence_score:.2f}")
    
    # Move task to completed 
    if msg.task_id in alice_memory["current_tasks"]:
        completed_task = alice_memory["current_tasks"].pop(msg.task_id)
        completed_task["final_decision"] = msg.final_choice
        completed_task["completion_time"] = datetime.datetime.now().isoformat()
        alice_memory["completed_tasks"].append(completed_task)
        
        ctx.logger.info("✅ Task completed and archived by Alice")

# === TEAM DISCOVERY ===
@alice.on_message(model=StatusUpdate)
async def handle_team_discovery(ctx: Context, sender: str, msg: StatusUpdate):
    """Discover other team members"""
    global BOB_ADDRESS, CHARLIE_ADDRESS
    if msg.sender == "Bob" and not BOB_ADDRESS:
        BOB_ADDRESS = sender
        alice_memory["team_addresses"]["bob"] = sender
        ctx.logger.info(f"🤝 Bob discovered! Address: {sender}")
    elif msg.sender == "Charlie" and not CHARLIE_ADDRESS:
        CHARLIE_ADDRESS = sender
        alice_memory["team_addresses"]["charlie"] = sender
        ctx.logger.info(f"🤝 Charlie discovered! Address: {sender}")

if __name__ == "__main__":
    print("🔍 Starting Alice - Data Collector Agent")
    print(f"📍 Alice will run on port {AGENTS['alice']['port']}")
    alice.run()
