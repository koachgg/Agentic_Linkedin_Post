# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and asset downloader
COPY requirements.txt download_assets.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download and vendor external assets (Tailwind CSS, Chart.js)
# This ensures dependencies are available locally, bypassing CSP issues
RUN python download_assets.py

# Copy application files
COPY . .

# Expose port 7860 (Hugging Face Spaces default)
EXPOSE 7860

# Run the application
CMD ["python", "docker_app.py"]
