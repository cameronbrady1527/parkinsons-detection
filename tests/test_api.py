"""
Test script for the Parkinson's Disease Detection API
"""

import requests
import json
import pandas as pd
from src.utils.data_loading import load_parkinsons_data

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8000"
    
    print("Testing Parkinson's Disease Detection API...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test info endpoint
    print("\n2. Testing info endpoint...")
    try:
        response = requests.get(f"{base_url}/info")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test predict endpoint with sample data
    print("\n3. Testing predict endpoint...")
    try:
        # Load sample data
        df = load_parkinsons_data()
        if df is not None:
            # Take first 5 samples for testing
            test_data = df.head(5)
            
            # Save to temporary file
            test_file = "test_data.csv"
            test_data.to_csv(test_file, index=False)
            
            # Upload and predict
            with open(test_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{base_url}/predict", files=files)
            
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"Sample count: {result['sample_count']}")
                print(f"Features used: {len(result['features_used'])}")
                print(f"Predictions available for models: {list(result['predictions'].keys())}")
            else:
                print(f"Error: {response.text}")
            
            # Clean up
            import os
            os.remove(test_file)
        else:
            print("Could not load test data")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 