"""
FastAPI Backend for LinkedIn Post Generator

This module provides a RESTful API for generating LinkedIn posts using AI.
It includes endpoints for post generation, user feedback, and health monitoring.

Key Features:
- AI-powered post generation with multiple tones and audiences
- Real-time web search integration for current information
- Streaming API responses for better user experience
- User feedback collection and logging
- Performance metrics tracking
- Content moderation and safety checks
- Comprehensive error handling

Dependencies:
- FastAPI: Web framework for building APIs
- Pydantic: Data validation and settings management
- post_generator: Custom module for AI post generation logic

Author: LinkedIn Post Generator Team
Date: August 2025
Version: 2.0.0
"""

import json
import logging
import os
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from post_generator import create_linkedin_posts, create_linkedin_posts_stream, LLMProviderError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="LinkedIn Post Generator",
    description="Generate engaging LinkedIn posts using AI",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load configuration
def load_config():
    """
    Load configuration from environment variables or config.json file.
    Environment variables take precedence over config file.
    
    Returns:
        dict: Configuration dictionary containing API keys and settings.
              
    Priority:
        1. Environment variables (for production deployment)
        2. config.json file (for local development)
        3. Empty values (fallback)
        
    Example:
        >>> config = load_config()
        >>> api_key = config.get("groq_api_key", "")
    """
    
    # Try environment variable first (for production deployment)
    groq_api_key = os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY")  # Support both spellings
    
    # Debug logging for deployment troubleshooting
    logger.info(f"🔍 Environment variable GROQ_API_KEY: {'SET' if os.getenv('GROQ_API_KEY') else 'NOT SET'}")
    logger.info(f"🔍 Environment variable GROK_API_KEY: {'SET' if os.getenv('GROK_API_KEY') else 'NOT SET'}")
    logger.info(f"🔑 Final API key selected: {'SET' if groq_api_key else 'NOT SET'}")
    
    if groq_api_key:
        logger.info(f"🔑 Using API key from environment variable: {groq_api_key[:10]}...")
        return {"groq_api_key": groq_api_key}
    
    # Fallback to config.json file (for local development)
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
            if config.get("groq_api_key"):
                logger.info("✅ Using API key from config.json")
                return config
    except FileNotFoundError:
        logger.warning("⚠️ config.json not found")
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON in config.json")
    
    logger.warning("⚠️ No API key found - using empty key (will use mock responses)")
    return {"groq_api_key": ""}

# Global config
config = load_config()

# Pydantic models
class PostGenerationRequest(BaseModel):
    topic: str
    tone: Optional[str] = None
    audience: Optional[str] = None
    post_count: Optional[int] = 3
    use_web_search: Optional[bool] = False
    
    class Config:
        json_schema_extra = {
            "example": {
                "topic": "artificial intelligence",
                "tone": "professional",
                "audience": "software engineers",
                "post_count": 3,
                "use_web_search": False
            }
        }

class PostResponse(BaseModel):
    post_text: str
    hashtags: List[str]
    cta: str

class PerformanceMetrics(BaseModel):
    total_tokens: int
    total_latency: float
    call_count: int
    avg_latency_per_call: float

class GenerationResponse(BaseModel):
    posts: List[PostResponse]
    message: str
    metrics: PerformanceMetrics
    used_web_search: bool
    context_found: bool

class PostFeedbackRequest(BaseModel):
    """Model for post feedback request"""
    post_index: int
    rating: str  # "positive" or "negative"
    post_preview: str  # First 50 chars of the post for identification
    timestamp: Optional[str] = None

class FeedbackResponse(BaseModel):
    """Model for feedback response"""
    success: bool
    message: str

# API Endpoints
@app.get("/")
async def serve_index():
    """Serve the main index.html file"""
    return FileResponse("static/index.html")

@app.get("/infographic")
async def serve_infographic():
    """Serve the LinkedIn Post Generator infographic page"""
    import os
    file_path = "static/linkedin_post_generator_infographic.html"
    
    # Debug logging
    logger.info(f"🎨 Serving beautiful infographic from: {file_path}")
    logger.info(f"🔍 File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="text/html")
    else:
        logger.error(f"❌ Infographic file not found at: {file_path}")
        raise HTTPException(status_code=404, detail="Infographic file not found")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "LinkedIn Post Generator API is running",
        "api_configured": bool(config.get("groq_api_key"))
    }

@app.get("/favicon.ico")
async def favicon_ico():
    """Redirect favicon.ico to favicon.svg"""
    return FileResponse("static/favicon.svg")

@app.get("/favicon.svg")
async def favicon_svg():
    """Serve the favicon SVG"""
    return FileResponse("static/favicon.svg")

