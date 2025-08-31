# LinkedIn Post Generator 

A comprehensive web application designed for generating professional LinkedIn content using advanced agentic AI architecture. Built with FastAPI backend and modern HTML/CSS/JavaScript frontend, featuring an enterprise-grade dark theme, real-time streaming capabilities, and comprehensive user feedback systems.

## **Core Features**

### **Professional User Interface Design**
- **Modern Dark Theme** with navy background (#0A0E1A) for professional corporate environments
- **Strategic Purple Accents** (#8B5CF6) for interactive elements and brand consistency
- **Inter Font Family** for optimal readability and professional typography standards
- **Single-Column Layout** designed for focused, distraction-free user experience
- **Minimalist Design** with strategic whitespace and clean visual hierarchy
- **High-Contrast Content Cards** with professional shadows for enhanced readability

### **Real-Time Streaming Technology**
- **Live Progress Monitoring** during content generation with detailed status indicators
- **Progressive Content Rendering** allowing users to monitor creation process in real-time
- **Dynamic Progress Tracking** with comprehensive status messages and completion metrics
- **Streaming Performance Analytics** providing detailed insights into generation efficiency

### **User Feedback & Analytics Framework**
- **Professional Rating System** with thumbs up/down functionality for quality assessment
- **Immediate Visual Confirmation** when feedback is successfully submitted
- **Backend Analytics Integration** with comprehensive logging of user ratings for continuous improvement
- **Enterprise-Grade Feedback UI** with smooth animations and responsive design principles

## **Advanced Capabilities**

### **Real-Time Web Research Integration**
- Comprehensive web search functionality to enhance content with current, factual information
- Privacy-focused DuckDuckGo search integration for reliable, unbiased data retrieval
- Seamless integration of research context into the advanced agentic AI workflow

### **Performance Analytics Dashboard**
- Real-time tracking and analysis of API latency and token usage statistics
- Comprehensive visual metrics displaying generation time, API calls, and system efficiency
- Performance optimization insights and actionable recommendations for users

### **Enterprise Content Moderation & Safety**
- Automated filtering of inappropriate content with intelligent detection algorithms
- Advanced pattern recognition for spam detection and excessive formatting prevention
- Professional moderation messaging with constructive retry suggestions and guidance

### **Enterprise-Grade Error Handling**
- Comprehensive exception handling for different error types and scenarios
- Graceful system degradation when external services are temporarily unavailable
- Detailed error messaging with clear recovery instructions and troubleshooting guidance

## **System Architecture**

- **Advanced Agentic AI Logic**: Multi-stage process for generating professional-grade content
  - Stage 0: Real-time web research integration (optional)
  - Stage A: Strategic brainstorming of unique angles for specified topics
  - Stage B: Professional content drafting with customizable tone and target audience parameters
  - Stage C: Strategic hashtag integration and compelling call-to-action optimization
  - Stage D: Comprehensive content moderation and safety validation

- **Professional Web Interface**: Clean, responsive design with real-time performance metrics
- **Customizable Parameters**: 
  - Topic specification (required)
  - Tone selection (professional, casual, inspirational, etc.)
  - Target audience definition
  - Content volume (1-10 posts)
  - Web search enhancement toggle

- **Enterprise Features**:
  - Copy-to-clipboard functionality
  - User feedback collection and analytics
  - Streaming API responses with real-time updates
  - Performance metrics dashboard
  - Content moderation indicators
  - Real-time validation and comprehensive error handling
  - API documentation with Swagger UI integration

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
