"""
Alice Agent - Agentverse Production Version
🔍 Data Collector & Problem Identifier for Global Restaurant Recommendations
🌐 Deployed on Fetch.ai Agentverse Platform
"""

from uagents import Agent, Context, Model
import datetime
import random

# === MESSAGE MODELS ===
class DataCollection(Model):
    task_id: str
    user_preferences: dict
    location_data: dict
    search_criteria: dict
    confidence_score: float
    timestamp: str
    sender: str = "Alice"

class AnalysisRequest(Model):
    task_id: str
    requested_data: list
    analysis_focus: str
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

class StatusUpdate(Model):
    task_id: str
    status: str
    progress_percentage: int
    message: str
    timestamp: str
    sender: str

# === AGENTVERSE ALICE AGENT ===
alice = Agent(
    name="alice_global_restaurant_collector",
    seed="alice_production_agentverse_seed_2024"
    # 🌐 No port or endpoint - Agentverse manages automatically
)

# Global team discovery
BOB_ADDRESS = ""
CHARLIE_ADDRESS = ""
alice_global_memory = {
    "completed_tasks": [],
    "active_collaborations": {},
    "global_stats": {"tasks_completed": 0, "success_rate": 0.0}
}

# Enhanced global restaurant requests
GLOBAL_REQUESTS = [
    "Find romantic fine dining restaurant for anniversary",
    "Family-friendly pizza place with kids menu", 
    "Authentic sushi restaurant with fresh fish",
    "Business lunch venue in financial district",
    "Upscale French bistro with wine pairing",
    "Casual Mexican restaurant with outdoor seating",
    "Vegetarian Indian restaurant with spice options",
    "Trendy rooftop bar with city views",
    "Traditional steakhouse for celebration dinner",
    "Health-conscious cafe with organic options"
]

@alice.on_event("startup")
async def alice_global_startup(ctx: Context):
    """Alice announces availability on global Agentverse network"""
    ctx.logger.info("🌐 Alice Restaurant Collector starting on Agentverse!")
    ctx.logger.info(f"📍 Global Address: {alice.address}")
    ctx.logger.info("🔍 Specialization: Restaurant data collection and user preference analysis")
    ctx.logger.info("🤝 Seeking Bob (Analyzer) and Charlie (Coordinator) for collaboration")
    ctx.logger.info("🌟 Ready for global restaurant recommendation tasks!")
    
    # Broadcast to global network
    startup_status = StatusUpdate(
        task_id="alice_global_startup",
        status="online_and_available",
        progress_percentage=100,
        message="Alice Restaurant Collector ready for global collaboration",
        timestamp=datetime.datetime.now().isoformat(),
        sender="Alice"
    )
    
    ctx.logger.info("📡 Broadcasting availability on Agentverse global network")

@alice.on_interval(period=90.0)  # Every 90 seconds for global demo
async def initiate_global_task(ctx: Context):
    """Generate global restaurant recommendation tasks"""
    
    # Wait for full team
    if not (BOB_ADDRESS and CHARLIE_ADDRESS):
        ctx.logger.info("🔍 Alice waiting for global team assembly...")
        ctx.logger.info(f"   Bob: {'✅ Connected' if BOB_ADDRESS else '⏳ Searching'}")
        ctx.logger.info(f"   Charlie: {'✅ Connected' if CHARLIE_ADDRESS else '⏳ Searching'}")
        return
    
    # Generate global task
    task_id = f"global_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    user_request = random.choice(GLOBAL_REQUESTS)
    
    ctx.logger.info("🌐 ===== GLOBAL COLLABORATION INITIATED =====")
    ctx.logger.info(f"🎯 Task ID: {task_id}")
    ctx.logger.info(f"👤 Global User Request: '{user_request}'")
    
    # Enhanced global data collection
    collected_data = collect_global_user_data(user_request)
    
    alice_global_memory["active_collaborations"][task_id] = {
        "start_time": datetime.datetime.now().isoformat(),
        "user_request": user_request,
        "status": "data_collected",
        "confidence": collected_data["confidence"]
    }
    
    ctx.logger.info("🔍 Alice: Global data collection complete")
    ctx.logger.info(f"   🍽️ Cuisine: {collected_data['preferences'].get('cuisine', 'Any')}")
    ctx.logger.info(f"   💰 Budget: {collected_data['preferences'].get('price_range', 'Any')}")
    ctx.logger.info(f"   🎭 Occasion: {collected_data['preferences'].get('occasion', 'Casual')}")
    ctx.logger.info(f"   📍 Location: {collected_data['location'].get('area', 'Global')}")
    ctx.logger.info(f"   📊 Confidence: {collected_data['confidence']:.2f}")
    
    # Send to global Bob
    global_data = DataCollection(
        task_id=task_id,
        user_preferences=collected_data["preferences"],
        location_data=collected_data["location"],
        search_criteria=collected_data["criteria"],
        confidence_score=collected_data["confidence"],
        timestamp=datetime.datetime.now().isoformat(),
        sender="Alice"
    )
    
    try:
        await ctx.send(BOB_ADDRESS, global_data)
        ctx.logger.info("🌐 ✅ Global data sent to Bob for analysis")
        alice_global_memory["active_collaborations"][task_id]["status"] = "sent_to_bob"
    except Exception as e:
        ctx.logger.error(f"❌ Global send failed: {str(e)}")