@app.post("/generate_posts", response_model=GenerationResponse)
async def generate_posts(request: PostGenerationRequest):
    """
    Generate LinkedIn posts based on the provided parameters
    """
    try:
        logger.info(f"📝 Generating posts for topic: {request.topic}")
        
        # Validate inputs
        if not request.topic or not request.topic.strip():
            raise HTTPException(status_code=400, detail="Topic is required and cannot be empty")
        
        if request.post_count and (request.post_count < 1 or request.post_count > 10):
            raise HTTPException(status_code=400, detail="Post count must be between 1 and 10")
        
        # Generate posts
        result = await create_linkedin_posts(
            topic=request.topic.strip(),
            tone=request.tone,
            audience=request.audience,
            post_count=request.post_count or 3,
            use_web_search=request.use_web_search or False,
            api_key=config.get("groq_api_key", "")
        )
        
        # Convert to response format
        post_responses = [
            PostResponse(
                post_text=post["post_text"],
                hashtags=post["hashtags"],
                cta=post["cta"]
            )
            for post in result["posts"]
        ]
        
        metrics_response = PerformanceMetrics(
            total_tokens=result["metrics"]["total_tokens"],
            total_latency=result["metrics"]["total_latency"],
            call_count=result["metrics"]["call_count"],
            avg_latency_per_call=result["metrics"]["avg_latency_per_call"]
        )
        
        logger.info(f"✅ Successfully generated {len(post_responses)} posts")
        
        return GenerationResponse(
            posts=post_responses,
            message=f"Successfully generated {len(post_responses)} LinkedIn posts",
            metrics=metrics_response,
            used_web_search=result["used_web_search"],
            context_found=result["context_found"]
        )
        
    except LLMProviderError as e:
        logger.error(f"❌ LLM Provider error: {str(e)}")
        raise HTTPException(
            status_code=502,
            detail=f"The AI service provider is currently unavailable: {str(e)}"
        )
    except Exception as e:
        logger.error(f"❌ Error generating posts: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate posts: {str(e)}"
        )

@app.post("/generate_posts_stream")
async def generate_posts_stream(request: PostGenerationRequest):
    """
    Generate LinkedIn posts with streaming response for real-time updates
    """
    async def stream_posts():
        try:
            logger.info(f"📝 Starting streaming generation for topic: {request.topic}")
            
            # Validate inputs
            if not request.topic or not request.topic.strip():
                yield f"data: {json.dumps({'error': 'Topic is required and cannot be empty'})}\n\n"
                return
            
            if request.post_count and (request.post_count < 1 or request.post_count > 10):
                yield f"data: {json.dumps({'error': 'Post count must be between 1 and 10'})}\n\n"
                return
            
            # Send initial status
            yield f"data: {json.dumps({'status': 'starting', 'message': 'Initializing AI generation...'})}\n\n"
            
            # Generate posts with streaming
            async for update in create_linkedin_posts_stream(
                topic=request.topic.strip(),
                tone=request.tone,
                audience=request.audience,
                post_count=request.post_count or 3,
                use_web_search=request.use_web_search or False,
                api_key=config.get("groq_api_key", "")
            ):
                yield f"data: {json.dumps(update)}\n\n"
                
        except Exception as e:
            logger.error(f"❌ Error in streaming generation: {str(e)}")
            yield f"data: {json.dumps({'error': str(e), 'status': 'error'})}\n\n"
    
    return StreamingResponse(
        stream_posts(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: PostFeedbackRequest):
    """
    Submit user feedback for a generated post
    
    Args:
        request: PostFeedbackRequest containing rating and post details
        
    Returns:
        FeedbackResponse confirming the feedback was logged
    """
    try:
        # Create feedback entry
        feedback_entry = {
            "timestamp": request.timestamp or datetime.now().isoformat(),
            "post_index": request.post_index,
            "rating": request.rating,
            "post_preview": request.post_preview,
            "session_id": "anonymous"  # Could be expanded for user sessions
        }
        
        # Log feedback to file (in production, this would go to a database)
        try:
            with open("feedback.json", "a") as f:
                f.write(json.dumps(feedback_entry) + "\n")
        except Exception as file_error:
            logger.warning(f"Could not write feedback to file: {file_error}")
        
        # Log feedback for monitoring
        logger.info(f"📝 User feedback received: {request.rating} for post {request.post_index}")
        
        return FeedbackResponse(
            success=True,
            message=f"Thank you for your {request.rating} feedback!"
        )
        
    except Exception as e:
        logger.error(f"❌ Error processing feedback: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process feedback"
        )

@app.post("/test")
async def test_endpoint(request: PostGenerationRequest):
    """Test endpoint to verify form submission is working"""
    logger.info(f"🧪 Test endpoint called with data: {request}")
    return {
        "message": "Test successful! Form submission is working.",
        "received_data": {
            "topic": request.topic,
            "tone": request.tone,
            "audience": request.audience,
            "post_count": request.post_count,
            "use_web_search": request.use_web_search
        }
    }

@app.get("/api/docs")
async def get_docs():
    """Redirect to API documentation"""
    return {"message": "Visit /docs for interactive API documentation"}

# Error handlers
@app.exception_handler(LLMProviderError)
async def llm_provider_error_handler(request, exc):
    return HTTPException(
        status_code=502,
        detail=f"The AI service provider is currently unavailable: {str(exc)}"
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "detail": "The requested endpoint does not exist"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": "An unexpected error occurred"}

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting LinkedIn Post Generator API...")
    logger.info("📖 API Documentation available at: http://localhost:8000/docs")
    logger.info("🌐 Web Interface available at: http://localhost:8000")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
