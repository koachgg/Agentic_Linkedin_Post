"""
FastAPI Backend for LinkedIn Post Generator
"""

import json
import logging
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from post_generator import create_linkedin_posts, LLMProviderError

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
    """Load configuration from config.json"""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("⚠️ config.json not found, using empty API key")
        return {"groq_api_key": ""}
    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON in config.json")
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

# API Endpoints
@app.get("/")
async def serve_index():
    """Serve the main index.html file"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "LinkedIn Post Generator API is running",
        "api_configured": bool(config.get("groq_api_key"))
    }

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
