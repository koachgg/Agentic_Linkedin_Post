"""
Test script for enhanced LinkedIn Post Generator features
"""

import asyncio
import json
from post_generator import (
    create_linkedin_posts, 
    moderate_content, 
    apply_content_moderation,
    web_search,
    LLMClient
)

def test_content_moderation():
    """Test content moderation functionality"""
    print("🛡️ Testing Content Moderation...")
    
    # Test clean content
    clean_text = "This is a great post about artificial intelligence and machine learning."
    is_clean, reason = moderate_content(clean_text)
    print(f"✅ Clean text: {is_clean} (reason: {reason})")
    
    # Test inappropriate content
    spam_text = "This contains spam and misleading information!!!"
    is_clean, reason = moderate_content(spam_text)
    print(f"❌ Spam text: {is_clean} (reason: {reason})")
    
    # Test excessive caps
    caps_text = "THIS IS ALL CAPS AND LOOKS LIKE SPAM!"
    is_clean, reason = moderate_content(caps_text)
    print(f"❌ Caps text: {is_clean} (reason: {reason})")

async def test_web_search():
    """Test web search functionality"""
    print("\n🔍 Testing Web Search...")
    
    context = await web_search("artificial intelligence trends 2025", max_results=2)
    if context:
        print(f"✅ Web search successful, found context:")
        print(f"Context preview: {context[:200]}...")
    else:
        print("⚠️ Web search returned no results")

def test_llm_metrics():
    """Test LLM client metrics tracking"""
    print("\n📊 Testing LLM Metrics...")
    
    client = LLMClient(provider="groq", api_key="")  # Will use mock
    
    # Simulate some API calls (mock responses)
    client.total_tokens = 150
    client.total_latency = 2.5
    client.call_count = 3
    
    metrics = client.get_metrics()
    print(f"✅ Metrics: {json.dumps(metrics, indent=2)}")

async def test_enhanced_post_generation():
    """Test the full enhanced post generation"""
    print("\n🎯 Testing Enhanced Post Generation...")
    
    # Test without web search
    result = await create_linkedin_posts(
        topic="machine learning",
        tone="professional",
        audience="data scientists",
        post_count=2,
        use_web_search=False,
        api_key=""
    )
    
    print(f"✅ Generated {len(result['posts'])} posts")
    print(f"📊 Metrics: {result['metrics']}")
    print(f"🔍 Used web search: {result['used_web_search']}")
    print(f"📄 Context found: {result['context_found']}")
    
    # Show first post
    if result['posts']:
        first_post = result['posts'][0]
        print(f"\n📝 Sample Post:")
        print(f"Text: {first_post['post_text'][:100]}...")
        print(f"Hashtags: {', '.join(first_post['hashtags'])}")
        print(f"CTA: {first_post['cta']}")

def test_post_moderation():
    """Test post moderation with sample data"""
    print("\n🛡️ Testing Post Moderation...")
    
    # Sample posts with one that should be moderated
    sample_posts = [
        {
            "post_text": "Great insights on AI development!",
            "hashtags": ["#AI", "#Tech"],
            "cta": "What do you think?"
        },
        {
            "post_text": "This is spam content with misleading information!",
            "hashtags": ["#spam"],
            "cta": "Click here!"
        }
    ]
    
    moderated_posts = apply_content_moderation(sample_posts)
    
    for i, post in enumerate(moderated_posts):
        print(f"Post {i+1}: {'✅ Clean' if 'moderated' not in post['post_text'].lower() else '❌ Moderated'}")

async def main():
    """Run all tests"""
    print("🧪 Running Enhanced LinkedIn Post Generator Tests\n")
    
    # Test individual components
    test_content_moderation()
    await test_web_search()
    test_llm_metrics()
    test_post_moderation()
    
    # Test full integration
    await test_enhanced_post_generation()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
