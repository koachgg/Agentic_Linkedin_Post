# LinkedIn Post Generator

A fully functional web application that generates engaging LinkedIn posts using AI. Built with FastAPI backend and modern HTML/CSS/JavaScript frontend.

## Features

- **Agentic AI Logic**: Multi-step process for generating high-quality posts
  - Step A: Brainstorming unique angles for your topic
  - Step B: Drafting engaging posts with customizable tone and audience
  - Step C: Adding relevant hashtags and compelling call-to-actions

- **Professional Web Interface**: Clean, responsive design with card-based post display
- **Customizable Parameters**: 
  - Topic (required)
  - Tone (professional, casual, inspirational, etc.)
  - Target audience
  - Number of posts (1-10)

- **Copy-to-Clipboard**: Easy sharing with one-click copy functionality
- **Real-time Validation**: Form validation and error handling
- **API Documentation**: Built-in Swagger UI for API testing

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

## License

This project is created for educational and demonstration purposes.

## Contributing

Feel free to submit issues and enhancement requests!
