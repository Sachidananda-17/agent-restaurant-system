# Bob Agent - The Message Receiver & Responder
"""
This is Bob - an agent that receives messages from other agents and responds back.
Bob will listen for messages from Alice and send responses.
"""

from uagents import Agent, Context, Model
import random

# Define the same message structure (must match Alice's)
class GreetingMessage(Model):
    message: str
    sender_name: str
    timestamp: str

# Create Bob agent with different configuration from Alice
bob = Agent(
    name="bob",
    seed="bob_secret_seed_phrase_2024",  # Different seed from Alice
    port=8001,  # Different port from Alice (8001 vs 8000)
    endpoint=["http://localhost:8001/submit"],  # Different endpoint
)

# Predefined responses Bob can send back
BOB_RESPONSES = [
    "Hey Alice! Great to hear from you! 😊",
    "Hello Alice! Hope you're having a wonderful day! 🌟",
    "Hi Alice! Thanks for the message, you're awesome! 🎉",
    "Greetings Alice! Always a pleasure to chat with you! 👋",
    "Hey there Alice! Your messages always brighten my day! ☀️"
]

@bob.on_event("startup")
async def introduce_bob(ctx: Context):
    """
    This function runs when Bob starts up
    """
    ctx.logger.info(f"🤖 Hello! I'm Bob and my address is: {bob.address}")
    ctx.logger.info(f"👂 Bob is ready to listen for messages!")
    ctx.logger.info(f"📧 Send messages to this address: {bob.address}")

@bob.on_message(model=GreetingMessage)
async def handle_greeting_from_alice(ctx: Context, sender: str, msg: GreetingMessage):
    """
    This is the main function - it handles incoming messages from other agents
    """
    # Log the received message
    ctx.logger.info(f"🎉 Bob received a message!")
    ctx.logger.info(f"👤 From: {msg.sender_name} (Address: {sender})")
    ctx.logger.info(f"💬 Message: {msg.message}")
    ctx.logger.info(f"⏰ Timestamp: {msg.timestamp}")
    
    # Prepare a response
    import datetime
    response_text = random.choice(BOB_RESPONSES)  # Pick a random response
    
    response = GreetingMessage(
        message=response_text,
        sender_name="Bob",
        timestamp=datetime.datetime.now().isoformat()
    )
    
    ctx.logger.info(f"📤 Bob is sending response: {response_text}")
    
    try:
        # Send response back to the sender (Alice)
        await ctx.send(sender, response)
        ctx.logger.info(f"✅ Response sent successfully!")
    except Exception as e:
        ctx.logger.error(f"❌ Failed to send response: {str(e)}")

# Optional: Bob can also send periodic status updates
@bob.on_interval(period=30.0)  # Every 30 seconds
async def bob_status_update(ctx: Context):
    """
    Optional: Bob sends a status update every 30 seconds
    """
    ctx.logger.info(f"💓 Bob is alive and listening for messages...")

if __name__ == "__main__":
    print("🎯 Starting Bob agent...")
    print(f"📍 Bob's address will be: {bob.address}")
    bob.run()
