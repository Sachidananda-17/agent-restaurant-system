"""
Agentverse Deployment Guide
This shows how to modify your agents for Agentverse deployment
"""

# Example: Alice Agent Modified for Agentverse
from uagents import Agent, Context, Model
import datetime

class GreetingMessage(Model):
    message: str
    sender_name: str
    timestamp: str

# For Agentverse deployment, agents need specific configurations
alice_agentverse = Agent(
    name="alice_agentverse",
    seed="alice_agentverse_seed_2024",  # Use a different seed for Agentverse
    # Remove port and endpoint - Agentverse handles this automatically
)

@alice_agentverse.on_event("startup")
async def alice_startup(ctx: Context):
    ctx.logger.info(f"Alice is running on Agentverse! Address: {alice_agentverse.address}")
    ctx.logger.info("Ready to communicate with agents globally!")

# Modified to find Bob by name or use agent registry
@alice_agentverse.on_interval(period=15.0)  # Less frequent for production
async def send_message_agentverse(ctx: Context):
    # In Agentverse, you can discover other agents by their registered names
    # or use the agent directory service
    
    ctx.logger.info("Alice looking for Bob on Agentverse...")
    
    # Example message for any agent listening
    greeting = GreetingMessage(
        message="Hello from Alice on Agentverse! Any agents listening?",
        sender_name="Alice",
        timestamp=datetime.datetime.now().isoformat()
    )
    
    ctx.logger.info("Message prepared for Agentverse network")

@alice_agentverse.on_message(model=GreetingMessage)
async def handle_agentverse_message(ctx: Context, sender: str, msg: GreetingMessage):
    ctx.logger.info(f"Alice received message on Agentverse from {sender}")
    ctx.logger.info(f"Message: {msg.message}")

if __name__ == "__main__":
    alice_agentverse.run()

print("=== AGENTVERSE DEPLOYMENT STEPS ===")
print()
print("1. ACCOUNT SETUP:")
print("   - Go to https://agentverse.ai")
print("   - Create free account")
print("   - Verify email address")
print()
print("2. AGENT MODIFICATION:")
print("   - Remove port and endpoint parameters")
print("   - Use unique seed for production")
print("   - Add error handling for network issues")
print("   - Reduce message frequency")
print()
print("3. DEPLOYMENT OPTIONS:")
print()
print("   OPTION A - Web IDE:")
print("   - Login to Agentverse")
print("   - Click 'Create New Agent'")  
print("   - Copy your code into the web editor")
print("   - Click 'Deploy'")
print()
print("   OPTION B - Local Upload:")
print("   - Install Agentverse CLI")
print("   - Configure authentication")
print("   - Push agent to platform")
print()
print("4. AGENT DISCOVERY:")
print("   - Deployed agents appear in Agent Marketplace")
print("   - Other agents can find yours by name/category")
print("   - You can search for other agents to communicate with")
print()
print("5. MONITORING:")
print("   - View logs in Agentverse dashboard")
print("   - Monitor performance metrics")
print("   - Track message exchanges")
print()
print("=== BENEFITS OF AGENTVERSE ===")
print("✅ Global agent discovery")
print("✅ Automatic scaling")  
print("✅ Managed infrastructure")
print("✅ Agent marketplace visibility")
print("✅ Built-in monitoring and logs")
print("✅ No server maintenance required")
