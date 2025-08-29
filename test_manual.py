"""
Quick test script to verify the LinkedIn Post Generator API
Run this to test the API endpoints manually
"""

import json
import requests

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_form_submission():
    """Test the test endpoint"""
    try:
        data = {
            "topic": "Test topic",
            "tone": "professional",
            "audience": "developers",
            "post_count": 2,
            "use_web_search": False
        }
        
        response = requests.post(f"{BASE_URL}/test", json=data)
        print(f"✅ Test endpoint: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Test endpoint failed: {e}")
        return False

def test_generate_posts():
    """Test the actual post generation"""
    try:
        data = {
            "topic": "Python programming",
            "tone": "educational",
            "audience": "beginner developers",
            "post_count": 1,
            "use_web_search": False
        }
        
        response = requests.post(f"{BASE_URL}/generate_posts", json=data)
        print(f"✅ Generate posts: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Generated {len(result.get('posts', []))} posts")
            if result.get('posts'):
                print(f"First post preview: {result['posts'][0]['post_text'][:100]}...")
        else:
            print(f"Error: {response.text}")
            
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Generate posts failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing LinkedIn Post Generator API")
    print("=" * 50)
    
    # Test health
    if not test_health():
        print("❌ Server is not running or health check failed")
        exit(1)
    
    print()
    
    # Test form submission
    if test_form_submission():
        print("✅ Form submission test passed")
    else:
        print("❌ Form submission test failed")
    
    print()
    
    # Test post generation
    if test_generate_posts():
        print("✅ Post generation test passed")
    else:
        print("❌ Post generation test failed")
    
    print()
    print("🎉 Testing complete!")
