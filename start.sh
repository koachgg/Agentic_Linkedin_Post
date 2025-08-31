#!/bin/bash
# Railway startup script to debug environment variables

echo "=== RAILWAY ENVIRONMENT DEBUG ==="
echo "GROQ_API_KEY set: ${GROQ_API_KEY:+YES}"
echo "GROQ_API_KEY length: ${#GROQ_API_KEY}"
echo "All environment variables:"
env | grep -E "(GROQ|RAILWAY|PORT)" | sort

echo "=== STARTING APPLICATION ==="
python -m uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
