"""
Test script for LinkedIn Post Generator API
"""

import asyncio
import aiohttp
import json

async def test_api():
    """Test the LinkedIn Post Generator API"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Testing LinkedIn Post Generator API\n")
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{base_url}/health") as response:
                if response.status == 200:
                    health_data = await response.json()
                    print(f"   ✅ Health check passed: {health_data['status']}")
                    print(f"   📊 API configured: {health_data['api_configured']}")
                else:
                    print(f"   ❌ Health check failed: {response.status}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    print()
    
    # Test post generation endpoint
    print("2. Testing post generation...")
    try:
        test_request = {
            "topic": "artificial intelligence",
            "tone": "professional",
            "audience": "software engineers",
            "post_count": 2
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{base_url}/generate_posts",
                json=test_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                
                if response.status == 200:
                    data = await response.json()
                    print(f"   ✅ Post generation successful!")
                    print(f"   📝 Generated {len(data['posts'])} posts")
                    
                    for i, post in enumerate(data['posts'], 1):
                        print(f"\n   === POST {i} ===")
                        print(f"   Text: {post['post_text'][:100]}...")
                        print(f"   Hashtags: {', '.join(post['hashtags'])}")
                        print(f"   CTA: {post['cta']}")
                else:
                    error_data = await response.json()
                    print(f"   ❌ Post generation failed: {response.status}")
                    print(f"   Error: {error_data.get('detail', 'Unknown error')}")
                    
    except Exception as e:
        print(f"   ❌ Post generation error: {e}")
    
    print("\n🎉 API testing completed!")

if __name__ == "__main__":
    asyncio.run(test_api())
