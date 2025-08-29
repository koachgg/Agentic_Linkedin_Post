#!/usr/bin/env python3
"""
Quick deployment script for Hugging Face Spaces.
This script helps automate the preparation for Hugging Face deployment.
"""

import os
import sys
import subprocess
import json

def print_banner():
    """Print deployment banner."""
    print("=" * 60)
    print("🤗 HUGGING FACE SPACES - LINKEDIN POST GENERATOR")
    print("=" * 60)
    print()

def check_requirements():
    """Check if all required files exist."""
    required_files = [
        "Dockerfile",
        "docker_app.py", 
        "main.py",
        "post_generator.py",
        "requirements.txt",
        "config.json",
        "static/index.html",
        "static/style.css",
        "static/script.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def check_docker_config():
    """Verify Docker configuration."""
    try:
        with open("Dockerfile", "r") as f:
            dockerfile_content = f.read()
            
        if "CMD [\"python\", \"docker_app.py\"]" not in dockerfile_content:
            print("❌ Dockerfile missing correct CMD instruction")
            return False
            
        if "EXPOSE 7860" not in dockerfile_content:
            print("❌ Dockerfile missing port 7860 exposure")
            return False
            
        print("✅ Dockerfile configuration correct")
        return True
        
    except FileNotFoundError:
        print("❌ Dockerfile not found")
        return False

def check_dependencies():
    """Check requirements.txt for essential dependencies."""
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().lower()
            
        essential_deps = ["fastapi", "uvicorn", "groq"]
        missing_deps = []
        
        for dep in essential_deps:
            if dep not in requirements:
                missing_deps.append(dep)
        
        if missing_deps:
            print("❌ Missing essential dependencies:")
            for dep in missing_deps:
                print(f"   - {dep}")
            return False
            
        print("✅ Essential dependencies present")
        return True
        
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False

def check_git_status():
    """Check Git repository status."""
    try:
        # Check if we're in a Git repository
        result = subprocess.run(["git", "status"], 
                              capture_output=True, text=True, shell=True)
        
        if result.returncode != 0:
            print("❌ Not a Git repository. Run 'git init' first.")
            return False
            
        # Check for uncommitted changes
        if "nothing to commit" not in result.stdout:
            print("⚠️  You have uncommitted changes:")
            print("   Run 'git add . && git commit -m \"Prepare for Hugging Face deployment\"'")
            return False
            
        print("✅ Git repository is clean")
        return True
        
    except FileNotFoundError:
        print("❌ Git not found. Please install Git.")
        return False

def generate_deployment_checklist():
    """Generate a deployment checklist."""
    checklist = """
🚀 HUGGING FACE SPACES DEPLOYMENT CHECKLIST

Pre-deployment:
□ All files present and correct
□ Docker configuration validated
□ Dependencies verified
□ Git repository clean and committed
□ Groq API key ready

Deployment Steps:
□ 1. Push code to GitHub repository
□ 2. Create new Hugging Face Space (Docker SDK)
□ 3. Connect Space to GitHub repository
□ 4. Add GROQ_API_KEY as repository secret
□ 5. Monitor build logs
□ 6. Test deployed application

Post-deployment:
□ Verify application functionality
□ Test API endpoints
□ Check error logs
□ Share application URL

📋 Deployment URL: https://YOUR_USERNAME-linkedin-post-generator.hf.space
📋 Build logs: Available in Space settings
📋 Support: https://discuss.huggingface.co
"""
    
    with open("HF_DEPLOYMENT_CHECKLIST.md", "w") as f:
        f.write(checklist)
    
    print("📋 Deployment checklist saved to HF_DEPLOYMENT_CHECKLIST.md")

def main():
    """Main deployment preparation function."""
    print_banner()
    
    print("🔍 Checking deployment readiness...\n")
    
    all_checks_passed = True
    
    # Run all checks
    all_checks_passed &= check_requirements()
    all_checks_passed &= check_docker_config()
    all_checks_passed &= check_dependencies()
    all_checks_passed &= check_git_status()
    
    print("\n" + "=" * 60)
    
    if all_checks_passed:
        print("🎉 READY FOR DEPLOYMENT!")
        print("\nNext steps:")
        print("1. Push to GitHub: git push origin main")
        print("2. Create Hugging Face Space")
        print("3. Connect to GitHub repository")
        print("4. Add GROQ_API_KEY secret")
        print("5. Monitor build and test")
        
        generate_deployment_checklist()
        
    else:
        print("❌ DEPLOYMENT NOT READY")
        print("\nPlease fix the issues above before deploying.")
        
    print("\n📖 Full guide: HUGGINGFACE_DEPLOYMENT.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
