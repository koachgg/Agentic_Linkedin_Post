#!/usr/bin/env python3
"""
Docker application launcher for Hugging Face Spaces deployment.
This file serves as the entry point when running the app in Docker.
"""

import os
import sys
import uvicorn
from main import app

def main():
    """Launch the FastAPI application for Docker deployment."""
    # Set default values for Hugging Face Spaces
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 7860))  # Hugging Face Spaces uses port 7860
    
    print(f"🚀 Starting LinkedIn Post Generator on {host}:{port}")
    print(f"📊 Environment: {'Production' if os.environ.get('GROQ_API_KEY') else 'Development'}")
    
    # Check for required environment variables
    if not os.environ.get("GROQ_API_KEY"):
        print("⚠️  WARNING: GROQ_API_KEY environment variable not set!")
        print("   The application will use demo mode with limited functionality.")
        print("   Set GROQ_API_KEY in your Hugging Face Space secrets for full functionality.")
    
    try:
        # Run the FastAPI application
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            reload=False  # Disable reload in production
        )
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