def collect_global_user_data(user_request: str) -> dict:
    """Enhanced global user data collection with intelligent analysis"""
    request_lower = user_request.lower()
    
    # Advanced preference extraction
    preferences = {
        "cuisine": "any",
        "occasion": "casual", 
        "price_range": "$$",
        "dietary_restrictions": [],
        "ambiance_preferences": [],
        "service_style": "table_service"
    }
    
    location = {
        "area": "city_center",
        "radius": "10km",
        "accessibility": "public_transport",
        "parking": "available"
    }
    
    criteria = {
        "min_rating": 4.0,
        "max_results": 5,
        "sort_by": "match_score",
        "include_reviews": True
    }
    
    # Intelligent analysis
    confidence = 0.7  # Base confidence
    
    # Cuisine detection
    cuisine_keywords = {
        "italian": "Italian", "pizza": "Italian", "pasta": "Italian",
        "french": "French", "bistro": "French", "wine": "French",
        "japanese": "Japanese", "sushi": "Japanese", "ramen": "Japanese",
        "chinese": "Chinese", "indian": "Indian", "mexican": "Mexican",
        "american": "American", "steakhouse": "American", "burger": "American"
    }
    
    for keyword, cuisine in cuisine_keywords.items():
        if keyword in request_lower:
            preferences["cuisine"] = cuisine
            confidence += 0.1
            break
    
    # Occasion analysis
    if any(word in request_lower for word in ["romantic", "anniversary", "date"]):
        preferences["occasion"] = "romantic"
        preferences["ambiance_preferences"].append("intimate_lighting")
        preferences["price_range"] = "$$$"
        confidence += 0.15
    elif any(word in request_lower for word in ["business", "meeting", "professional"]):
        preferences["occasion"] = "business"
        preferences["ambiance_preferences"].append("quiet_environment")
        preferences["price_range"] = "$$$"
        confidence += 0.15
    elif any(word in request_lower for word in ["family", "kids", "children"]):
        preferences["occasion"] = "family"
        preferences["ambiance_preferences"].append("family_friendly")
        preferences["service_style"] = "casual_dining"
        confidence += 0.1
    elif any(word in request_lower for word in ["celebration", "birthday", "party"]):
        preferences["occasion"] = "celebration"
        preferences["ambiance_preferences"].append("lively_atmosphere")
        confidence += 0.1
    
    # Price analysis  
    if any(word in request_lower for word in ["upscale", "fine", "luxury"]):
        preferences["price_range"] = "$$$$"
        confidence += 0.1
    elif any(word in request_lower for word in ["budget", "cheap", "affordable"]):
        preferences["price_range"] = "$"
        confidence += 0.1
    elif any(word in request_lower for word in ["mid-range", "moderate"]):
        preferences["price_range"] = "$$"
        confidence += 0.05
    
    # Special requirements
    if "vegetarian" in request_lower or "vegan" in request_lower:
        preferences["dietary_restrictions"].append("vegetarian_options")
        confidence += 0.1
    
    if "outdoor" in request_lower or "patio" in request_lower:
        preferences["ambiance_preferences"].append("outdoor_seating")
        confidence += 0.05
        
    
    if "rooftop" in request_lower:
        preferences["ambiance_preferences"].append("rooftop_dining")
        location["area"] = "downtown"  # Rooftops usually downtown
        confidence += 0.1
    
    return {
        "preferences": preferences,
        "location": location,
        "criteria": criteria,
        "confidence": min(confidence, 1.0)
    }

