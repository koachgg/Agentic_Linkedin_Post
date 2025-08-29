"""
LinkedIn Post Generator with Agentic AI Logic

This module implements an advanced AI-powered LinkedIn post generation system
using agentic workflows, real-time web search, and comprehensive content moderation.

Key Components:
1. LLMClient: Unified interface for multiple AI providers (Groq, Gemini)
2. Agentic Workflow: Multi-step content creation process
3. Web Search Integration: Real-time information gathering
4. Content Moderation: Safety and quality filtering
5. Performance Metrics: Comprehensive tracking and monitoring
6. Streaming Support: Real-time progress updates

Agentic Workflow Steps:
A. Research Phase: Optional web search for current information
B. Brainstorming: Generate multiple content angles and ideas
C. Drafting: Create initial posts for each angle in parallel
D. Refinement: Add hashtags, CTAs, and polish content
E. Moderation: Apply safety filters and quality checks

Features:
- Supports multiple AI providers with automatic fallback
- Real-time web search integration using DuckDuckGo
- Content moderation for profanity and spam detection
- Performance metrics tracking (tokens, latency, calls)
- Streaming API for real-time progress updates
- Comprehensive error handling and logging

Author: LinkedIn Post Generator Team
Date: August 2025
Version: 2.0.0
"""

import asyncio
import json
import logging
import time
import re
from typing import List, Dict, Optional, Tuple
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Custom exceptions
class LLMProviderError(Exception):
    """Custom exception for LLM provider issues"""
    pass

class ContentModerationError(Exception):
    """Custom exception for content moderation issues"""
    pass

