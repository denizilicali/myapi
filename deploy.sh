#!/bin/bash

# Niche Business APIs Suite - Deployment Script
echo "🚀 Deploying Niche Business APIs Suite..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cat > .env << EOF
# API Configuration
API_KEY=your_secret_api_key_here
DEBUG=True

# Database Configuration (for future use)
DATABASE_URL=sqlite:///./api_database.db

# Payment Configuration (for future use)
STRIPE_SECRET_KEY=your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=your_stripe_publishable_key

# Monitoring Configuration (for future use)
SENTRY_DSN=your_sentry_dsn

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000
EOF
    echo "✅ Created .env file. Please update with your actual API keys."
fi

# Create logs directory
mkdir -p logs

# Test the API
echo "🧪 Testing API..."
python -c "
import requests
import time
import sys

try:
    # Start the server in background
    import subprocess
    import threading
    
    def start_server():
        subprocess.run(['uvicorn', 'main:app', '--host', '0.0.0.0', '--port', '8000'], 
                      capture_output=True, text=True)
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    time.sleep(5)
    
    # Test the API
    response = requests.get('http://localhost:8000/')
    if response.status_code == 200:
        print('✅ API is running successfully!')
        print(f'📊 Response: {response.json()}')
    else:
        print(f'❌ API test failed with status code: {response.status_code}')
        sys.exit(1)
        
except Exception as e:
    print(f'❌ Error testing API: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Deployment successful!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Update the .env file with your actual API keys"
    echo "2. Run: uvicorn main:app --host 0.0.0.0 --port 8000"
    echo "3. Visit: http://localhost:8000/docs for API documentation"
    echo "4. Visit: http://localhost:8000/ for API status"
    echo ""
    echo "💰 Revenue Opportunities:"
    echo "- Content Moderation: $0.01-0.05 per request"
    echo "- Crypto Analytics: $0.02-0.10 per request"
    echo "- Email Validation: $0.005-0.02 per email"
    echo "- Sentiment Analysis: $0.01-0.03 per analysis"
    echo "- PDF Processing: $0.05-0.20 per document"
    echo "- Weather BI: $0.01-0.05 per analysis"
    echo ""
    echo "🚀 Start monetizing your APIs today!"
else
    echo "❌ Deployment failed. Please check the error messages above."
    exit 1
fi 