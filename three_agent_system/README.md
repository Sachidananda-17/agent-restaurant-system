# 🎯 3-Agent Collaborative Decision Making System

A sophisticated multi-agent system built with **Fetch.ai uAgents** that demonstrates advanced AI collaboration through specialized roles, intelligent communication, and collective decision-making.

## 🌟 What This System Does

Three autonomous AI agents work together to solve complex problems by combining their unique expertise:

- 🔍 **Alice** collects and processes user requirements
- 🧠 **Bob** analyzes data and generates smart recommendations  
- 👑 **Charlie** makes final decisions through multi-criteria evaluation

**Real-world Application**: Collaborative restaurant recommendation engine that considers preferences, location, budget, ratings, and contextual factors.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ 
- pip package manager

### Installation

1. **Clone or navigate to the project directory**
```bash
cd three_agent_system
```

2. **Install uAgents framework**
```bash
pip install uagents
```

3. **Launch the system automatically** 
```bash
python examples/quick_start.py
```
*Choose 'y' when prompted for automatic launch*

### Alternative Manual Launch

```bash
# Terminal 1 - Start coordinator first
python agents/charlie_coordinator.py

# Terminal 2 - Start analyzer  
python agents/bob_analyzer.py

# Terminal 3 - Start data collector
python agents/alice_data_collector.py
```

## 📊 System Monitoring

### Real-time Dashboard
```bash
python utils/system_monitor.py
```
- Live health monitoring for all agents
- Communication status tracking
- Auto-refreshing system overview

### Address Lookup
```bash
python utils/get_team_addresses.py
```
- View all agent network addresses
- Export addresses for debugging
- Verify agent identity and connectivity

## 🏗️ Project Structure

```
three_agent_system/
│
├── 🤖 agents/                    # Core agent implementations
│   ├── alice_data_collector.py   # Data collection & user interface
│   ├── bob_analyzer.py           # Analysis engine & recommendations
│   └── charlie_coordinator.py    # Decision making & team coordination
│
├── ⚙️ config/                    # System configuration
│   ├── agent_config.py           # Agent settings & sample data
│   └── message_models.py         # Communication protocols
│
├── 🛠️ utils/                     # System utilities
│   ├── team_launcher.py          # Automated system startup
│   ├── system_monitor.py         # Health monitoring dashboard
│   └── get_team_addresses.py     # Agent address management
│
├── 📚 examples/                  # Usage examples
│   └── quick_start.py            # Getting started guide
│
└── 📖 docs/                      # Documentation
    └── SYSTEM_ARCHITECTURE.md    # Technical deep-dive
```

## 🔄 How It Works

### Collaboration Flow
```
🔍 Alice: "User wants romantic Italian restaurant downtown"
           ↓ [DataCollection Message]
🧠 Bob:   "Found 3 Italian restaurants, analyzing ratings, price, ambiance..."
           ↓ [AnalysisResult Message] 
👑 Charlie: "Based on analysis, selecting Villa Roma (4.8★, $$, romantic atmosphere)"
           ↓ [FinalDecision Broadcast]
📊 Result: Optimal recommendation with detailed reasoning
```

### Key Features

**🧠 Intelligent Specialization**
- Each agent has distinct expertise and decision-making capabilities
- Specialized algorithms for data processing, analysis, and coordination

**💬 Advanced Communication**
- Structured message protocols with type safety
- Automatic peer discovery and team formation
- Error handling and retry mechanisms

**📊 Multi-Criteria Analysis** 
- Rating-based scoring (40% weight)
- Preference matching (30% weight) 
- Location convenience (20% weight)
- Feature bonuses (10% weight)

**🎯 Decision Intelligence**
- Confidence thresholding for decision quality
- Risk assessment and mitigation
- Human-readable reasoning generation

## 📈 What You'll See

### Alice (Data Collector)
```
🔍 Alice Data Collector Agent Starting...
🎯 Role: Data Collection & Problem Identification
📋 Capabilities:
   • User preference analysis
   • Location data processing  
   • Search criteria optimization
🚀 Alice is ready for collaborative tasks!

🎯 Alice initiating new task: task_143022
📝 User Request: Find me a romantic restaurant for date night
📤 Data sent to Bob for analysis: task_143022
```

