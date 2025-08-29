"""
LinkedIn Post Generator with Agentic AI Logic
Extracted and adapted from LinkedIn Sourcing Agent
"""

import asyncio
import json
import logging
from typing import List, Dict, Optional
import aiohttp

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LLMClient:
    """Unified LLM client supporting Gemini and Groq APIs"""
    
    def __init__(self, provider: str = "groq", api_key: str = ""):
        self.provider = provider.lower()
        self.api_key = api_key
        
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
        """Call Groq API"""
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
                    if response.status == 200:
                        data = await response.json()
                        text = data["choices"][0]["message"]["content"]
                        logger.info("✅ Groq API call successful")
                        return text
                    else:
                        error_text = await response.text()
                        logger.error(f"❌ Groq API error {response.status}: {error_text}")
                        return self._mock_response(prompt)
                        
        except Exception as e:
            logger.error(f"❌ Groq API exception: {str(e)}")
            return self._mock_response(prompt)
    
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


async def create_linkedin_posts(
    topic: str,
    tone: Optional[str] = None,
    audience: Optional[str] = None,
    post_count: int = 3,
    api_key: str = ""
) -> List[Dict]:
    """
    Create LinkedIn posts using agentic AI logic with multi-step process
    
    Args:
        topic: Main topic for the posts
        tone: Optional tone (e.g., professional, casual, inspirational)
        audience: Optional target audience (e.g., software engineers, marketers)
        post_count: Number of posts to generate (default: 3)
        api_key: Groq API key
    
    Returns:
        List of dictionaries with post_text, hashtags, and cta
    """
    
    # Initialize LLM client
    llm_client = LLMClient(provider="groq", api_key=api_key)
    
    logger.info(f"🎯 Starting LinkedIn post generation for topic: {topic}")
    
    # Step A - Brainstorming: Generate different angles
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
    
    draft_tasks = []
    for i, angle in enumerate(angles):
        draft_prompt = f"Write a LinkedIn post from the angle: '{angle}'. {audience_text}{tone_text}The post should be engaging and around 150 words. Include emojis where appropriate."
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
    
    logger.info(f"🎉 Successfully generated {len(final_posts)} LinkedIn posts")
    return final_posts


# Test function for development
async def test_post_generation():
    """Test the post generation function"""
    posts = await create_linkedin_posts(
        topic="artificial intelligence",
        tone="professional",
        audience="software engineers",
        post_count=2,
        api_key=""  # Will use mock responses
    )
    
    for i, post in enumerate(posts, 1):
        print(f"\n=== POST {i} ===")
        print(f"Text: {post['post_text']}")
        print(f"Hashtags: {', '.join(post['hashtags'])}")
        print(f"CTA: {post['cta']}")


if __name__ == "__main__":
    asyncio.run(test_post_generation())
