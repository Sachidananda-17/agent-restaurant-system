"""
Complete Response Monitor - See ALL 3 Agent Responses
🔍 Monitors Alice, Bob, Charlie intercommunication on Agentverse
📊 Shows real-time collaboration workflow with all responses
"""

from uagents import Agent, Context, Model
import datetime
import asyncio

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

class StatusUpdate(Model):
    task_id: str
    status: str
    progress_percentage: int
    message: str
    timestamp: str
    sender: str

# === MONITORING CLIENT ===
monitor = Agent(
    name="restaurant_response_monitor",
    seed="monitor_global_responses_2024"
)

# === YOUR DEPLOYED AGENT ADDRESSES ===
# Update these with your actual Agentverse addresses after deployment
DEPLOYED_AGENTS = {
    "alice": "agent1qv7cp9rmuln4ay27sxr7wfe5027er9xm3kx3fweckk55avl5xwhuv2rwqs3",  # Your deployed Alice address
    "bob": "agent1qfktux3y85zl4lajwh5shm7paputfddyrevdqq3stn7n65mgz9yxzf0sknu",                      # Update after Bob deployment  
    "charlie": "agent1q28h0anmn790wka6r7ws23jnt62546yza07q9cr7y9t988dzn7hy7se8khy"                   # Update after Charlie deployment
}

# Response tracking
response_tracker = {
    "active_tasks": {},
    "completed_workflows": [],
    "agent_stats": {
        "alice": {"messages_sent": 0, "last_seen": None},
        "bob": {"analyses_completed": 0, "last_seen": None}, 
        "charlie": {"decisions_made": 0, "last_seen": None}
    }
}

@monitor.on_event("startup")
async def monitor_startup(ctx: Context):
    """Monitor starts up and connects to deployed agents"""
    print("🌐" + "="*80 + "🌐")
    print("📊 COMPLETE RESPONSE MONITOR - AGENTVERSE EDITION")
    print("🔍 Monitoring Your Deployed Restaurant Recommendation Agents")
    print("🌐" + "="*80 + "🌐")
    print()
    
    ctx.logger.info("📊 Response Monitor starting...")
    ctx.logger.info(f"📍 Monitor Address: {monitor.address}")
    print(f"📍 Monitor Address: {monitor.address}")
    
    print("\n🤖 DEPLOYED AGENT STATUS:")
    print("-" * 40)
    
    for agent_name, address in DEPLOYED_AGENTS.items():
        if address:
            print(f"✅ {agent_name.upper()}: {address[:20]}... (Connected)")
            ctx.logger.info(f"✅ Connected to {agent_name}: {address[:20]}...")
        else:
            print(f"⏳ {agent_name.upper()}: Not deployed yet")
            ctx.logger.info(f"⏳ Waiting for {agent_name} deployment")
    
    print("\n🔄 MONITORING CAPABILITIES:")
    print("• Real-time intercommunication tracking")
    print("• Complete workflow visualization")
    print("• Response analysis and statistics")
    print("• Performance monitoring")
    
    print("\n📡 Starting continuous monitoring...")
    print("🎯 Send requests to Alice to see complete collaboration!")