### Bob (Analyzer)  
```
🧠 Bob Analyzer Agent Starting...
🎯 Role: Solution Analysis & Processing
🔧 Analysis Capabilities:
   • Multi-criteria recommendation engine
   • Sentiment analysis processing
   • Price-performance optimization
🚀 Bob is ready for analytical tasks!

📊 Analysis request received for task: task_143022
🔄 Starting multi-stage analysis...
📊 Stage 1: Filtered to 3 restaurants
📊 Stage 2: Scoring and ranking completed
📤 Analysis results sent to Charlie: task_143022
```

### Charlie (Decision Coordinator)
```
👑 Charlie Coordinator Agent Starting...
🎯 Role: Final Decision Making & Team Coordination
🧠 Decision-Making Capabilities:
   • Multi-criteria decision analysis
   • Risk assessment & mitigation
   • Team coordination & communication
🚀 Charlie is ready to coordinate and decide!

🎯 Decision request received for task: task_143022
🔄 Starting decision evaluation process...
📊 Stage 1: Analysis quality score: 0.87
🎉 FINAL DECISION SUMMARY:
   🏆 Choice: Villa Roma
   🍽️ Cuisine: Italian
   ⭐ Rating: 4.8/5.0
   💰 Price: $$
   📍 Location: Historic District
   📊 Confidence: 0.92
```

## 🎓 Learning Outcomes

This system teaches advanced concepts in:

**Multi-Agent Systems**
- Agent specialization and role definition
- Distributed decision making
- Inter-agent communication protocols

**AI Collaboration**  
- Task decomposition and delegation
- Collective intelligence patterns
- Consensus building algorithms

**System Architecture**
- Modular design principles
- Event-driven programming
- Message-based communication

**Practical Applications**
- Recommendation engines
- Decision support systems
- Collaborative AI workflows

## 🔧 Customization Options

### Modify Decision Criteria
Edit `config/agent_config.py` to adjust:
- Confidence thresholds
- Scoring weights  
- Risk tolerance levels
- Sample data sets

### Add New Message Types
Extend `config/message_models.py` with:
- Custom data structures
- New communication patterns
- Additional metadata fields

### Create New Use Cases
The system is designed for easy adaptation to:
- Travel planning (hotels, flights, activities)
- Investment analysis (risk, returns, portfolios) 
- Healthcare recommendations (symptoms, treatments)
- Supply chain optimization (inventory, logistics)

## 🛠️ Advanced Usage

### Custom Restaurant Data
```python
# Add to config/agent_config.py
CUSTOM_RESTAURANTS = [
    {
        "name": "Your Restaurant",
        "cuisine": "Custom Cuisine",
        "rating": 4.9,
        "price": "$$$",
        "location": "Your Location",
        "features": ["your_feature_1", "your_feature_2"]
    }
]
```

### Deploy to Agentverse
1. Modify agents to remove port/endpoint parameters
2. Upload agent code to Agentverse platform
3. Enable global agent discovery and collaboration

### Scale to More Agents
1. Create new agent files in `agents/` directory
2. Define roles in `config/agent_config.py`
3. Implement message handlers for team integration

## 🤝 Contributing

This system serves as a foundation for advanced multi-agent applications. Contributions and extensions are welcome:

- Enhanced algorithms and decision logic
- New use cases and domain applications  
- Improved monitoring and debugging tools
- Additional communication patterns

## 📚 Further Reading

- **System Architecture**: `docs/SYSTEM_ARCHITECTURE.md` - Technical deep-dive
- **Fetch.ai Documentation**: Official uAgents framework guide
- **Multi-Agent Systems**: Academic resources on distributed AI

---

**🎉 Ready to explore AI collaboration?** 

Start with `python examples/quick_start.py` and watch three AI agents work together to solve complex problems!

**Built with ❤️ using Fetch.ai uAgents Framework**
