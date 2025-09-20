"""
Agent Status Monitor
Shows the current status of both Alice and Bob agents
"""
import requests
import time

def check_agent_status(port, name):
    """Check if an agent is responding on its port"""
    try:
        response = requests.get(f"http://localhost:{port}/", timeout=2)
        return f"✅ {name} is running on port {port}"
    except requests.exceptions.RequestException:
        return f"❌ {name} is NOT responding on port {port}"

def main():
    print("🔍 AGENT STATUS MONITOR")
    print("=" * 40)
    
    while True:
        print(f"\n⏰ Status Check: {time.strftime('%H:%M:%S')}")
        print(check_agent_status(8000, "Alice"))
        print(check_agent_status(8001, "Bob"))
        print("📱 Press Ctrl+C to stop monitoring")
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped!")