@monitor.on_interval(period=45.0)  # Every 45 seconds
async def send_test_request(ctx: Context):
    """Send test requests to deployed Alice to trigger collaboration"""
    
    alice_address = DEPLOYED_AGENTS.get("alice")
    if not alice_address:
        ctx.logger.info("⏳ Waiting for Alice deployment...")
        return
    
    # Generate test scenarios
    test_scenarios = [
        {
            "request": "Find romantic Italian restaurant for anniversary dinner",
            "preferences": {"cuisine": "Italian", "occasion": "romantic", "price_range": "$$$"},
            "location": "downtown"
        },
        {
            "request": "Family-friendly sushi restaurant with kids options",
            "preferences": {"cuisine": "Japanese", "occasion": "family", "price_range": "$$"},
            "location": "suburbs"
        },
        {
            "request": "Business lunch venue in financial district",
            "preferences": {"cuisine": "American", "occasion": "business", "price_range": "$$$"},
            "location": "financial_district"
        },
        {
            "request": "Casual Mexican restaurant with outdoor seating",
            "preferences": {"cuisine": "Mexican", "occasion": "casual", "price_range": "$$"},
            "location": "riverside"
        }
    ]
    
    import random
    scenario = random.choice(test_scenarios)
    task_id = f"monitor_test_{datetime.datetime.now().strftime('%H%M%S')}"
    
    # Track this request
    response_tracker["active_tasks"][task_id] = {
        "start_time": datetime.datetime.now(),
        "scenario": scenario,
        "alice_response": None,
        "bob_response": None,
        "charlie_response": None,
        "status": "initiated"
    }
    
    request = UserRequest(
        task_id=task_id,
        user_request=scenario["request"],
        preferences=scenario["preferences"],
        location=scenario["location"],
        timestamp=datetime.datetime.now().isoformat()
    )
    
    print("\n🌐" + "="*60 + "🌐")
    print("🚀 INITIATING NEW COLLABORATION WORKFLOW")
    print("🌐" + "="*60 + "🌐")
    print(f"📋 Task ID: {task_id}")
    print(f"👤 User Request: '{scenario['request']}'")
    print(f"📍 Location: {scenario['location']}")
    print(f"🍽️ Cuisine: {scenario['preferences']['cuisine']}")
    print(f"🎭 Occasion: {scenario['preferences']['occasion']}")
    print(f"💰 Budget: {scenario['preferences']['price_range']}")
    print("📡 Sending to deployed Alice...")
    
    try:
        await ctx.send(alice_address, request)
        ctx.logger.info(f"✅ Test request sent to Alice: {task_id}")
        print("✅ Request sent to Alice - monitoring intercommunication...")
        
        # Update stats
        response_tracker["agent_stats"]["alice"]["messages_sent"] += 1
        response_tracker["agent_stats"]["alice"]["last_seen"] = datetime.datetime.now()
        
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send request to Alice: {str(e)}")
        print(f"❌ Failed to send request: {str(e)}")

@monitor.on_message(model=DataCollection)
async def track_alice_response(ctx: Context, sender: str, msg: DataCollection):
    """Track Alice's data collection response"""
    task_id = msg.task_id
    
    print("\n🔍" + "-"*50 + "🔍")
    print("🔍 ALICE RESPONSE RECEIVED")
    print("🔍" + "-"*50 + "🔍")
    print(f"📋 Task: {task_id}")
    print(f"📊 Confidence: {msg.confidence_score:.3f}")
    print(f"🍽️ Cuisine: {msg.user_preferences.get('cuisine', 'Any')}")
    print(f"💰 Budget: {msg.user_preferences.get('price_range', 'Any')}")
    print(f"📍 Location: {msg.location_data.get('area', 'Any')}")
    print(f"⏰ Timestamp: {msg.timestamp}")
    print("🔄 Alice → Bob: Data collection complete, sending to analyzer...")
    
    # Track Alice's response
    if task_id in response_tracker["active_tasks"]:
        response_tracker["active_tasks"][task_id]["alice_response"] = {
            "preferences": msg.user_preferences,
            "location": msg.location_data,
            "confidence": msg.confidence_score,
            "timestamp": msg.timestamp
        }
        response_tracker["active_tasks"][task_id]["status"] = "alice_completed"
    
    # Update Alice stats
    response_tracker["agent_stats"]["alice"]["last_seen"] = datetime.datetime.now()
    
    ctx.logger.info(f"📊 Alice response tracked: {task_id}")