class LLMClient:
    """
    Unified LLM client supporting multiple AI providers with performance tracking.
    
    This class provides a consistent interface for interacting with different
    Large Language Model providers (Groq, Gemini) while automatically tracking
    performance metrics and providing fallback behavior.
    
    Features:
    - Multi-provider support (Groq, Gemini)
    - Automatic performance metrics tracking
    - Mock mode for development/testing
    - Comprehensive error handling
    - Token and latency monitoring
    
    Attributes:
        provider (str): The AI provider being used ('groq' or 'gemini')
        api_key (str): API key for the provider
        use_mock (bool): Whether to use mock responses
        total_tokens (int): Total tokens used across all calls
        total_latency (float): Total time spent on API calls
        call_count (int): Number of API calls made
        
    Example:
        >>> client = LLMClient(provider="groq", api_key="your_key")
        >>> response = await client.generate_text("Write a LinkedIn post about AI")
        >>> metrics = client.get_metrics()
    """
    
    def __init__(self, provider: str = "groq", api_key: str = ""):
        self.provider = provider.lower()
        self.api_key = api_key
        self.total_tokens = 0
        self.total_latency = 0.0
        self.call_count = 0
        
        if self.provider not in ["gemini", "groq"]:
            raise ValueError("Provider must be 'gemini' or 'groq'")
        
        # Check if we have a valid API key
        if not api_key or api_key in ["your_api_key_here", "YOUR_API_KEY_HERE"]:
            logger.warning(f"No valid API key for {provider}, will use mock responses")
            self.use_mock = True
        else:
            self.use_mock = False
            logger.info(f"✅ Using real {provider.upper()} API")
        
        # Set up API endpoints
        if self.provider == "gemini":
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        elif self.provider == "groq":
            self.base_url = "https://api.groq.com/openai/v1/chat/completions"
    
    def get_metrics(self) -> Dict:
        """Get performance metrics"""
        return {
            "total_tokens": self.total_tokens,
            "total_latency": round(self.total_latency, 3),
            "call_count": self.call_count,
            "avg_latency_per_call": round(self.total_latency / max(self.call_count, 1), 3)
        }
    
    async def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate text using real API or mock response"""
        if self.use_mock:
            return self._mock_response(prompt)
        
        if self.provider == "gemini":
            return await self._call_gemini(prompt, max_tokens)
        elif self.provider == "groq":
            return await self._call_groq(prompt, max_tokens)
    
    async def _call_gemini(self, prompt: str, max_tokens: int) -> str:
        """Call Gemini API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {"Content-Type": "application/json"}
                
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "maxOutputTokens": max_tokens,
                        "temperature": 0.7
                    }
                }
                
                url = f"{self.base_url}?key={self.api_key}"
                
                async with session.post(url, json=payload, headers=headers) as response:
                    if response.status == 200:
                        data = await response.json()
                        text = data["candidates"][0]["content"]["parts"][0]["text"]
                        logger.info("✅ Gemini API call successful")
                        return text
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Gemini API error {response.status}: {error_text}")
                        return self._mock_response(prompt)
                        
        except Exception as e:
            logger.error(f"❌ Gemini API exception: {str(e)}")
            return self._mock_response(prompt)
    
    async def _call_groq(self, prompt: str, max_tokens: int) -> str:
        """Call Groq API with performance tracking"""
        start_time = time.time()
        
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": 0.7
                }
                
                async with session.post(self.base_url, json=payload, headers=headers) as response:
                    end_time = time.time()
                    latency = end_time - start_time
                    self.total_latency += latency
                    self.call_count += 1
                    
                    if response.status == 200:
                        data = await response.json()
                        text = data["choices"][0]["message"]["content"]
                        
                        # Track token usage if available
                        if "usage" in data:
                            tokens = data["usage"].get("total_tokens", 0)
                            self.total_tokens += tokens
                        
                        logger.info(f"✅ Groq API call successful ({latency:.2f}s)")
                        return text
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Groq API error {response.status}: {error_text}")
                        raise LLMProviderError(f"Groq API error {response.status}: {error_text}")
                        
        except aiohttp.ClientError as e:
            end_time = time.time()
            latency = end_time - start_time
            self.total_latency += latency
            self.call_count += 1
            logger.error(f"❌ Groq API connection error: {str(e)}")
            raise LLMProviderError(f"Connection error: {str(e)}")
        except Exception as e:
            end_time = time.time()
            latency = end_time - start_time
            self.total_latency += latency
            self.call_count += 1
            logger.error(f"❌ Groq API unexpected error: {str(e)}")
            raise LLMProviderError(f"Unexpected error: {str(e)}")
    
    def _mock_response(self, prompt: str) -> str:
        """Generate mock response as fallback"""
        logger.warning("🔄 Using mock LLM response")
        
        if "brainstorm" in prompt.lower() and "angles" in prompt.lower():
            return """1. Personal career journey and lessons learned
2. Industry trends and future predictions
3. Tips and best practices for professionals"""
        
        elif "linkedin post" in prompt.lower() and "write" in prompt.lower():
            return """🚀 Exciting times in the tech industry! 

As someone passionate about innovation, I've been reflecting on how rapidly our field evolves. Every day brings new opportunities to learn, grow, and make an impact.

Whether you're just starting your career or you're a seasoned professional, remember that continuous learning is key. Embrace challenges, seek mentorship, and don't be afraid to step outside your comfort zone.

What's one thing you've learned recently that changed your perspective? I'd love to hear your thoughts in the comments!

#TechInnovation #CareerGrowth #ContinuousLearning #ProfessionalDevelopment #Innovation"""
        
        elif "hashtags" in prompt.lower() and "cta" in prompt.lower():
            return """{
    "hashtags": ["#TechInnovation", "#CareerGrowth", "#ContinuousLearning", "#ProfessionalDevelopment", "#Innovation"],
    "cta": "What's one thing you've learned recently that changed your perspective? Share your thoughts in the comments!"
}"""
        
        else:
            return "Mock response - API call failed or not configured"


