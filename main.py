#!/usr/bin/env python3
"""
AI Hiring Evaluation System
Main entry point for the application
"""

import os
import sys
from pathlib import Path

# Add the app directory to Python path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

from dotenv import load_dotenv
import uvicorn

# Load environment variables
load_dotenv()

def main():
    """Main function to run the application"""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key in the .env file or environment variables")
        print("Example: export OPENAI_API_KEY='your-api-key-here'")
        sys.exit(1)
    
    print("🚀 Starting AI Hiring Evaluation System...")
    print("📊 Multi-Agent AI System for Automated Candidate Evaluation")
    print("🌐 Web interface will be available at: http://localhost:8000")
    print("📚 API documentation will be available at: http://localhost:8000/docs")
    print("\n" + "="*60)
    
    # Run the FastAPI application
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()

