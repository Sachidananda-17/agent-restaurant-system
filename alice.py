# Alice Agent - The Message Sender
"""
This is Alice - an agent that can send messages to other agents.
Alice will periodically send greeting messages to Bob.
"""

from uagents import Agent, Context, Model
import asyncio

# Define the message structure that Alice will send
class GreetingMessage(Model):
    message: str
    sender_name: str
    timestamp: str

# Create Alice agent with unique configuration
alice = Agent(
    name="alice",
    seed="alice_secret_seed_phrase_2024",  # Unique seed for Alice's identity
    port=8000,  # Port where Alice will listen
    endpoint=["http://localhost:8000/submit"],  # Endpoint for receiving messages
)

# Bob's address (actual address from Bob agent)
BOB_ADDRESS = "agent1qfpl88grxndqgmp9lq6a6yx3wuvjwt8j3y3nltt9cetueahdqlcpzvy2ulj"

@alice.on_event("startup")
async def introduce_alice(ctx: Context):
    """
    This function runs when Alice starts up
    """
    ctx.logger.info(f"🌟 Hello! I'm Alice and my address is: {alice.address}")
    ctx.logger.info(f"🚀 Alice is ready to send messages!")

@alice.on_interval(period=10.0)  # Send a message every 10 seconds
async def send_greeting_to_bob(ctx: Context):
    """
    This function runs every 10 seconds and sends a greeting to Bob
    """
    import datetime
    
    # Create a greeting message
    greeting = GreetingMessage(
        message="Hello Bob! This is Alice sending you a friendly greeting! 👋",
        sender_name="Alice",
        timestamp=datetime.datetime.now().isoformat()
    )
    
    ctx.logger.info(f"📨 Alice is sending message to Bob...")
    
    try:
        # Send message to Bob
        await ctx.send(BOB_ADDRESS, greeting)
        ctx.logger.info(f"✅ Message sent successfully!")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send message: {str(e)}")

# This allows Alice to respond to messages (optional)
@alice.on_message(model=GreetingMessage)
async def handle_response_from_bob(ctx: Context, sender: str, msg: GreetingMessage):
    """
    This function handles responses from other agents (like Bob)
    """
    ctx.logger.info(f"📬 Alice received a message from {sender}:")
    ctx.logger.info(f"💬 Message: {msg.message}")
    ctx.logger.info(f"👤 From: {msg.sender_name}")
    ctx.logger.info(f"⏰ At: {msg.timestamp}")

if __name__ == "__main__":
    print("🎯 Starting Alice agent...")
    alice.run()
