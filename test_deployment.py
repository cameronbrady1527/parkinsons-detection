#!/usr/bin/env python3
"""
Test script to verify the API works locally before deployment
"""

import requests
import time
import sys

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing API endpoints...")
    
    # Test ping endpoint
    try:
        response = requests.get(f"{base_url}/ping", timeout=10)
        print(f"✅ Ping endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Ping endpoint failed: {e}")
        return False
    
    # Test root endpoint
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        print(f"✅ Health endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Health endpoint failed: {e}")
        return False
    
    # Test info endpoint
    try:
        response = requests.get(f"{base_url}/info", timeout=10)
        print(f"✅ Info endpoint: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Info endpoint failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Starting API test...")
    
    # Wait a bit for the API to start
    print("Waiting 5 seconds for API to start...")
    time.sleep(5)
    
    success = test_api()
    
    if success:
        print("\n🎉 All tests passed! API is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the API logs.")
        sys.exit(1) 