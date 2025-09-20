# Agent Communication Flow Explanation

## What Just Happened? 🚀

### 1. Agent Initialization
- **Alice** started on port 8000 with address `agent1q22h3n52hrp4sn0rytaumaatetvd4r02h9zptpq3g27ptnxvhhkyg8r0tnn`
- **Bob** started on port 8001 with address `agent1qfpl88grxndqgmp9lq6a6yx3wuvjwt8j3y3nltt9cetueahdqlcpzvy2ulj`

### 2. Communication Process
```
[Alice] ------ GreetingMessage ------> [Bob]
   |                                     |
   |    <----- ResponseMessage --------  |
   |                                     |
   v                                     v
Logs success                      Logs received message
```

### 3. Message Structure
Both agents use the same `GreetingMessage` model:
- `message`: The actual text content
- `sender_name`: Who sent it ("Alice" or "Bob")
- `timestamp`: When it was sent

### 4. Timing
- **Alice**: Sends message every 10 seconds
- **Bob**: Responds immediately when receiving
- **Bob**: Status update every 30 seconds

### 5. Network Details
- Agents communicate over HTTP
- Each has unique endpoints (localhost:8000 and localhost:8001)
- Messages are serialized using Pydantic models
- Addresses are cryptographically derived from seeds

## Key Concepts Demonstrated

### 🎯 **Agent Identity**
- Each agent has a unique address (like a crypto wallet)
- Generated from the `seed` parameter
- Used for routing messages in the network

### 📨 **Message Passing**
- Structured data using Pydantic models
- Asynchronous communication
- Error handling for failed sends

### ⚡ **Event-Driven Architecture**
- `@agent.on_event("startup")`: Runs when agent starts
- `@agent.on_interval(period=X)`: Runs every X seconds  
- `@agent.on_message(model=MessageType)`: Handles incoming messages

### 🔄 **Bidirectional Communication**
- Alice can send to Bob
- Bob can respond back to Alice
- Both can handle receiving messages

## This Is Just The Beginning!

Your agents are now:
✅ Created and running
✅ Communicating with each other
✅ Handling responses
✅ Running autonomously

Next steps: Deploy to Agentverse for global visibility!
