#!/bin/bash

# Word to PowerPoint Converter - Setup Script

set -e

echo "🔧 Setting up Word to PowerPoint Converter..."

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "❌ Python 3 is required"; exit 1; }

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p uploads/word_files uploads/temp
mkdir -p outputs/presentations outputs/previews
mkdir -p assets/fonts assets/templates assets/default_images
mkdir -p logs config tests/sample_files
mkdir -p static/js docs scripts

# Create default images (placeholder)
echo "Creating placeholder images..."
python -c "
from PIL import Image, ImageDraw
import os

# Create default images directory
os.makedirs('assets/default_images', exist_ok=True)

# Title background
img = Image.new('RGB', (1920, 1080), color=(41, 128, 185))
draw = ImageDraw.Draw(img)
draw.rectangle([(0, 400), (1920, 680)], fill=(52, 152, 219))
img.save('assets/default_images/title_bg.jpg')

# Section background
img = Image.new('RGB', (1920, 1080), color=(39, 174, 96))
draw = ImageDraw.Draw(img)
for i in range(0, 1920, 50):
    draw.line([(i, 0), (i, 1080)], fill=(46, 204, 113), width=2)
img.save('assets/default_images/section_bg.jpg')

# Content background
img = Image.new('RGB', (1920, 1080), color=(142, 68, 173))
draw = ImageDraw.Draw(img)
draw.ellipse([(400, 200), (1520, 880)], outline=(155, 89, 182), width=10)
img.save('assets/default_images/content_bg.jpg')
"

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# OpenAI API Key (required for AI features)
OPENAI_API_KEY=your_openai_api_key_here

# Unsplash Access Key (required for image fetching)
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

# Flask Secret Key (for session security)
FLASK_SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(32))")

# Optional: Customize AI behavior
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.5
EOL
    echo "⚠️  Please update the .env file with your API keys!"
fi

# Create sample Word document for testing
echo "Creating sample documents..."
cat > tests/sample_files/sample1.docx << 'EOL'
This is a sample Word document for testing.

# Introduction
This document demonstrates the capabilities of the Word to PowerPoint converter.

## Features
The converter has several amazing features:
1. AI-powered summarization
2. Automatic image selection
3. Multiple template support
4. Real-time preview

### How It Works
The system processes your Word document, extracts headings and content, then creates a beautiful presentation with relevant images and concise summaries.

## Benefits
Save time by automatically converting documents to presentations. Focus on content while the tool handles formatting and design.

# Conclusion
Try it out with your own documents!
EOL

# Make scripts executable
chmod +x scripts/*.sh 2>/dev/null || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your API keys"
echo "2. Activate virtual environment: source venv/bin/activate"
echo "3. Run the app: python app.py"
echo "4. Open browser: http://localhost:5000"
echo ""