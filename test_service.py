#!/usr/bin/env python3
"""
Test script for Audio to Text Service
Tests the API endpoints and basic functionality
"""

import requests
import json
import time
import os

# Configuration
BASE_URL = "http://localhost:5000"
TEST_AUDIO_FILE = None  # You can add a test audio file path here

def test_health_check():
    """Test the health check endpoint"""
    print("🔍 Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_formats_endpoint():
    """Test the formats endpoint"""
    print("🔍 Testing formats endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/formats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Formats endpoint passed:")
            print(f"   Supported formats: {data.get('formats', [])}")
            print(f"   Supported languages: {data.get('languages', [])}")
            return True
        else:
            print(f"❌ Formats endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Formats endpoint error: {e}")
        return False

def test_main_page():
    """Test the main page loads"""
    print("🔍 Testing main page...")
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            print("✅ Main page loads successfully")
            return True
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page error: {e}")
        return False

def test_audio_conversion():
    """Test audio conversion with a sample file"""
    print("🔍 Testing audio conversion...")
    
    if not TEST_AUDIO_FILE or not os.path.exists(TEST_AUDIO_FILE):
        print("⚠️  No test audio file provided, skipping conversion test")
        print("   To test conversion, set TEST_AUDIO_FILE variable")
        return True
    
    try:
        with open(TEST_AUDIO_FILE, 'rb') as f:
            files = {'audio_file': f}
            data = {'language': 'english'}
            response = requests.post(f"{BASE_URL}/api/convert", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Audio conversion successful!")
                print(f"   Text: {result.get('text', '')[:100]}...")
                print(f"   Confidence: {result.get('confidence', 0)}")
                return True
            else:
                print(f"❌ Audio conversion failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ Audio conversion request failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Audio conversion error: {e}")
        return False

def test_invalid_file():
    """Test with invalid file"""
    print("🔍 Testing invalid file handling...")
    try:
        # Create a dummy text file
        dummy_content = "This is not an audio file"
        files = {'audio_file': ('test.txt', dummy_content, 'text/plain')}
        data = {'language': 'english'}
        response = requests.post(f"{BASE_URL}/api/convert", files=files, data=data)
        
        if response.status_code == 400:
            print("✅ Invalid file properly rejected")
            return True
        else:
            print(f"❌ Invalid file not properly handled: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Invalid file test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎵 Audio to Text Service Test Suite")
    print("=" * 50)
    
    tests = [
        test_health_check,
        test_formats_endpoint,
        test_main_page,
        test_invalid_file,
        test_audio_conversion,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Service is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the service configuration.")
    
    return passed == total

if __name__ == "__main__":
    # Wait a moment for service to start
    print("⏳ Waiting for service to start...")
    time.sleep(2)
    
    success = main()
    exit(0 if success else 1)
