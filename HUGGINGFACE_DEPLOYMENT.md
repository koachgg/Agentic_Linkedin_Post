# 🤗 Hugging Face Spaces Deployment Guide

This guide provides step-by-step instructions to deploy the LinkedIn Post Generator to Hugging Face Spaces using Docker.

## Prerequisites

1. **Hugging Face Account**: Create a free account at [huggingface.co](https://huggingface.co)
2. **GitHub Repository**: Your code should be pushed to a GitHub repository
3. **Groq API Key**: Get your free API key from [console.groq.com](https://console.groq.com)

## Step 1: Prepare Your Repository

Ensure your GitHub repository contains all necessary files:

```
linkedin-post-generator/
├── Dockerfile              # Docker configuration
├── docker_app.py          # Docker entry point
├── main.py                # FastAPI application
├── post_generator.py      # Core logic
├── requirements.txt       # Python dependencies
├── config.json           # Configuration file
├── static/               # Frontend files
│   ├── index.html
│   ├── style.css
│   └── script.js
└── README.md             # Documentation
```

## Step 2: Push to GitHub (if not already done)

1. **Initialize Git repository** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Hugging Face deployment"
   ```

2. **Create GitHub repository**:
   - Go to [github.com/new](https://github.com/new)
   - Repository name: `linkedin-post-generator`
   - Make it public (required for free Hugging Face Spaces)
   - Click "Create repository"

3. **Push your code**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/linkedin-post-generator.git
   git branch -M main
   git push -u origin main
   ```

## Step 3: Create Hugging Face Space

1. **Go to Hugging Face Spaces**:
   - Visit [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"

2. **Configure your Space**:
   - **Space name**: `linkedin-post-generator` (or your preferred name)
   - **License**: Apache-2.0 (recommended)
   - **Select SDK**: Choose **Docker**
   - **Hardware**: CPU basic (free tier)
   - **Visibility**: Public

3. **Click "Create Space"**

## Step 4: Connect to GitHub

1. **In your new Space**, go to **Settings** tab

2. **Connect to GitHub**:
   - Scroll to "Repository"
   - Click "Connect to GitHub"
   - Authorize Hugging Face to access your GitHub account
   - Select your repository: `YOUR_USERNAME/linkedin-post-generator`
   - Branch: `main`
   - Click "Connect"

## Step 5: Configure Environment Variables

1. **In Space Settings**, scroll to **"Repository secrets"**

2. **Add GROQ_API_KEY**:
   - Click "New secret"
   - Name: `GROQ_API_KEY`
   - Value: Your Groq API key from console.groq.com
   - Click "Add secret"

## Step 6: Deploy and Monitor

1. **Automatic Build**:
   - Hugging Face will automatically detect your Dockerfile
   - The build process will start automatically
   - Monitor progress in the "Logs" tab

2. **Build Process** (takes 3-5 minutes):
   ```
   Building Docker image...
   Installing dependencies from requirements.txt...
   Starting application on port 7860...
   ```

3. **Successful Deployment**:
   - You'll see: "🚀 Starting LinkedIn Post Generator on 0.0.0.0:7860"
   - Your app will be available at: `https://YOUR_USERNAME-linkedin-post-generator.hf.space`

## Step 7: Test Your Deployment

1. **Access your app** at the provided URL
2. **Test functionality**:
   - Enter a topic in the input field
   - Click "Generate LinkedIn Post"
   - Verify AI-powered post generation works
   - Test copy-to-clipboard functionality

## Configuration Files

### Dockerfile
```dockerfile
# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run the application
CMD ["python", "docker_app.py"]
```

### docker_app.py
```python
#!/usr/bin/env python3
import os
import uvicorn
from main import app

def main():
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 7860))
    
    print(f"🚀 Starting LinkedIn Post Generator on {host}:{port}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        reload=False
    )

if __name__ == "__main__":
    main()
```

## Troubleshooting

### Build Failures

**Dependency Issues**:
```
ERROR: Could not find a version that satisfies the requirement...
```
**Solution**: Update `requirements.txt` with compatible versions:
```
fastapi==0.104.1
uvicorn==0.24.0
groq==0.9.0
duckduckgo-search==6.2.13
httpx>=0.27.0
```

**Port Issues**:
```
ERROR: [Errno 98] Address already in use
```
**Solution**: Hugging Face Spaces uses port 7860 automatically. Ensure `docker_app.py` uses `PORT` environment variable.

### Runtime Issues

**GROQ_API_KEY Missing**:
- Check Space Settings → Repository secrets
- Ensure secret name is exactly `GROQ_API_KEY`
- Restart the Space after adding secrets

**Application Not Loading**:
1. Check Logs tab for error messages
2. Verify all files are in GitHub repository
3. Ensure Dockerfile syntax is correct

### Performance Issues

**Slow Response Times**:
- Free CPU tier has limitations
- Consider upgrading to CPU basic or GPU for better performance
- Optimize code for faster execution

## Updates and Maintenance

### Updating Your App

1. **Make changes** to your local code
2. **Commit and push** to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
3. **Automatic rebuild**: Hugging Face will automatically rebuild your Space

### Monitoring

- **Check Logs**: Monitor application logs in the Logs tab
- **Usage Analytics**: View usage statistics in your Space dashboard
- **Error Tracking**: Monitor for errors and fix issues promptly

## Cost Considerations

- **Free Tier**: CPU basic is free with limitations
- **Paid Tiers**: Available for better performance
- **Usage Limits**: Monitor your usage to avoid unexpected charges

## Security Best Practices

1. **API Keys**: Always use environment variables, never hard-code
2. **Repository**: Keep sensitive data out of your repository
3. **Updates**: Regularly update dependencies for security

## Support and Community

- **Hugging Face Forums**: [discuss.huggingface.co](https://discuss.huggingface.co)
- **Discord**: Hugging Face Discord community
- **Documentation**: [huggingface.co/docs/hub/spaces](https://huggingface.co/docs/hub/spaces)

---

🎉 **Congratulations!** Your LinkedIn Post Generator is now deployed on Hugging Face Spaces and accessible worldwide!

Your app URL: `https://YOUR_USERNAME-linkedin-post-generator.hf.space`
