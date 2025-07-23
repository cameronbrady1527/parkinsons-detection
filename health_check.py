#!/usr/bin/env python3
"""
Health check script for the API
"""

import requests
import sys
import os

def health_check():
    """Perform health check on the API"""
    port = os.getenv('PORT', '8000')
    base_url = f"http://localhost:{port}"
    
    try:
        # Test ping endpoint
        response = requests.get(f"{base_url}/ping", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1) 