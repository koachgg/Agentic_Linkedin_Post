"""
Basic tests for LinkedIn Post Generator
"""

import pytest
import asyncio
from post_generator import LLMClient, create_linkedin_posts


def test_llm_client_initialization():
    """Test LLM client can be initialized"""
    client = LLMClient(provider="groq", api_key="test_key")
    assert client.provider == "groq"
    assert client.api_key == "test_key"


def test_llm_client_mock_response():
    """Test LLM client mock response functionality"""
    client = LLMClient(provider="groq", api_key="")
    assert client.use_mock == True
    
    # Test different prompt types
    brainstorm_response = client._mock_response("brainstorm angles for topic")
    assert "1." in brainstorm_response
    
    post_response = client._mock_response("write a linkedin post")
    assert len(post_response) > 50
    
    hashtag_response = client._mock_response("generate hashtags and cta")
    assert "hashtags" in hashtag_response.lower()


@pytest.mark.asyncio
async def test_create_linkedin_posts():
    """Test the main post creation function"""
    posts = await create_linkedin_posts(
        topic="artificial intelligence",
        tone="professional",
        audience="software engineers",
        post_count=2,
        api_key=""  # Will use mock responses
    )
    
    assert len(posts) == 2
    
    for post in posts:
        assert "post_text" in post
        assert "hashtags" in post
        assert "cta" in post
        assert isinstance(post["hashtags"], list)
        assert len(post["post_text"]) > 10
        assert len(post["cta"]) > 5


@pytest.mark.asyncio
async def test_create_linkedin_posts_different_counts():
    """Test post creation with different post counts"""
    # Test with 1 post
    posts_1 = await create_linkedin_posts(
        topic="machine learning",
        post_count=1,
        api_key=""
    )
    assert len(posts_1) == 1
    
    # Test with 5 posts
    posts_5 = await create_linkedin_posts(
        topic="data science",
        post_count=5,
        api_key=""
    )
    assert len(posts_5) == 5


def test_invalid_provider():
    """Test that invalid provider raises error"""
    with pytest.raises(ValueError):
        LLMClient(provider="invalid", api_key="test")


if __name__ == "__main__":
    # Run tests manually
    print("🧪 Running basic tests...")
    
    # Test 1: LLM Client
    print("Testing LLM Client initialization...")
    test_llm_client_initialization()
    print("✅ LLM Client test passed")
    
    # Test 2: Mock responses
    print("Testing mock responses...")
    test_llm_client_mock_response()
    print("✅ Mock response test passed")
    
    # Test 3: Post creation
    print("Testing post creation...")
    asyncio.run(test_create_linkedin_posts())
    print("✅ Post creation test passed")
    
    print("🎉 All tests passed!")
