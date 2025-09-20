"""
System Monitor Utility
Monitors the health and communication status of all three agents
"""

import requests
import time
import sys
import os
from datetime import datetime

# Add the parent directory to sys.path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.agent_config import AGENTS

class AgentMonitor:
    """Monitor individual agent health and status"""
    
    def __init__(self):
        self.agent_status = {}
        self.monitoring_start = datetime.now()
        
    def check_agent_health(self, agent_name: str, port: int) -> dict:
        """Check if an agent is responding"""
        try:
            response = requests.get(f"http://localhost:{port}/", timeout=2)
            return {
                "status": "✅ ONLINE",
                "response_time": "< 2s",
                "port": port,
                "health": "HEALTHY"
            }
        except requests.exceptions.ConnectionError:
            return {
                "status": "❌ OFFLINE", 
                "response_time": "N/A",
                "port": port,
                "health": "NOT_RESPONDING"
            }
        except requests.exceptions.Timeout:
            return {
                "status": "⚠️ SLOW",
                "response_time": "> 2s", 
                "port": port,
                "health": "SLOW_RESPONSE"
            }
        except Exception as e:
            return {
                "status": "❓ UNKNOWN",
                "response_time": "N/A",
                "port": port, 
                "health": f"ERROR: {str(e)[:30]}"
            }
    
    def monitor_all_agents(self):
        """Monitor all three agents"""
        agent_health = {}
        
        for agent_name, config in AGENTS.items():
            health = self.check_agent_health(agent_name, config["port"])
            agent_health[agent_name] = {
                **health,
                "role": config["role"],
                "expected_port": config["port"]
            }
        
        return agent_health
    
    def display_system_status(self, agent_health: dict):
        """Display formatted system status"""
        current_time = datetime.now().strftime("%H:%M:%S")
        monitoring_duration = datetime.now() - self.monitoring_start
        
        print("\033c", end="")  # Clear screen
        print("🔍 3-AGENT SYSTEM MONITOR")
        print("=" * 60)
        print(f"📅 Time: {current_time}")
        print(f"⏱️ Monitoring Duration: {str(monitoring_duration).split('.')[0]}")
        print(f"🔄 Auto-refresh: Every 5 seconds")
        print("=" * 60)
        print()
        
        # System Overview
        online_count = sum(1 for health in agent_health.values() if health["health"] == "HEALTHY")
        print(f"📊 SYSTEM OVERVIEW: {online_count}/3 agents online")
        
        if online_count == 3:
            print("🎉 Status: ALL SYSTEMS OPERATIONAL")
            print("🤝 Collaboration: ACTIVE")
        elif online_count >= 2:
            print("⚠️ Status: PARTIAL OPERATIONS")
            print("🤝 Collaboration: LIMITED")
        elif online_count == 1:
            print("❗ Status: MINIMAL OPERATIONS")
            print("🤝 Collaboration: UNAVAILABLE")
        else:
            print("❌ Status: SYSTEM DOWN")
            print("🤝 Collaboration: UNAVAILABLE")
        
        print()
        print("🤖 INDIVIDUAL AGENT STATUS:")
        print("-" * 60)
        
        # Individual Agent Status
        agent_icons = {"alice": "🔍", "bob": "🧠", "charlie": "👑"}
        
        for agent_name, health in agent_health.items():
            icon = agent_icons.get(agent_name, "🤖")
            print(f"{icon} {agent_name.upper():8} | {health['status']:12} | Port {health['port']:4} | {health['response_time']:8}")
            print(f"   Role: {health['role']}")
            print(f"   Health: {health['health']}")
            print()
        
        # Collaboration Status
        print("🔗 COLLABORATION STATUS:")
        print("-" * 60)
        
        if online_count == 3:
            print("🔍 Alice → 🧠 Bob → 👑 Charlie: ✅ FULL PIPELINE ACTIVE")
            print("📊 Data Collection: OPERATIONAL")
            print("🧮 Analysis Processing: OPERATIONAL") 
            print("🎯 Decision Making: OPERATIONAL")
        elif online_count == 2:
            offline_agents = [name for name, health in agent_health.items() if health["health"] != "HEALTHY"]
            print(f"⚠️ Missing: {', '.join(offline_agents).upper()}")
            print("🔗 Partial collaboration possible")
        else:
            print("❌ Insufficient agents for collaboration")
        
        print()
        print("💡 TIPS:")
        print("• Press Ctrl+C to stop monitoring")
        print("• Use team_launcher.py to start missing agents")
        print("• Check agent windows for detailed logs")
        print("=" * 60)

def main():
    """Main monitoring loop"""
    
    print("🔍 Starting 3-Agent System Monitor...")
    print("⏳ Initializing monitoring system...")
    time.sleep(2)
    
    monitor = AgentMonitor()
    
    try:
        while True:
            # Get current agent health status
            agent_health = monitor.monitor_all_agents()
            
            # Display the status  
            monitor.display_system_status(agent_health)
            
            # Wait before next check
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped by user")
        print("📊 Final System Status:")
        
        # Show final status
        final_health = monitor.monitor_all_agents()
        for agent_name, health in final_health.items():
            print(f"   {agent_name}: {health['status']}")
        
        print("\n🏁 Monitor shutdown complete")
    except Exception as e:
        print(f"\n❌ Monitoring error: {str(e)}")
        print("🔄 Try restarting the monitor")

if __name__ == "__main__":
    main()
