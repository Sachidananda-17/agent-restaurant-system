"""
Client Agent Example - How to Use Your Deployed Restaurant Agents
This shows how to create a client that interacts with your deployed Alice, Bob, Charlie
"""

from uagents import Agent, Context, Model
import datetime

# === CLIENT MESSAGE MODELS ===
class UserRequest(Model):
    task_id: str
    user_request: str
    preferences: dict
    location: str
    timestamp: str

class FinalDecision(Model):
    task_id: str
    final_choice: dict
    decision_reasoning: str
    confidence_score: float
    all_participants: list
    timestamp: str
    sender: str = "Charlie"

# === CLIENT AGENT ===
client = Agent(
    name="restaurant_client",
    seed="client_seed_2024"
    # This client can run locally or also be deployed to Agentverse
)

# === YOUR DEPLOYED AGENTS' ADDRESSES ===
# Replace these with your actual deployed agent addresses from Agentverse dashboard
ALICE_GLOBAL_ADDRESS = "agent1qf...0z4m09"  # Your deployed Alice address
BOB_GLOBAL_ADDRESS = ""    # Will get Bob's address after deployment
CHARLIE_GLOBAL_ADDRESS = ""  # Will get Charlie's address after deployment

@client.on_event("startup")
async def client_startup(ctx: Context):
    """Client starts up and can send requests to deployed agents"""
    ctx.logger.info("🍽️ Restaurant Client starting...")
    ctx.logger.info(f"📍 Client Address: {client.address}")
    ctx.logger.info("🌐 Ready to request restaurant recommendations from deployed agents!")

@client.on_interval(period=30.0)  # Every 30 seconds
async def request_restaurant_recommendation(ctx: Context):
    """Send restaurant requests to your deployed Alice agent"""
    
    if not ALICE_GLOBAL_ADDRESS:
        ctx.logger.info("⏳ Waiting for Alice's global address...")
        return
    
    # Create user request
    task_id = f"client_request_{datetime.datetime.now().strftime('%H%M%S')}"
    
    user_scenarios = [
        {
            "request": "Find romantic Italian restaurant for anniversary dinner",
            "preferences": {"cuisine": "Italian", "occasion": "romantic", "price_range": "$$$"},
            "location": "downtown"
        },
        {
            "request": "Family-friendly pizza place with kids menu",
            "preferences": {"cuisine": "Italian", "occasion": "family", "price_range": "$$"},
            "location": "suburbs"
        },
        {
            "request": "Business lunch venue in financial district", 
            "preferences": {"cuisine": "American", "occasion": "business", "price_range": "$$$"},
            "location": "financial_district"
        }
    ]
    
    import random
    scenario = random.choice(user_scenarios)
    
    request = UserRequest(
        task_id=task_id,
        user_request=scenario["request"],
        preferences=scenario["preferences"], 
        location=scenario["location"],
        timestamp=datetime.datetime.now().isoformat()
    )
    
    ctx.logger.info("🌐 ===== SENDING REQUEST TO DEPLOYED AGENTS =====")
    ctx.logger.info(f"📋 Task: {task_id}")
    ctx.logger.info(f"🍽️ Request: {scenario['request']}")
    ctx.logger.info(f"📍 Location: {scenario['location']}")
    
    try:
        # Send to your deployed Alice on Agentverse
        await ctx.send(ALICE_GLOBAL_ADDRESS, request)
        ctx.logger.info("✅ Request sent to deployed Alice on Agentverse!")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send request: {str(e)}")

@client.on_message(model=FinalDecision)
async def receive_restaurant_decision(ctx: Context, sender: str, msg: FinalDecision):
    """Receive final restaurant decisions from deployed Charlie"""
    ctx.logger.info("🌐 ===== RECEIVED RECOMMENDATION FROM DEPLOYED AGENTS =====")
    ctx.logger.info(f"🎉 Task completed: {msg.task_id}")
    ctx.logger.info(f"🏆 Recommended restaurant: {msg.final_choice.get('name', 'Unknown')}")
    ctx.logger.info(f"🍽️ Cuisine: {msg.final_choice.get('cuisine', 'N/A')}")
    ctx.logger.info(f"⭐ Rating: {msg.final_choice.get('rating', 'N/A')}/5.0")
    ctx.logger.info(f"💰 Price: {msg.final_choice.get('price', 'N/A')}")
    ctx.logger.info(f"📍 Location: {msg.final_choice.get('location', 'N/A')}")
    ctx.logger.info(f"📊 Confidence: {msg.confidence_score:.3f}")
    ctx.logger.info(f"💭 Reasoning: {msg.decision_reasoning}")
    ctx.logger.info("✅ Global agent collaboration completed!")
    
    # Here you could:
    # - Store the recommendation in a database
    # - Send to a web application
    # - Trigger booking actions
    # - Notify mobile app users
    # - etc.

if __name__ == "__main__":
    print("🌐 Starting Restaurant Recommendation Client")
    print("📱 This client will interact with your deployed Agentverse agents")
    print(f"🔍 Sending requests to Alice: {ALICE_GLOBAL_ADDRESS[:20]}...")
    client.run()