# Web search functionality
async def web_search(query: str, max_results: int = 3) -> str:
    """
    Perform web search using DuckDuckGo and return formatted context
    """
    try:
        logger.info(f"🔍 Performing web search for: {query}")
        
        # Import here to avoid issues if package is not available
        try:
            from duckduckgo_search import DDGS
        except ImportError:
            logger.warning("DuckDuckGo search not available, skipping web search")
            return ""
        
        # Use DuckDuckGo search
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        
        if not results:
            logger.warning("⚠️ No search results found")
            return ""
        
        # Format results into context
        context_parts = []
        for i, result in enumerate(results, 1):
            title = result.get('title', 'No title')
            snippet = result.get('body', 'No description')
            context_parts.append(f"{i}. {title}: {snippet}")
        
        context = "\n".join(context_parts)
        logger.info(f"✅ Found {len(results)} search results")
        return context
        
    except Exception as e:
        logger.error(f"❌ Web search failed: {str(e)}")
        return ""


# Content moderation
def moderate_content(text: str) -> Tuple[bool, str]:
    """
    Simple content moderation function
    Returns (is_clean, reason_if_not_clean)
    """
    # List of inappropriate words/phrases to filter
    banned_words = [
        # Add more comprehensive list as needed
        'spam', 'scam', 'hate', 'violence', 'discriminat', 'harass',
        'illegal', 'fraud', 'misleading', 'fake news', 'misinformation'
    ]
    
    # Convert to lowercase for checking
    text_lower = text.lower()
    
    # Check for banned words
    for word in banned_words:
        if word in text_lower:
            return False, f"Contains potentially inappropriate content: '{word}'"
    
    # Check for excessive capitalization (potential spam)
    if len(text) > 50:  # Only check if text is substantial
        caps_count = sum(1 for c in text if c.isupper())
        caps_ratio = caps_count / len(text)
        if caps_ratio > 0.7:  # More than 70% caps
            return False, "Excessive capitalization detected"
    
    # Check for excessive punctuation (potential spam)
    punct_pattern = r'[!]{3,}|[?]{3,}|[.]{3,}'
    if re.search(punct_pattern, text):
        return False, "Excessive punctuation detected"
    
    return True, ""


def apply_content_moderation(posts: List[Dict]) -> List[Dict]:
    """
    Apply content moderation to a list of posts
    """
    moderated_posts = []
    
    for i, post in enumerate(posts):
        is_clean, reason = moderate_content(post['post_text'])
        
        if not is_clean:
            logger.warning(f"⚠️ Post {i+1} moderated: {reason}")
            # Replace with moderated message
            moderated_post = post.copy()
            moderated_post['post_text'] = "[This post was moderated for containing potentially inappropriate content. Please try generating again with a different topic.]"
            moderated_post['hashtags'] = ["#ContentModerated"]
            moderated_post['cta'] = "Please try again with a different topic."
            moderated_posts.append(moderated_post)
        else:
            moderated_posts.append(post)
    
    return moderated_posts


