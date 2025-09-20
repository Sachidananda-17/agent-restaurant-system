"""
Quick Start Example for 3-Agent Collaborative System
This example shows the simplest way to get the system running
"""

import os
import sys
import time
import subprocess

def main():
    """Quick start guide for the 3-agent system"""
    
    print("🚀 QUICK START - 3-Agent Collaborative System")
    print("=" * 55)
    print()
    
    print("📋 This system demonstrates:")
    print("🔍 Alice: Collects user preferences and requirements")
    print("🧠 Bob: Analyzes data and generates recommendations")  
    print("👑 Charlie: Makes final decisions and coordinates team")
    print()
    
    print("🎯 Example Task: Restaurant Recommendation")
    print("The agents collaborate to recommend restaurants based on")
    print("user preferences, location, budget, and occasion.")
    print()
    
    print("🔄 Collaboration Flow:")
    print("1. Alice collects user data and preferences")
    print("2. Alice sends data to Bob for analysis")  
    print("3. Bob analyzes options and sends recommendations to Charlie")
    print("4. Charlie makes final decision and notifies the team")
    print("5. Process repeats with new requests")
    print()
    
    # Check if we're in the right directory
    if not os.path.exists("agents"):
        print("❌ Error: Please run this from the three_agent_system directory")
        print("📂 Expected structure:")
        print("   three_agent_system/")
        print("   ├── agents/")
        print("   ├── utils/")
        print("   ├── config/")
        print("   └── examples/")
        return
    
    print("🚀 LAUNCH OPTIONS:")
    print()
    
    print("📌 OPTION 1: Automatic Launch (Recommended)")
    print("   Run: python utils/team_launcher.py")
    print("   • Starts all agents in correct order")
    print("   • Opens separate windows for each agent")
    print("   • Provides status feedback")
    print()
    
    print("📌 OPTION 2: Manual Launch")
    print("   Terminal 1: python agents/charlie_coordinator.py")
    print("   Terminal 2: python agents/bob_analyzer.py")
    print("   Terminal 3: python agents/alice_data_collector.py")
    print("   • Start Charlie first (coordinator)")
    print("   • Start Bob second (analyzer)")
    print("   • Start Alice last (data collector)")
    print()
    
    print("📊 MONITORING OPTIONS:")
    print()
    
    print("📌 System Monitor:")
    print("   Run: python utils/system_monitor.py")
    print("   • Real-time health monitoring")
    print("   • Collaboration status tracking")
    print("   • Auto-refreshing dashboard")
    print()
    
    print("📌 Address Lookup:")
    print("   Run: python utils/get_team_addresses.py")
    print("   • Shows all agent addresses")
    print("   • Export to JSON for reference")
    print("   • Debug communication issues")
    print()
    
    # Interactive launch option
    print("=" * 55)
    
    try:
        choice = input("🎯 Launch automatically now? (y/n): ").lower().strip()
        
        if choice in ['y', 'yes']:
            print("\n🚀 Starting automatic launch...")
            print("⏳ This will open multiple windows...")
            time.sleep(2)
            
            # Check operating system and launch accordingly
            if os.name == 'nt':  # Windows
                launcher_path = os.path.join("utils", "team_launcher.py")
                subprocess.run(f"python {launcher_path}", shell=True)
            else:  # Unix-like
                launcher_path = os.path.join("utils", "team_launcher.py") 
                subprocess.run(f"python {launcher_path}", shell=True)
        else:
            print("\n📝 Manual launch instructions:")
            print("1. Open 3 separate terminal windows")
            print("2. Navigate to three_agent_system directory in each")
            print("3. Run the commands shown in OPTION 2 above")
            print("4. Watch the collaboration happen!")
        
    except KeyboardInterrupt:
        print("\n👋 Quick start cancelled")
    
    print("\n🎉 Enjoy exploring the 3-agent collaboration!")
    print("📚 Check the docs/ folder for detailed documentation")

if __name__ == "__main__":
    main()
