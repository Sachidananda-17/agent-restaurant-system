"""
Simple launcher for the 3-Agent Dashboard Web Application
Run this to start the web dashboard at http://localhost:5000
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    required_packages = ['flask', 'flask-socketio', 'uagents']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ All packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install packages: {e}")
        return False

def start_dashboard():
    """Start the dashboard application"""
    print("🌐 Starting 3-Agent Dashboard Web Application")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("❌ app.py not found. Please run this from the web_app directory.")
        return False
    
    # Check requirements
    missing = check_requirements()
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("📦 Installing missing packages...")
        if not install_requirements():
            return False
    
    print("🚀 Dashboard Features:")
    print("   • Real-time agent response monitoring")
    print("   • Interactive workflow visualization") 
    print("   • Live activity logging")
    print("   • Custom request sending")
    print("   • Performance statistics")
    print("   • Data export capabilities")
    print()
    
    print("🤖 Your Deployed Agents:")
    print("   🔍 Alice: agent1qv7cp9rmuln4ay27sxr7wfe5027er9xm3kx3fweckk55avl5xwhuv2rwqs3")
    print("   🧠 Bob:   agent1qfktux3y85zl4lajwh5shm7paputfddyrevdqq3stn7n65mgz9yxzf0sknu")
    print("   👑 Charlie: agent1q28h0anmn790wka6r7ws23jnt62546yza07q9cr7y9t988dzn7hy7se8khy")
    print()
    
    print("🌐 Starting web server...")
    print("📱 Dashboard will open at: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print()
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        try:
            webbrowser.open('http://localhost:5000')
        except Exception as e:
            print(f"⚠️ Could not open browser automatically: {e}")
            print("📱 Please manually open: http://localhost:5000")
    
    # Start browser opening in background
    import threading
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Import and run the Flask app
    try:
        from app import app, socketio
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Dashboard stopped by user")
        return True
    except Exception as e:
        print(f"❌ Dashboard error: {e}")
        return False

def show_help():
    """Show help information"""
    print("🤖 3-Agent Dashboard Launcher")
    print("=" * 40)
    print()
    print("🎯 Purpose:")
    print("   Launch a web dashboard to monitor your deployed")
    print("   Alice, Bob, and Charlie agents on Agentverse")
    print()
    print("🚀 Usage:")
    print("   python run_dashboard.py")
    print()
    print("📱 Features:")
    print("   • Real-time agent response monitoring")
    print("   • Visual workflow tracking")
    print("   • Interactive request sending")
    print("   • Performance statistics")
    print("   • Activity logging")
    print()
    print("🌐 Access:")
    print("   http://localhost:5000")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
    else:
        success = start_dashboard()
        if success:
            print("✅ Dashboard session completed successfully!")
        else:
            print("❌ Dashboard failed to start properly")
            sys.exit(1)
