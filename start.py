#!/usr/bin/env python3
"""
Startup script for AI Hiring Evaluation System
Provides easy startup with environment validation
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if required environment variables are set"""
    required_vars = ['OPENAI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment")
        print("Example .env file:")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        return False
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import crewai
        import fastapi
        import uvicorn
        import openai
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    """Main startup function"""
    print("🤖 AI Hiring Evaluation System")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    print("🚀 Starting the application...")
    print("🌐 Web interface: http://localhost:8000")
    print("📚 API docs: http://localhost:8000/docs")
    print("=" * 40)
    
    # Import and run the main application
    try:
        from main import main as run_app
        run_app()
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

