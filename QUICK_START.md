# Quick Start Guide - LinkedIn Post Generator

## 🚀 How to Run Locally

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- A Groq API key (optional, works with mock data without it)

### Step 1: Navigate to Project Directory
```bash
cd c:\Users\abhig\Documents\Belo\Nugget\linkedin-post-generator
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set Up Configuration (Optional)
Create a `config.json` file with your Groq API key:
```json
{
  "groq_api_key": "your_groq_api_key_here"
}
```

**Note:** If you don't have an API key, the app will work with mock responses for testing.

### Step 4: Run the Application
```bash
python main.py
```

### Step 5: Open in Browser
The application will start and display:
```
🚀 Starting LinkedIn Post Generator API...
📖 API Documentation available at: http://localhost:8000/docs
🌐 Web Interface available at: http://localhost:8000
```

Open your browser and go to: **http://localhost:8000**

## 🎯 Quick Test

1. Enter a topic like "artificial intelligence"
2. Select a tone (optional)
3. Enter target audience (optional)
4. Choose number of posts (1-10)
5. Optionally enable web search
6. Click "Generate Posts"
7. Watch the streaming progress and real-time post generation!
8. Use the feedback buttons (👍/👎) on generated posts

## 🔧 Troubleshooting

### Common Issues:

**Port Already in Use:**
```bash
# Kill any existing processes on port 8000
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

**Missing Dependencies:**
```bash
pip install fastapi uvicorn pydantic aiohttp duckduckgo-search
```

**Python Not Found:**
Make sure Python is installed and added to your PATH.

## 🌐 API Documentation
Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

## 🎨 Features to Try

- **Dark Theme**: Enjoy the Nugget.com-inspired dark UI
- **Streaming**: Watch posts generate in real-time
- **Feedback**: Rate posts with thumbs up/down
- **Web Search**: Enable for current information
- **Copy Function**: One-click copy to clipboard
- **Performance Metrics**: See generation statistics

Enjoy generating amazing LinkedIn posts! 🚀
