#!/usr/bin/env python3
"""
Deployment script for Parkinson's Disease Detection Frontend

This script helps you test the frontend locally before deploying to production.
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        print("✅ FastAPI and Uvicorn are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install production dependencies:")
        print("pip install -r requirements-prod.txt")
        return False

def check_static_files():
    """Check if static files exist"""
    static_dir = Path("static")
    required_files = ["index.html", "styles.css", "script.js"]
    
    if not static_dir.exists():
        print("❌ Static directory not found")
        return False
    
    missing_files = []
    for file in required_files:
        if not (static_dir / file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing static files: {missing_files}")
        return False
    
    print("✅ All static files found")
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting Parkinson's Disease Detection Server...")
    print("=" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "api_prod.py"
        ], check=True)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start server: {e}")
        return False
    
    return True

def main():
    """Main deployment function"""
    print("🎯 Parkinson's Disease Detection - Frontend Deployment")
    print("=" * 55)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check static files
    if not check_static_files():
        return False
    
    print("\n📋 Deployment Checklist:")
    print("✅ Dependencies installed")
    print("✅ Static files present")
    print("✅ Ready to start server")
    
    # Ask user if they want to start the server
    response = input("\n🤔 Start the server now? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🌐 Server will start on http://localhost:8000")
        print("📱 Frontend will be available at the same URL")
        print("🔄 Press Ctrl+C to stop the server")
        
        # Give user time to read
        time.sleep(2)
        
        # Start server
        start_server()
    else:
        print("\n👋 Deployment cancelled. You can start manually with:")
        print("python api_prod.py")
    
    return True

if __name__ == "__main__":
    main() 