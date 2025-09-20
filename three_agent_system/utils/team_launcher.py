"""
Team Launcher Utility
Helps start all three agents in the correct order and provides status monitoring
"""

import subprocess
import time
import sys
import os

# Add the parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.agent_config import AGENTS

def launch_agent(agent_name: str, agent_file: str):
    """Launch an individual agent in a separate process"""
    agent_path = os.path.join("agents", agent_file)
    
    print(f"🚀 Starting {agent_name}...")
    print(f"📍 Port: {AGENTS[agent_name]['port']}")
    print(f"🎯 Role: {AGENTS[agent_name]['role']}")
    
    try:
        # Start agent in a new command window (Windows)
        if os.name == 'nt':  # Windows
            cmd = f'start "{agent_name.title()} Agent" python {agent_path}'
            subprocess.run(cmd, shell=True, check=True)
        else:  # Unix-like systems
            cmd = f'python {agent_path} &'
            subprocess.run(cmd, shell=True, check=True)
        
        print(f"✅ {agent_name.title()} started successfully!\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start {agent_name}: {str(e)}\n")
        return False

def main():
    """Launch all three agents in the optimal order"""
    
    print("🎯 3-AGENT COLLABORATIVE SYSTEM LAUNCHER")
    print("=" * 50)
    print()
    
    print("📋 System Overview:")
    print("🔍 Alice: Data Collector & Problem Identifier")
    print("🧠 Bob: Solution Analyzer & Processor")  
    print("👑 Charlie: Final Decision Maker & Coordinator")
    print()
    
    # Launch order: Charlie -> Bob -> Alice
    # This ensures coordinators are ready before data flows
    
    agents_to_launch = [
        ("charlie", "charlie_coordinator.py"),
        ("bob", "bob_analyzer.py"), 
        ("alice", "alice_data_collector.py")
    ]
    
    print("🚀 Starting agents in optimal order...")
    print("⏰ 5-second delay between each agent for proper initialization")
    print()
    
    successful_launches = 0
    
    for i, (agent_name, agent_file) in enumerate(agents_to_launch):
        if launch_agent(agent_name, agent_file):
            successful_launches += 1
        
        # Wait between launches (except for the last one)
        if i < len(agents_to_launch) - 1:
            print("⏳ Waiting 5 seconds for initialization...")
            time.sleep(5)
            print()
    
    print("=" * 50)
    if successful_launches == 3:
        print("🎉 ALL AGENTS LAUNCHED SUCCESSFULLY!")
        print()
        print("📊 System Status:")
        print("✅ Alice - Ready for data collection")
        print("✅ Bob - Ready for analysis")  
        print("✅ Charlie - Ready for decision making")
        print()
        print("🔄 The agents will now:")
        print("1. Discover each other automatically")
        print("2. Start collaborative restaurant recommendation tasks")
        print("3. Demonstrate full inter-agent communication")
        print()
        print("👀 Watch the agent windows to see the collaboration in action!")
        print("🛑 Press Ctrl+C in any agent window to stop that agent")
    else:
        print(f"⚠️ Only {successful_launches}/3 agents launched successfully")
        print("❗ Some agents may not be able to collaborate properly")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