@monitor.on_message(model=AnalysisResult)
async def track_bob_response(ctx: Context, sender: str, msg: AnalysisResult):
    """Track Bob's analysis response"""
    task_id = msg.task_id
    
    print("\n🧠" + "-"*50 + "🧠")
    print("🧠 BOB RESPONSE RECEIVED") 
    print("🧠" + "-"*50 + "🧠")
    print(f"📋 Task: {task_id}")
    print(f"📊 Analysis: {msg.analysis_summary}")
    print(f"🏆 Recommendations: {len(msg.recommendations)} options found")
    
    if msg.recommendations:
        top_rec = msg.recommendations[0]
        restaurant = top_rec['restaurant']
        print(f"🥇 Top Choice: {restaurant['name']} ({restaurant['cuisine']})")
        print(f"⭐ Rating: {restaurant['rating']}/5.0")
        print(f"💰 Price: {restaurant['price']}")
        print(f"📍 Location: {restaurant['location']}")
        print(f"📊 Match Score: {top_rec['analysis_scores']['overall_match']:.3f}")
    
    print(f"📈 Overall Confidence: {msg.confidence_scores.get('overall_confidence', 0):.3f}")
    print(f"⏰ Timestamp: {msg.timestamp}")
    print("🔄 Bob → Charlie: Analysis complete, sending for final decision...")
    
    # Track Bob's response
    if task_id in response_tracker["active_tasks"]:
        response_tracker["active_tasks"][task_id]["bob_response"] = {
            "analysis_summary": msg.analysis_summary,
            "recommendations": msg.recommendations,
            "confidence_scores": msg.confidence_scores,
            "processing_time": msg.supporting_data.get("processing_time_seconds", 0),
            "timestamp": msg.timestamp
        }
        response_tracker["active_tasks"][task_id]["status"] = "bob_completed"
    
    # Update Bob stats
    response_tracker["agent_stats"]["bob"]["analyses_completed"] += 1
    response_tracker["agent_stats"]["bob"]["last_seen"] = datetime.datetime.now()
    
    ctx.logger.info(f"📊 Bob response tracked: {task_id}")

@monitor.on_message(model=FinalDecision)
async def track_charlie_response(ctx: Context, sender: str, msg: FinalDecision):
    """Track Charlie's final decision response"""
    task_id = msg.task_id
    
    print("\n👑" + "-"*50 + "👑")
    print("👑 CHARLIE RESPONSE RECEIVED")
    print("👑" + "-"*50 + "👑")
    print(f"📋 Task: {task_id}")
    print(f"🏆 FINAL RECOMMENDATION: {msg.final_choice.get('name', 'Unknown')}")
    print(f"🍽️ Cuisine: {msg.final_choice.get('cuisine', 'N/A')}")
    print(f"⭐ Rating: {msg.final_choice.get('rating', 'N/A')}/5.0")
    print(f"💰 Price: {msg.final_choice.get('price', 'N/A')}")
    print(f"📍 Location: {msg.final_choice.get('location', 'N/A')}")
    print(f"📊 Decision Confidence: {msg.confidence_score:.3f}")
    print(f"💭 Reasoning: {msg.decision_reasoning}")
    print(f"👥 Participants: {', '.join(msg.all_participants)}")
    print(f"⏰ Timestamp: {msg.timestamp}")
    
    # Show enhanced metrics if available
    choice = msg.final_choice
    if isinstance(choice, dict):
        if 'cultural_appropriateness' in choice:
            print(f"🌍 Cultural Score: {choice['cultural_appropriateness']:.3f}")
        if 'sustainability_rating' in choice:
            print(f"🌱 Sustainability: {choice['sustainability_rating']:.3f}")
        if 'global_standards_compliance' in choice:
            print(f"✅ Compliance: {choice['global_standards_compliance']:.3f}")
    
    # Track Charlie's response and complete the workflow
    if task_id in response_tracker["active_tasks"]:
        task_data = response_tracker["active_tasks"][task_id]
        
        task_data["charlie_response"] = {
            "final_choice": msg.final_choice,
            "decision_reasoning": msg.decision_reasoning,
            "confidence_score": msg.confidence_score,
            "timestamp": msg.timestamp
        }
        task_data["status"] = "completed"
        task_data["end_time"] = datetime.datetime.now()
        
        # Calculate total processing time
        total_time = (task_data["end_time"] - task_data["start_time"]).total_seconds()
        task_data["total_processing_time"] = total_time
        
        print("\n🎉" + "="*60 + "🎉")
        print("🎉 COMPLETE COLLABORATION WORKFLOW FINISHED!")
        print("🎉" + "="*60 + "🎉")
        print(f"⏱️ Total Processing Time: {total_time:.1f} seconds")
        print("📊 WORKFLOW SUMMARY:")
        print(f"   🔍 Alice: Collected user preferences → Bob")
        print(f"   🧠 Bob: Analyzed {len(task_data['bob_response']['recommendations'])} recommendations → Charlie")
        print(f"   👑 Charlie: Made final decision → All agents")
        print("✅ 3-Agent intercommunication successful!")
        print()
        
        # Move to completed workflows
        response_tracker["completed_workflows"].append(task_data)
        del response_tracker["active_tasks"][task_id]
    
    # Update Charlie stats
    response_tracker["agent_stats"]["charlie"]["decisions_made"] += 1
    response_tracker["agent_stats"]["charlie"]["last_seen"] = datetime.datetime.now()
    
    ctx.logger.info(f"📊 Charlie response tracked and workflow completed: {task_id}")

