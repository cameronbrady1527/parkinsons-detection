#!/usr/bin/env python3
"""
Test script for Railway deployment
Replace YOUR_RAILWAY_URL with your actual Railway URL
"""

import requests
import sys
import json

# Replace this with your actual Railway URL
RAILWAY_URL = "YOUR_RAILWAY_URL"  # e.g., "https://your-app-name.railway.app"

def test_railway_api():
    """Test the deployed Railway API"""
    print(f"Testing Railway API at: {RAILWAY_URL}")
    print("=" * 50)
    
    endpoints = [
        ("/ping", "Health Check"),
        ("/", "Root Endpoint"),
        ("/health", "Health Status"),
        ("/info", "Model Information"),
        ("/test", "Basic Test")
    ]
    
    all_passed = True
    
    for endpoint, description in endpoints:
        try:
            url = f"{RAILWAY_URL}{endpoint}"
            print(f"\n🔍 Testing {description} ({endpoint})...")
            
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                print(f"✅ {description}: SUCCESS")
                data = response.json()
                print(f"   Response: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ {description}: FAILED (Status: {response.status_code})")
                print(f"   Response: {response.text}")
                all_passed = False
                
        except requests.exceptions.Timeout:
            print(f"❌ {description}: TIMEOUT")
            all_passed = False
        except requests.exceptions.ConnectionError:
            print(f"❌ {description}: CONNECTION ERROR")
            all_passed = False
        except Exception as e:
            print(f"❌ {description}: ERROR - {str(e)}")
            all_passed = False
    
    return all_passed

def test_prediction_endpoint():
    """Test the prediction endpoint with sample data"""
    print(f"\n🔍 Testing Prediction Endpoint...")
    
    try:
        # Create a minimal test CSV
        import pandas as pd
        import io
        
        # Sample data based on your training data structure
        sample_data = {
            'name': ['test_sample'],
            'MDVP:Fo(Hz)': [119.992],
            'MDVP:Fhi(Hz)': [157.302],
            'MDVP:Flo(Hz)': [74.997],
            'MDVP:Jitter(%)': [0.00784],
            'MDVP:Jitter(Abs)': [0.00007],
            'MDVP:RAP': [0.0037],
            'MDVP:PPQ': [0.00554],
            'Jitter:DDP': [0.01109],
            'MDVP:Shimmer': [0.04374],
            'MDVP:Shimmer(dB)': [0.426],
            'Shimmer:APQ3': [0.02182],
            'Shimmer:APQ5': [0.0313],
            'MDVP:APQ': [0.02971],
            'Shimmer:DDA': [0.06545],
            'NHR': [0.02211],
            'HNR': [21.033],
            'status': [1],
            'RPDE': [0.414783],
            'DFA': [0.815285],
            'spread1': [-4.813031],
            'spread2': [0.266482],
            'D2': [2.301442],
            'PPE': [0.284654]
        }
        
        df = pd.DataFrame(sample_data)
        
        # Convert to CSV string
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()
        
        # Test prediction endpoint
        url = f"{RAILWAY_URL}/predict"
        files = {'file': ('test_data.csv', csv_data, 'text/csv')}
        
        response = requests.post(url, files=files, timeout=60)
        
        if response.status_code == 200:
            print("✅ Prediction Endpoint: SUCCESS")
            data = response.json()
            print(f"   Predictions: {json.dumps(data, indent=2)}")
            return True
        else:
            print(f"❌ Prediction Endpoint: FAILED (Status: {response.status_code})")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Prediction Endpoint: ERROR - {str(e)}")
        return False

if __name__ == "__main__":
    if RAILWAY_URL == "YOUR_RAILWAY_URL":
        print("❌ Please update the RAILWAY_URL variable with your actual Railway URL")
        print("Example: RAILWAY_URL = 'https://your-app-name.railway.app'")
        sys.exit(1)
    
    print("🚀 Testing Railway Deployment")
    print("=" * 50)
    
    # Test basic endpoints
    basic_tests = test_railway_api()
    
    # Test prediction endpoint
    prediction_test = test_prediction_endpoint()
    
    print("\n" + "=" * 50)
    if basic_tests and prediction_test:
        print("🎉 ALL TESTS PASSED! Your Railway deployment is working perfectly!")
        print("\n📋 Next steps:")
        print("1. Share your API URL with others")
        print("2. Integrate with frontend applications")
        print("3. Monitor usage in Railway dashboard")
        print("4. Set up custom domain if needed")
    else:
        print("❌ Some tests failed. Check the Railway logs for issues.")
        print("\n🔧 Troubleshooting:")
        print("1. Check Railway deployment logs")
        print("2. Verify the URL is correct")
        print("3. Ensure all files were deployed")
        print("4. Check if the app is still starting up")
    
    sys.exit(0 if (basic_tests and prediction_test) else 1) 