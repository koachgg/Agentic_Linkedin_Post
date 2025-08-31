#!/usr/bin/env python3
"""
Hugging Face Spaces deployment preparation and validation script.
This script ensures all files are ready for HF Spaces deployment.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def print_banner():
    """Print the deployment banner"""
    print("=" * 60)
    print("🤗 HUGGING FACE SPACES DEPLOYMENT VALIDATOR")
    print("=" * 60)
    print()

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ Missing {description}: {filepath}")
        return False

def check_docker_files():
    """Validate Docker configuration files"""
    print("🐳 Checking Docker Configuration...")
    
    files_ok = True
    files_ok &= check_file_exists("Dockerfile", "Docker configuration")
    files_ok &= check_file_exists("docker_app.py", "Docker entry point")
    files_ok &= check_file_exists(".dockerignore", "Docker ignore file")
    files_ok &= check_file_exists("requirements.txt", "Python dependencies")
    
    return files_ok

def check_application_files():
    """Validate application files"""
    print("\n📱 Checking Application Files...")
    
    files_ok = True
    files_ok &= check_file_exists("main.py", "FastAPI application")
    files_ok &= check_file_exists("post_generator.py", "AI post generator")
    files_ok &= check_file_exists("static/index.html", "Main web interface")
    files_ok &= check_file_exists("static/linkedin_post_generator_infographic.html", "Infographic page")
    files_ok &= check_file_exists("static/style.css", "Application styles")
    files_ok &= check_file_exists("static/script.js", "Application JavaScript")
    
    return files_ok

def check_huggingface_config():
    """Check Hugging Face specific configuration"""
    print("\n🤗 Checking Hugging Face Configuration...")
    
    files_ok = True
    files_ok &= check_file_exists("README_HF.md", "Hugging Face README")
    
    # Check Dockerfile for correct port
    try:
        with open("Dockerfile", "r") as f:
            dockerfile_content = f.read()
            if "EXPOSE 7860" in dockerfile_content:
                print("✅ Docker port 7860 configured")
            else:
                print("❌ Docker port 7860 not found")
                files_ok = False
                
            if 'CMD ["python", "docker_app.py"]' in dockerfile_content:
                print("✅ Docker entry point configured")
            else:
                print("❌ Docker entry point not configured correctly")
                files_ok = False
    except FileNotFoundError:
        print("❌ Dockerfile not found")
        files_ok = False
    
    return files_ok

def check_dependencies():
    """Check Python dependencies"""
    print("\n📦 Checking Dependencies...")
    
    try:
        with open("requirements.txt", "r") as f:
            deps = f.read()
            required_deps = ["fastapi", "uvicorn", "groq", "aiohttp", "pydantic"]
            
            for dep in required_deps:
                if dep in deps.lower():
                    print(f"✅ {dep} dependency found")
                else:
                    print(f"❌ {dep} dependency missing")
                    return False
        return True
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def validate_main_py():
    """Validate main.py has infographic endpoint"""
    print("\n🔍 Checking main.py configuration...")
    
    try:
        with open("main.py", "r", encoding="utf-8") as f:
            content = f.read()
            
            if "/infographic" in content:
                print("✅ Infographic endpoint found in main.py")
                return True
            else:
                print("❌ Infographic endpoint not found in main.py")
                return False
    except FileNotFoundError:
        print("❌ main.py not found")
        return False
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open("main.py", "r", encoding="latin-1") as f:
                content = f.read()
                if "/infographic" in content:
                    print("✅ Infographic endpoint found in main.py")
                    return True
                else:
                    print("❌ Infographic endpoint not found in main.py")
                    return False
        except:
            print("❌ Could not read main.py due to encoding issues")
            return False

def generate_deployment_summary():
    """Generate deployment summary and next steps"""
    print("\n📋 DEPLOYMENT SUMMARY")
    print("=" * 40)
    
    summary = """
🎯 READY FOR HUGGING FACE SPACES!

📂 Your project structure:
├── Dockerfile                 # HF Spaces configuration
├── docker_app.py             # Application entry point  
├── main.py                   # FastAPI backend
├── post_generator.py         # AI logic
├── requirements.txt          # Dependencies
├── static/
│   ├── index.html           # Main interface
│   ├── infographic.html     # Analytics page
│   ├── style.css           # Styling
│   └── script.js           # Frontend logic
└── README_HF.md            # HF Spaces description

🚀 DEPLOYMENT STEPS:
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose "Docker" as SDK
4. Connect to your GitHub repository
5. Set GROQ_API_KEY in Space secrets
6. Deploy and test!

🔗 SPACE URLS (after deployment):
- Main App: https://your-username-space-name.hf.space/
- Infographic: https://your-username-space-name.hf.space/infographic
- API Docs: https://your-username-space-name.hf.space/docs

💡 TIPS:
- Use CPU basic (free tier) for testing
- Upgrade to GPU for better performance
- Monitor logs during deployment
- Test all endpoints after deployment
"""
    
    print(summary)

def main():
    """Main validation function"""
    print_banner()
    
    all_checks_passed = True
    
    # Run all validations
    all_checks_passed &= check_docker_files()
    all_checks_passed &= check_application_files()
    all_checks_passed &= check_huggingface_config()
    all_checks_passed &= check_dependencies()
    all_checks_passed &= validate_main_py()
    
    print("\n" + "=" * 60)
    
    if all_checks_passed:
        print("🎉 ALL CHECKS PASSED!")
        generate_deployment_summary()
    else:
        print("❌ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before deploying to Hugging Face Spaces.")
        print("📖 See HUGGINGFACE_DEPLOYMENT.md for detailed instructions.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