@alice.on_message(model=AnalysisRequest)
async def handle_global_analysis_request(ctx: Context, sender: str, msg: AnalysisRequest):
    """Handle requests for additional data from global Bob"""
    ctx.logger.info(f"📨 Global analysis request from Bob: {msg.task_id}")
    ctx.logger.info(f"🔍 Additional data requested: {msg.requested_data}")
    
    # Generate enhanced data
    enhanced_data = {}
    for data_type in msg.requested_data:
        if data_type == "user_reviews":
            enhanced_data[data_type] = {
                "sentiment": "positive",
                "common_complaints": ["slow_service", "noise_level"],
                "highlights": ["food_quality", "atmosphere", "value"]
            }
        elif data_type == "location_details":
            enhanced_data[data_type] = {
                "parking": "street_and_garage",
                "public_transport": "metro_accessible",
                "nearby": ["shopping", "entertainment"]
            }
        elif data_type == "pricing_details":
            enhanced_data[data_type] = {
                "average_cost": 45,
                "price_range": "$20-80 per person",
                "specials": ["happy_hour", "lunch_menu"]
            }
    
    # Send enhanced response
    try:
        # Create enhanced data collection response
        task_id = msg.task_id
        if task_id in alice_global_memory["active_collaborations"]:
            original_data = alice_global_memory["active_collaborations"][task_id]
            
            enhanced_response = DataCollection(
                task_id=task_id,
                user_preferences=original_data.get("preferences", {}),
                location_data=original_data.get("location", {}),
                search_criteria={"enhanced_data": enhanced_data},
                confidence_score=0.95,  # Higher confidence with additional data
                timestamp=datetime.datetime.now().isoformat(),
                sender="Alice"
            )
            
            await ctx.send(sender, enhanced_response)
            ctx.logger.info("🌐 ✅ Enhanced global data sent to Bob")
        
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send enhanced data: {str(e)}")

@alice.on_message(model=FinalDecision)
async def handle_global_final_decision(ctx: Context, sender: str, msg: FinalDecision):
    """Receive and process global final decisions"""
    ctx.logger.info("🌐 ===== GLOBAL COLLABORATION COMPLETED =====")
    ctx.logger.info(f"🎉 Final decision received: {msg.task_id}")
    ctx.logger.info(f"🏆 Global recommendation: {msg.final_choice.get('name', 'Unknown')}")
    ctx.logger.info(f"🍽️ Cuisine: {msg.final_choice.get('cuisine', 'N/A')}")
    ctx.logger.info(f"⭐ Rating: {msg.final_choice.get('rating', 'N/A')}")
    ctx.logger.info(f"💰 Price: {msg.final_choice.get('price', 'N/A')}")
    ctx.logger.info(f"📍 Location: {msg.final_choice.get('location', 'N/A')}")
    ctx.logger.info(f"📊 Decision confidence: {msg.confidence_score:.2f}")
    ctx.logger.info(f"💭 Reasoning: {msg.decision_reasoning}")
    
    # Update global memory
    if msg.task_id in alice_global_memory["active_collaborations"]:
        completed_task = alice_global_memory["active_collaborations"].pop(msg.task_id)
        completed_task.update({
            "completion_time": datetime.datetime.now().isoformat(),
            "final_decision": msg.final_choice,
            "confidence": msg.confidence_score,
            "status": "completed_successfully"
        })
        alice_global_memory["completed_tasks"].append(completed_task)
        alice_global_memory["global_stats"]["tasks_completed"] += 1
        
        # Calculate success rate
        total_tasks = len(alice_global_memory["completed_tasks"])
        successful_tasks = len([t for t in alice_global_memory["completed_tasks"] 
                              if t.get("confidence", 0) > 0.7])
        alice_global_memory["global_stats"]["success_rate"] = successful_tasks / total_tasks if total_tasks > 0 else 0
        
        ctx.logger.info(f"✅ Global task archived - Total completed: {total_tasks}")
        ctx.logger.info(f"📊 Global success rate: {alice_global_memory['global_stats']['success_rate']:.1%}")
        ctx.logger.info("🔄 Ready for next global collaboration")

@alice.on_message(model=StatusUpdate)
async def discover_global_team_members(ctx: Context, sender: str, msg: StatusUpdate):
    """Discover Bob and Charlie on the global Agentverse network"""
    global BOB_ADDRESS, CHARLIE_ADDRESS
    
    if msg.sender == "Bob" and not BOB_ADDRESS:
        BOB_ADDRESS = sender
        ctx.logger.info(f"🌐 ✅ Global Bob discovered: {sender[:16]}...")
        ctx.logger.info("🧠 Bob Analyzer connected to global network")
    elif msg.sender == "Charlie" and not CHARLIE_ADDRESS:
        CHARLIE_ADDRESS = sender
        ctx.logger.info(f"🌐 ✅ Global Charlie discovered: {sender[:16]}...")
        ctx.logger.info("👑 Charlie Coordinator connected to global network")
    
    # Check if team is complete
    if BOB_ADDRESS and CHARLIE_ADDRESS:
        ctx.logger.info("🎉 ===== GLOBAL TEAM ASSEMBLED =====")
        ctx.logger.info("🔍 Alice: Data Collector - READY")
        ctx.logger.info("🧠 Bob: Solution Analyzer - READY") 
        ctx.logger.info("👑 Charlie: Decision Coordinator - READY")
        ctx.logger.info("🌐 Global restaurant recommendation service ACTIVE!")

if __name__ == "__main__":
    print("🌐 Starting Alice on Agentverse Global Network")
    print(f"🔍 Alice will provide restaurant data collection services worldwide")
    alice.run()
