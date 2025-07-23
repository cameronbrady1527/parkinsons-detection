#!/usr/bin/env python3
"""
Complete Application Test Script

This script tests all components of the Parkinson's Disease Detection application
to ensure everything works together properly.
"""

import requests
import json
import time
import sys
from pathlib import Path

def test_api_health():
    """Test API health endpoint"""
    print("🔍 Testing API Health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Health: {data['status']}")
            print(f"   Models Loaded: {data['models_loaded']}")
            print(f"   Scaler Loaded: {data['scaler_loaded']}")
            print(f"   Features Loaded: {data['features_loaded']}")
            return True
        else:
            print(f"❌ API Health failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API Health error: {e}")
        return False

def test_model_info():
    """Test model information endpoint"""
    print("\n🔍 Testing Model Information...")
    try:
        response = requests.get("http://localhost:8000/info", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'ready':
                print(f"✅ Models Ready: {len(data['models'])} models loaded")
                for model_name, model_data in data['models'].items():
                    accuracy = model_data['cv_accuracy'] * 100
                    print(f"   {model_name}: {accuracy:.1f}% accuracy")
                return True
            else:
                print(f"⚠️ Models not ready: {data.get('message', 'Unknown')}")
                return False
        else:
            print(f"❌ Model info failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Model info error: {e}")
        return False

def test_prediction():
    """Test prediction endpoint with sample data"""
    print("\n🔍 Testing Prediction Endpoint...")
    try:
        sample_file = Path("static/sample_data.csv")
        if not sample_file.exists():
            print("❌ Sample data file not found")
            return False
        
        with open(sample_file, 'rb') as f:
            files = {'file': f}
            response = requests.post("http://localhost:8000/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful: {data['sample_count']} samples processed")
            for model_name, predictions in data['predictions'].items():
                print(f"   {model_name}: {predictions}")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_frontend():
    """Test frontend page loading"""
    print("\n🔍 Testing Frontend...")
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            content = response.text
            if "Parkinson's Disease Detection" in content:
                print("✅ Frontend page loads correctly")
                return True
            else:
                print("❌ Frontend content not found")
                return False
        else:
            print(f"❌ Frontend failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend error: {e}")
        return False

def test_static_files():
    """Test static file serving"""
    print("\n🔍 Testing Static Files...")
    static_files = ['styles.css', 'script.js']
    
    for file_name in static_files:
        try:
            response = requests.get(f"http://localhost:8000/static/{file_name}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {file_name} served correctly")
            else:
                print(f"❌ {file_name} failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ {file_name} error: {e}")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🎯 Parkinson's Disease Detection - Complete Application Test")
    print("=" * 60)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    tests = [
        ("API Health", test_api_health),
        ("Model Information", test_model_info),
        ("Prediction Endpoint", test_prediction),
        ("Frontend Page", test_frontend),
        ("Static Files", test_static_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your application is working perfectly!")
        print("\n🌐 You can now:")
        print("   1. Open http://localhost:8000 in your browser")
        print("   2. Upload the sample_data.csv file")
        print("   3. See beautiful prediction results!")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 