---
title: LinkedIn Post Generator
emoji: 🚀
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: apache-2.0
custom_headers:
  cross-origin-embedder-policy: unsafe-none
  cross-origin-opener-policy: unsafe-none
  cross-origin-resource-policy: cross-origin
---

# 🚀 LinkedIn Post Generator - Enhanced Edition

A fully functional web application that generates engaging LinkedIn posts using advanced agentic AI. Built with FastAPI backend and modern HTML/CSS/JavaScript frontend, featuring a beautiful Nugget.com-inspired dark theme, real-time streaming, and comprehensive user feedback.

## 🎨 **New UI/UX Features**

### 🌙 **Nugget.com-Inspired Dark Theme**
- **Dark Navy Background** (#0A0E1A) for a professional, modern look
- **Vibrant Purple Accents** (#8B5CF6) for buttons and interactive elements
- **Inter Font Family** for clean, readable typography
- **Single-Column Layout** for focused, distraction-free experience
- **Minimalist Design** with generous whitespace and clean lines
- **White Post Cards** with subtle shadows for excellent contrast

### ⚡ **Real-time Streaming API**
- **Live Progress Updates** during post generation
- **Progressive Post Rendering** - see posts as they're created
- **Dynamic Progress Bar** with status messages
- **Streaming Performance Metrics** for real-time insights

### 👥 **User Feedback System**
- **Thumbs Up/Down Buttons** on each generated post
- **Instant Visual Confirmation** when feedback is submitted
- **Backend Logging** of all user ratings for analytics
- **Elegant Feedback UI** with smooth animations

## 🚀 Enhanced Features

### 🔍 **Real-time Web Search Integration**
- Optional web search to enhance posts with current, factual information
- Uses DuckDuckGo search for privacy-friendly data retrieval
- Seamlessly integrates search context into the agentic workflow

### 📊 **Performance Metrics Dashboard**
- Real-time tracking of API latency and token usage
- Visual metrics display showing generation time, API calls, and efficiency
- Performance optimization insights for users

### 🛡️ **Content Moderation System**
- Automatic filtering of inappropriate content
- Smart detection of spam patterns and excessive formatting
- User-friendly moderation messages with retry suggestions

### ⚡ **Enhanced Error Handling**
- Specific exception handling for different error types
- Graceful degradation when services are unavailable
- Detailed error messages with recovery instructions

## Features

- **Advanced Agentic AI Logic**: Multi-step process for generating high-quality posts
  - Step 0: Real-time web research (optional)
  - Step A: Brainstorming unique angles for your topic
  - Step B: Drafting engaging posts with customizable tone and audience
  - Step C: Adding relevant hashtags and compelling call-to-actions
  - Step D: Content moderation and safety checks

- **Professional Web Interface**: Clean, responsive design with real-time metrics
- **Customizable Parameters**: 
  - Topic (required)
  - Tone (professional, casual, inspirational, etc.)
  - Target audience
  - Number of posts (1-10)
  - Web search enhancement toggle

- **Advanced Features**:
  - Copy-to-clipboard functionality
  - User feedback collection
  - Streaming API responses
  - Performance metrics display
  - Content moderation indicators
  - Real-time validation and error handling
  - API documentation with Swagger UI

## Project Structure

```
linkedin-post-generator/
├── static/
│   ├── index.html          # Main web interface
│   ├── style.css           # Professional styling
│   └── script.js           # Frontend logic
├── main.py                 # FastAPI backend
├── post_generator.py       # AI logic and LLM client
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
├── start_server.bat        # Windows startup script
└── README.md              # This file
```

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/linkedin-post-generator.git
cd linkedin-post-generator
```

### 2. Set Up Python Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Key
```bash
# Copy the example config
cp config.example.json config.json
# Edit config.json and add your Groq API key
```

### 5. Run the Application
```bash
python main.py
```

Visit http://localhost:8000 to use the application!

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Edit `config.json` and add your Groq API key:

```json
{
    "groq_api_key": "your_actual_groq_api_key_here"
}
```

**Note**: The application will work without an API key using mock responses for demonstration purposes.

### 3. Start the Server

#### Option A: Using the batch file (Windows)
```bash
start_server.bat
```

#### Option B: Using Python directly
```bash
python main.py
```

#### Option C: Using uvicorn
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## API Endpoints

### POST /generate_posts
Generate LinkedIn posts based on provided parameters.

**Request Body:**
```json
{
    "topic": "artificial intelligence",
    "tone": "professional",
    "audience": "software engineers",
    "post_count": 3
}
```

**Response:**
```json
{
    "posts": [
        {
            "post_text": "🚀 Exciting developments in AI...",
            "hashtags": ["#AI", "#TechInnovation", "#SoftwareEngineering"],
            "cta": "What's your experience with AI? Share in the comments!"
        }
    ],
    "message": "Successfully generated 3 LinkedIn posts"
}
```

### GET /health
Check API health and configuration status.

## How It Works

### Agentic AI Process

1. **Brainstorming Phase**: The AI generates multiple unique angles for your topic
2. **Drafting Phase**: For each angle, creates a full post considering tone and audience
3. **Refinement Phase**: Adds relevant hashtags and compelling call-to-actions

### Frontend Features

- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Validation**: Immediate feedback on form inputs
- **Loading States**: Visual feedback during post generation
- **Error Handling**: Clear error messages and recovery suggestions
- **Copy Functionality**: One-click copying of complete posts

## Customization

### Adding New Tones
Edit the tone dropdown in `static/index.html`:
```html
<option value="new_tone">New Tone</option>
```

### Modifying Post Count Limits
Update the validation in both `static/script.js` and `main.py`:
```python
if request.post_count and (request.post_count < 1 or request.post_count > 20):
```

### Styling Changes
Modify `static/style.css` to customize the appearance:
- Colors: Update CSS variables
- Layout: Modify grid and flexbox properties
- Animations: Adjust keyframes and transitions

## Development

### Adding New Features

1. **Backend**: Add new endpoints in `main.py`
2. **AI Logic**: Extend `post_generator.py` with new functions
3. **Frontend**: Update HTML/CSS/JS in the `static/` directory

### Testing

Run the post generator directly:
```bash
python post_generator.py
```

### Debugging

Enable debug mode by setting `log_level="debug"` in `main.py`:
```python
uvicorn.run("main:app", log_level="debug")
```

## Deployment

### Local Development
The application is ready to run locally using the provided scripts.

### Production Deployment
For production deployment:

1. Use a production WSGI server like Gunicorn
2. Set up reverse proxy with Nginx
3. Configure environment variables for API keys
4. Enable HTTPS
5. Set up monitoring and logging

Example production command:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **API Key Issues**: Check config.json format and key validity
3. **Port Conflicts**: Change port in main.py if 8000 is occupied
4. **CORS Issues**: Add allowed origins in FastAPI CORS middleware

### Getting Help

1. Check the console logs for error messages
2. Visit http://localhost:8000/health to verify API status
3. Test the API directly at http://localhost:8000/docs
4. Ensure Python environment is properly configured

## 🆕 Enhanced API Documentation

### Enhanced Features in API

#### Web Search Integration
- Add `"use_web_search": true` to your request to enhance posts with real-time data
- The system will automatically search for current information about your topic
- Search results are integrated into the brainstorming and drafting phases

#### Performance Metrics
- Every response now includes detailed performance metrics
- Track API latency, token usage, and efficiency
- Monitor the impact of web search on generation time

#### Content Moderation
- All generated posts are automatically screened for inappropriate content
- Moderated posts are replaced with user-friendly messages
- Helps ensure professional, appropriate content for LinkedIn

#### Error Handling
- **502 Bad Gateway**: AI service temporarily unavailable
- **400 Bad Request**: Invalid input parameters
- **500 Internal Server Error**: Unexpected server issues

### Sample Enhanced Request
```bash
curl -X POST "http://localhost:8000/generate_posts" \
-H "Content-Type: application/json" \
-d '{
    "topic": "remote work productivity",
    "tone": "inspirational",
    "audience": "remote workers",
    "post_count": 2,
    "use_web_search": true
}'
```

## License

This project is created for educational and demonstration purposes.

## Contributing

Feel free to submit issues and enhancement requests!
