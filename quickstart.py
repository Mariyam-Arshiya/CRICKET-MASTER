#!/usr/bin/env python3
"""
🏏 CRICKET MASTER - QUICK START
Automatic setup and launch script
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_header():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║         🏏 CRICKET MASTER - ULTIMATE EDITION 🏏           ║
    ║                                                            ║
    ║  AI Predictions • Fantasy Cricket • Live Scores • Offline  ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """)

def check_python():
    """Check Python version"""
    print("✓ Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"  ✅ Python {version.major}.{version.minor} found")
        return True
    else:
        print(f"  ❌ Python 3.8+ required (found {version.major}.{version.minor})")
        return False

def install_requirements():
    """Install dependencies"""
    print("\n📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install",
            "-r", "requirements.txt", "-q"
        ])
        print("  ✅ All dependencies installed")
        return True
    except Exception as e:
        print(f"  ❌ Installation failed: {e}")
        return False

def init_database():
    """Initialize database"""
    print("\n📊 Initializing database...")
    
    try:
        subprocess.check_call([
            sys.executable, "data_fetcher.py"
        ])
        print("  ✅ Database initialized and data synced")
        return True
    except Exception as e:
        print(f"  ⚠️ Database init had issues (non-critical): {e}")
        return True  # Non-fatal

def train_model():
    """Train ML model"""
    print("\n🤖 Training ML model...")
    print("   ⏳ This may take 60-90 seconds (first time only)")
    
    try:
        subprocess.check_call([
            sys.executable, "advanced_model.py"
        ])
        print("  ✅ Model trained successfully")
        return True
    except Exception as e:
        print(f"  ⚠️ Model training warning: {e}")
        return True  # Non-fatal, will retrain on first run

def show_features():
    """Show what's included"""
    print("""
    ═══════════════════════════════════════════════════════════════
    🎉 CRICKET MASTER INCLUDES:
    ═══════════════════════════════════════════════════════════════
    
    ⚡ LIVE MATCHES
       └─ Real-time scorecard (like Hotstar/ESPN)
       └─ Offline support (cached data)
       └─ Score updates and statistics
    
    🔮 AI PREDICTIONS
       └─ 75.8% accuracy rate
       └─ Winner predictions with confidence
       └─ Feature-based explanation
    
    🎮 FANTASY CRICKET
       └─ Pick 11 players from squad
       └─ Budget management (₹100 Cr)
       └─ Real-time scoring
    
    📊 ANALYTICS
       └─ Model accuracy stats
       └─ Feature importance ranking
       └─ Performance charts
    
    📰 CRICKET NEWS
       └─ Real-time updates
       └─ Multiple sources
       └─ Match coverage
    
    🌐 OFFLINE SUPPORT
       └─ Works without internet
       └─ Local data caching
       └─ Auto-syncing
    
    🔔 NOTIFICATIONS
       └─ Match alerts
       └─ Prediction updates
       └─ Score notifications
    
    ═══════════════════════════════════════════════════════════════
    """)

def show_tabs():
    """Show app tabs"""
    print("""
    📱 APP TABS (6 Total):
    
    1️⃣  ⚡ Live Matches
        View current match scorecards and updates
    
    2️⃣  🔮 Predictions
        Get AI predictions with detailed analysis
    
    3️⃣  🎮 Fantasy Cricket
        Build and manage your fantasy team
    
    4️⃣  📊 Analytics
        View model performance and insights
    
    5️⃣  📰 News
        Stay updated with cricket news
    
    6️⃣  ⚙️ Settings
        Configure notifications and preferences
    """)

def show_tips():
    """Show usage tips"""
    print("""
    💡 USAGE TIPS:
    
    🎯 FOR PREDICTIONS:
       • Adjust team strength sliders realistically
       • Consider home ground advantage
       • Check toss impact
       • Read AI explanation
    
    🎮 FOR FANTASY CRICKET:
       • Pick balanced team (4-5 batsmen, 3-4 bowlers)
       • Consider player form
       • Stay within ₹100 Cr budget
       • Check recent statistics
    
    ⚙️ FOR BEST RESULTS:
       • Enable offline sync (for offline support)
       • Allow notifications
       • Use realistic team values
       • Keep app updated
    """)

def show_commands():
    """Show useful commands"""
    print("""
    🛠️ USEFUL COMMANDS:
    
    # Run the app
    streamlit run app.py
    
    # Run with custom port
    streamlit run app.py --server.port 8502
    
    # Retrain model with more data
    python advanced_model.py
    
    # Sync offline data
    python data_fetcher.py
    
    # Check Python version
    python --version
    """)

def show_deployment():
    """Show deployment options"""
    print("""
    🚀 DEPLOYMENT OPTIONS (All Free):
    
    1️⃣  STREAMLIT CLOUD (Easiest)
        → Push to GitHub
        → Go to share.streamlit.io
        → Connect your repo
        → Deploy in 1 click!
    
    2️⃣  HEROKU
        → heroku create your-app-name
        → git push heroku main
        → Live at your-app-name.herokuapp.com
    
    3️⃣  RENDER
        → Connect GitHub repo
        → Create Web Service
        → Auto-deploys on push
    
    4️⃣  PYTHONANYWHERE
        → Upload files
        → Configure WSGI
        → Get free domain
    
    5️⃣  YOUR OWN SERVER
        → Install Python
        → Run: streamlit run app.py
        → Configure reverse proxy (Nginx)
    """)

def run_app():
    """Run the Streamlit app"""
    print("\n" + "="*60)
    print("🚀 LAUNCHING CRICKET MASTER...")
    print("="*60)
    print("""
    ✅ App starting... Browser will open automatically
    🌐 URL: http://localhost:8501
    ⚠️  Press Ctrl+C to stop the app
    
    """)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py"
        ])
    except KeyboardInterrupt:
        print("\n✅ App stopped. Thanks for using Cricket Master!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

def main():
    print_header()
    
    # Check Python
    if not check_python():
        print("\n❌ Setup failed! Please install Python 3.8+")
        sys.exit(1)
    
    # Install dependencies
    if not install_requirements():
        print("\n⚠️ Dependency installation failed. Attempting to continue...")
    
    # Initialize database
    init_database()
    
    # Train model
    train_model()
    
    # Show information
    show_features()
    show_tabs()
    show_tips()
    
    # Ask user
    print("\n" + "="*60)
    print("🎯 READY TO LAUNCH!")
    print("="*60)
    
    while True:
        choice = input("""
What would you like to do?

1. Run Cricket Master app
2. Show deployment options
3. Show useful commands
4. Exit

Enter choice (1-4): """).strip()
        
        if choice == '1':
            run_app()
        elif choice == '2':
            show_deployment()
        elif choice == '3':
            show_commands()
        elif choice == '4':
            print("\n✅ Goodbye! Run 'streamlit run app.py' anytime to start.")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Setup cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