async def create_linkedin_posts(
    topic: str,
    tone: Optional[str] = None,
    audience: Optional[str] = None,
    post_count: int = 3,
    use_web_search: bool = False,
    api_key: str = ""
) -> Dict:
    """
    Create LinkedIn posts using agentic AI logic with multi-step process
    
    Args:
        topic: Main topic for the posts
        tone: Optional tone (e.g., professional, casual, inspirational)
        audience: Optional target audience (e.g., software engineers, marketers)
        post_count: Number of posts to generate (default: 3)
        use_web_search: Whether to enhance with real-time web search
        api_key: Groq API key
    
    Returns:
        Dictionary containing posts, metrics, and metadata
    """
    
    # Initialize LLM client
    llm_client = LLMClient(provider="groq", api_key=api_key)
    
    logger.info(f"🎯 Starting LinkedIn post generation for topic: {topic}")
    
    context = ""
    
    # Step 0 - Research (optional): Web search for real-time data
    if use_web_search:
        logger.info("🔍 Step 0: Researching with web search...")
        context = await web_search(f"{topic} latest news trends 2025")
        if context:
            logger.info("✅ Web search context obtained")
        else:
            logger.warning("⚠️ Web search failed, proceeding without context")
    
    # Step A - Brainstorming: Generate different angles
    if context:
        brainstorm_prompt = f"Using the following recent context about {topic}, brainstorm {post_count} unique angles for a LinkedIn post. Context: {context}\n\nReturn only a numbered list of these angles."
    else:
        brainstorm_prompt = f"Based on the topic '{topic}', brainstorm {post_count} unique angles for a LinkedIn post. Return only a numbered list of these angles."
    
    logger.info("📝 Step A: Brainstorming angles...")
    angles_response = await llm_client.generate_text(brainstorm_prompt, max_tokens=500)
    
    # Parse angles from response
    angles = []
    for line in angles_response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
            # Remove numbering and clean up
            angle = line.split('.', 1)[-1].strip()
            if angle:
                angles.append(angle)
    
    # Fallback if parsing fails
    if not angles:
        angles = [
            f"Personal experience with {topic}",
            f"Industry trends related to {topic}",
            f"Best practices for {topic}"
        ]
        if post_count > 3:
            angles.extend([f"Future of {topic}", f"Common mistakes in {topic}"][:post_count-3])
    
    # Ensure we have the right number of angles
    angles = angles[:post_count]
    
    logger.info(f"✅ Generated {len(angles)} angles")
    
    # Step B - Drafting: Create posts for each angle in parallel
    logger.info("✍️ Step B: Drafting posts...")
    
    tone_text = f"The tone should be {tone}. " if tone else ""
    audience_text = f"The target audience is {audience}. " if audience else ""
    context_text = f"Use this context for factual accuracy: {context}\n\n" if context else ""
    
    draft_tasks = []
    for i, angle in enumerate(angles):
        draft_prompt = f"{context_text}Write a LinkedIn post from the angle: '{angle}'. {audience_text}{tone_text}The post should be engaging and around 150 words. Include emojis where appropriate."
        task = llm_client.generate_text(draft_prompt, max_tokens=800)
        draft_tasks.append(task)
    
    # Execute all drafting tasks in parallel
    drafted_posts = await asyncio.gather(*draft_tasks)
    
    logger.info(f"✅ Drafted {len(drafted_posts)} posts")
    
    # Step C - Refinement: Extract hashtags and CTAs in parallel
    logger.info("🏷️ Step C: Adding hashtags and CTAs...")
    
    refinement_tasks = []
    for post in drafted_posts:
        refinement_prompt = f"""For the following LinkedIn post, generate 5 relevant hashtags and a compelling call-to-action (CTA). 
Format the output as JSON with 'hashtags' and 'cta' keys. 

Post: {post}

Return only the JSON object."""
        
        task = llm_client.generate_text(refinement_prompt, max_tokens=300)
        refinement_tasks.append(task)
    
    # Execute all refinement tasks in parallel
    refinement_responses = await asyncio.gather(*refinement_tasks)
    
    # Combine everything into final posts
    final_posts = []
    for i, (post, refinement) in enumerate(zip(drafted_posts, refinement_responses)):
        try:
            # Try to parse JSON response
            if '{' in refinement and '}' in refinement:
                # Extract JSON part
                json_start = refinement.find('{')
                json_end = refinement.rfind('}') + 1
                json_str = refinement[json_start:json_end]
                refinement_data = json.loads(json_str)
                
                hashtags = refinement_data.get('hashtags', [])
                cta = refinement_data.get('cta', '')
            else:
                raise ValueError("No JSON found")
                
        except Exception as e:
            logger.warning(f"⚠️ Failed to parse refinement for post {i+1}: {e}")
            # Fallback hashtags and CTA
            hashtags = [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Professional", "#Growth", "#Insights"]
            cta = "What are your thoughts? Share in the comments!"
        
        # Ensure hashtags are properly formatted
        if isinstance(hashtags, list):
            hashtags = [tag if tag.startswith('#') else f"#{tag.replace(' ', '')}" for tag in hashtags]
        else:
            hashtags = [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Professional", "#Growth", "#Insights"]
        
        final_post = {
            "post_text": post.strip(),
            "hashtags": hashtags,
            "cta": cta.strip()
        }
        
        final_posts.append(final_post)
    
    # Step D - Content Moderation
    logger.info("🛡️ Step D: Applying content moderation...")
    moderated_posts = apply_content_moderation(final_posts)
    
    # Get performance metrics
    metrics = llm_client.get_metrics()
    
    logger.info(f"🎉 Successfully generated {len(moderated_posts)} LinkedIn posts")
    
    return {
        "posts": moderated_posts,
        "metrics": metrics,
        "used_web_search": use_web_search,
        "context_found": bool(context)
    }


# Streaming version of post generation
async def create_linkedin_posts_stream(
    topic: str,
    tone: Optional[str] = None,
    audience: Optional[str] = None,
    post_count: int = 3,
    use_web_search: bool = False,
    api_key: str = ""
):
    """
    Generate LinkedIn posts with streaming updates for real-time feedback
    
    Yields progress updates as JSON objects with different event types:
    - status: General progress updates
    - post: Individual completed posts
    - metrics: Performance metrics
    - complete: Final completion message
    """
    try:
        # Initialize client
        llm_client = LLMClient(provider="groq", api_key=api_key)
        
        yield {
            "status": "starting",
            "message": "Initializing post generation...",
            "progress": 5
        }
        
        context = ""
        
        # Step 0 - Research (optional): Web search for real-time data
        if use_web_search:
            yield {
                "status": "researching",
                "message": "Searching for latest information...",
                "progress": 15
            }
            
            context = await web_search(f"{topic} latest news trends 2025")
            if context:
                logger.info("✅ Web search context obtained")
            else:
                logger.warning("⚠️ Web search failed, proceeding without context")
        
        # Step A - Brainstorming: Generate different angles
        yield {
            "status": "brainstorming",
            "message": "Brainstorming content angles...",
            "progress": 25
        }
        
        if context:
            brainstorm_prompt = f"Using the following recent context about {topic}, brainstorm {post_count} unique angles for a LinkedIn post. Context: {context}\n\nReturn only a numbered list of these angles."
        else:
            brainstorm_prompt = f"Based on the topic '{topic}', brainstorm {post_count} unique angles for a LinkedIn post. Return only a numbered list of these angles."
        
        angles_response = await llm_client.generate_text(brainstorm_prompt, max_tokens=500)
        
        # Parse angles from response
        angles = []
        for line in angles_response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                angle = line.split('.', 1)[-1].strip()
                if angle:
                    angles.append(angle)
        
        # Fallback if parsing fails
        if not angles:
            angles = [
                f"Personal experience with {topic}",
                f"Industry trends related to {topic}",
                f"Best practices for {topic}"
            ]
            if post_count > 3:
                angles.extend([f"Future of {topic}", f"Common mistakes in {topic}"][:post_count-3])
        
        angles = angles[:post_count]
        
        # Step B - Drafting: Create posts for each angle
        yield {
            "status": "drafting",
            "message": f"Creating {len(angles)} post drafts...",
            "progress": 40
        }
        
        tone_text = f"The tone should be {tone}. " if tone else ""
        audience_text = f"The target audience is {audience}. " if audience else ""
        context_text = f"Use this context for factual accuracy: {context}\n\n" if context else ""
        
        draft_tasks = []
        for i, angle in enumerate(angles):
            draft_prompt = f"{context_text}Write a LinkedIn post from the angle: '{angle}'. {audience_text}{tone_text}The post should be engaging and around 150 words. Include emojis where appropriate."
            task = llm_client.generate_text(draft_prompt, max_tokens=800)
            draft_tasks.append(task)
        
        # Execute all drafting tasks in parallel
        drafted_posts = await asyncio.gather(*draft_tasks)
        
        # Step C - Refinement: Extract hashtags and CTAs
        yield {
            "status": "refining",
            "message": "Adding hashtags and call-to-actions...",
            "progress": 65
        }
        
        refinement_tasks = []
        for post in drafted_posts:
            refinement_prompt = f"""For the following LinkedIn post, generate 5 relevant hashtags and a compelling call-to-action (CTA). 
Format the output as JSON with 'hashtags' and 'cta' keys. 

Post: {post}

Return only the JSON object."""
            
            task = llm_client.generate_text(refinement_prompt, max_tokens=300)
            refinement_tasks.append(task)
        
        # Execute all refinement tasks in parallel
        refinement_responses = await asyncio.gather(*refinement_tasks)
        
        # Combine everything into final posts
        final_posts = []
        for i, (post, refinement) in enumerate(zip(drafted_posts, refinement_responses)):
            try:
                # Try to parse JSON response
                if '{' in refinement and '}' in refinement:
                    json_start = refinement.find('{')
                    json_end = refinement.rfind('}') + 1
                    json_str = refinement[json_start:json_end]
                    refinement_data = json.loads(json_str)
                    
                    hashtags = refinement_data.get('hashtags', [])
                    cta = refinement_data.get('cta', '')
                else:
                    raise ValueError("No JSON found")
                    
            except Exception as e:
                logger.warning(f"⚠️ Failed to parse refinement for post {i+1}: {e}")
                hashtags = [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Professional", "#Growth", "#Insights"]
                cta = "What are your thoughts? Share in the comments!"
            
            # Ensure hashtags are properly formatted
            if isinstance(hashtags, list):
                hashtags = [tag if tag.startswith('#') else f"#{tag.replace(' ', '')}" for tag in hashtags]
            else:
                hashtags = [f"#{topic.replace(' ', '')}", "#LinkedIn", "#Professional", "#Growth", "#Insights"]
            
            final_post = {
                "post_text": post.strip(),
                "hashtags": hashtags,
                "cta": cta.strip()
            }
            
            # Apply content moderation to individual post
            moderated_post = apply_content_moderation([final_post])[0]
            final_posts.append(moderated_post)
            
            # Yield each completed post
            yield {
                "type": "post",
                "data": moderated_post,
                "index": i,
                "progress": 65 + (25 * (i + 1) / len(drafted_posts))
            }
        
        # Final metrics
        metrics = llm_client.get_metrics()
        
        yield {
            "type": "metrics",
            "data": metrics,
            "progress": 95
        }
        
        # Completion
        yield {
            "type": "complete",
            "message": f"Successfully generated {len(final_posts)} LinkedIn posts",
            "posts": final_posts,
            "metrics": metrics,
            "used_web_search": use_web_search,
            "context_found": bool(context),
            "progress": 100
        }
        
    except Exception as e:
        logger.error(f"❌ Error in streaming generation: {str(e)}")
        yield {
            "type": "error",
            "message": str(e),
            "progress": 0
        }


# Test function for development
async def test_post_generation():
    """Test the post generation function"""
    result = await create_linkedin_posts(
        topic="artificial intelligence",
        tone="professional",
        audience="software engineers",
        post_count=2,
        use_web_search=False,  # Set to True to test web search
        api_key=""  # Will use mock responses
    )
    
    posts = result["posts"]
    metrics = result["metrics"]
    
    print(f"\n📊 Performance Metrics:")
    print(f"Total Tokens: {metrics['total_tokens']}")
    print(f"Total Latency: {metrics['total_latency']}s")
    print(f"API Calls: {metrics['call_count']}")
    print(f"Avg Latency per Call: {metrics['avg_latency_per_call']}s")
    print(f"Used Web Search: {result['used_web_search']}")
    print(f"Context Found: {result['context_found']}")
    
    for i, post in enumerate(posts, 1):
        print(f"\n=== POST {i} ===")
        print(f"Text: {post['post_text']}")
        print(f"Hashtags: {', '.join(post['hashtags'])}")
        print(f"CTA: {post['cta']}")


if __name__ == "__main__":
    asyncio.run(test_post_generation())
