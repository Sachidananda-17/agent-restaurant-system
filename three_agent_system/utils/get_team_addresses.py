"""
Team Address Utility
Displays the addresses of all three agents for debugging and reference
"""

import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_agent_addresses():
    """Get addresses for all three agents"""
    
    addresses = {}
    
    try:
        # Import each agent to get their addresses
        from agents.alice_data_collector import alice
        addresses["alice"] = {
            "address": alice.address,
            "name": alice.name,
            "port": 8000,
            "role": "Data Collector & Problem Identifier"
        }
    except Exception as e:
        addresses["alice"] = {"error": f"Failed to import Alice: {str(e)}"}
    
    try:
        from agents.bob_analyzer import bob
        addresses["bob"] = {
            "address": bob.address,
            "name": bob.name,
            "port": 8001,
            "role": "Solution Analyzer & Processor"
        }
    except Exception as e:
        addresses["bob"] = {"error": f"Failed to import Bob: {str(e)}"}
    
    try:
        from agents.charlie_coordinator import charlie
        addresses["charlie"] = {
            "address": charlie.address,
            "name": charlie.name,
            "port": 8002,
            "role": "Final Decision Maker & Coordinator"
        }
    except Exception as e:
        addresses["charlie"] = {"error": f"Failed to import Charlie: {str(e)}"}
    
    return addresses

def display_addresses():
    """Display agent addresses in a formatted way"""
    
    print("🎯 3-AGENT TEAM ADDRESS DIRECTORY")
    print("=" * 70)
    print()
    
    addresses = get_agent_addresses()
    
    agent_icons = {"alice": "🔍", "bob": "🧠", "charlie": "👑"}
    
    for agent_name, info in addresses.items():
        icon = agent_icons.get(agent_name, "🤖")
        
        print(f"{icon} {agent_name.upper()} AGENT:")
        
        if "error" in info:
            print(f"   ❌ Error: {info['error']}")
        else:
            print(f"   📍 Address: {info['address']}")
            print(f"   🏷️ Name: {info['name']}")
            print(f"   🚪 Port: {info['port']}")
            print(f"   🎯 Role: {info['role']}")
        
        print()
    
    print("=" * 70)
    print("💡 USAGE NOTES:")
    print("• These addresses are used for inter-agent communication")
    print("• Addresses are generated from agent seeds")
    print("• Copy these addresses for manual message testing")
    print("• Agents automatically discover each other during runtime")
    print("=" * 70)

def export_addresses_to_file():
    """Export addresses to a JSON file for reference"""
    import json
    from datetime import datetime
    
    addresses = get_agent_addresses()
    
    # Add timestamp and metadata
    export_data = {
        "generated_at": datetime.now().isoformat(),
        "system": "3-Agent Collaborative System",
        "version": "1.0",
        "agents": addresses
    }
    
    filename = "team_addresses.json"
    filepath = os.path.join("docs", filename)
    
    # Ensure docs directory exists
    os.makedirs("docs", exist_ok=True)
    
    try:
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📁 Addresses exported to: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Failed to export addresses: {str(e)}")
        return False

def main():
    """Main function"""
    
    print("🔍 Retrieving team agent addresses...")
    print("⏳ Loading agent configurations...")
    print()
    
    # Display addresses
    display_addresses()
    
    # Ask if user wants to export
    try:
        export_choice = input("\n💾 Export addresses to JSON file? (y/n): ").lower().strip()
        if export_choice in ['y', 'yes']:
            export_addresses_to_file()
    except KeyboardInterrupt:
        print("\n👋 Address lookup cancelled")

if __name__ == "__main__":
    main()