@monitor.on_message(model=StatusUpdate)
async def track_status_updates(ctx: Context, sender: str, msg: StatusUpdate):
    """Track status updates from all agents"""
    sender_name = msg.sender.lower()
    
    if sender_name in response_tracker["agent_stats"]:
        response_tracker["agent_stats"][sender_name]["last_seen"] = datetime.datetime.now()
    
    # Log important status updates
    if "discovered" in msg.message.lower() or "assembled" in msg.message.lower():
        print(f"\n🔗 AGENT NETWORK UPDATE: {msg.message}")
        ctx.logger.info(f"🔗 Network update: {msg.message}")

@monitor.on_interval(period=120.0)  # Every 2 minutes
async def show_monitoring_statistics(ctx: Context):
    """Show comprehensive monitoring statistics"""
    stats = response_tracker["agent_stats"]
    
    print("\n📊" + "="*60 + "📊")
    print("📊 MONITORING STATISTICS")
    print("📊" + "="*60 + "📊")
    
    print(f"🔍 Alice Stats:")
    print(f"   • Messages sent: {stats['alice']['messages_sent']}")
    print(f"   • Last seen: {stats['alice']['last_seen']}")
    
    print(f"🧠 Bob Stats:")
    print(f"   • Analyses completed: {stats['bob']['analyses_completed']}")
    print(f"   • Last seen: {stats['bob']['last_seen']}")
    
    print(f"👑 Charlie Stats:")
    print(f"   • Decisions made: {stats['charlie']['decisions_made']}")
    print(f"   • Last seen: {stats['charlie']['last_seen']}")
    
    print(f"\n📈 Workflow Stats:")
    print(f"   • Active tasks: {len(response_tracker['active_tasks'])}")
    print(f"   • Completed workflows: {len(response_tracker['completed_workflows'])}")
    
    if response_tracker["completed_workflows"]:
        avg_time = sum(w["total_processing_time"] for w in response_tracker["completed_workflows"]) / len(response_tracker["completed_workflows"])
        print(f"   • Average processing time: {avg_time:.1f} seconds")
    
    print("📊" + "="*60 + "📊")

def update_agent_addresses():
    """Helper function to update agent addresses after deployment"""
    print("\n🔧 UPDATE AGENT ADDRESSES:")
    print("-" * 30)
    print("After deploying Bob and Charlie, update these addresses in the code:")
    print(f'DEPLOYED_AGENTS = {{')
    print(f'    "alice": "{DEPLOYED_AGENTS["alice"]}",')
    print(f'    "bob": "agent1qf...xyz789",      # Update with Bob\'s address')
    print(f'    "charlie": "agent1qf...abc456",  # Update with Charlie\'s address')
    print(f'}}')

if __name__ == "__main__":
    print("🌐 Starting Complete Response Monitor for Agentverse")
    print("📊 This monitor will show ALL agent responses and intercommunication")
    print()
    
    update_agent_addresses()
    print()
    
    print("🚀 Starting monitoring...")
    print("🎯 The monitor will send test requests and show complete workflows")
    print("👀 Watch for Alice → Bob → Charlie collaboration!")
    
    monitor.run()
