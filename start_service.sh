#!/bin/bash
# Audio to Text Service Startup Script

echo "🎵 Starting Audio to Text Conversion Service..."

# Activate virtual environment
if [ -d "venv" ]; then
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Check if FFmpeg is available
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg not found. Please install FFmpeg first."
    exit 1
fi

# Start the service
echo "🚀 Starting service on http://localhost:5000"
python audio_to_text_service.py
