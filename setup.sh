#!/bin/bash

# Audio to Text Service Setup Script
# This script sets up the environment and installs dependencies

set -e  # Exit on any error

echo "🎵 Audio to Text Conversion Service Setup"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION found"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version 2>&1 | cut -d' ' -f2)
        if [[ $PYTHON_VERSION == 3.* ]]; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python"
        else
            print_error "Python 3 is required. Found Python $PYTHON_VERSION"
            exit 1
        fi
    else
        print_error "Python is not installed. Please install Python 3.7 or higher."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        print_error "pip is not installed. Please install pip."
        exit 1
    fi
    print_success "pip found"
}

# Check if FFmpeg is installed
check_ffmpeg() {
    print_status "Checking FFmpeg installation..."
    if command -v ffmpeg &> /dev/null; then
        FFMPEG_VERSION=$(ffmpeg -version 2>&1 | head -n1 | cut -d' ' -f3)
        print_success "FFmpeg $FFMPEG_VERSION found"
    else
        print_warning "FFmpeg not found. This is required for audio format conversion."
        print_status "Installing FFmpeg..."
        
        # Detect OS and install FFmpeg
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS
            if command -v brew &> /dev/null; then
                brew install ffmpeg
                print_success "FFmpeg installed via Homebrew"
            else
                print_error "Homebrew not found. Please install FFmpeg manually:"
                print_error "  brew install ffmpeg"
                exit 1
            fi
        elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
            # Linux
            if command -v apt-get &> /dev/null; then
                sudo apt-get update
                sudo apt-get install -y ffmpeg
                print_success "FFmpeg installed via apt-get"
            elif command -v yum &> /dev/null; then
                sudo yum install -y ffmpeg
                print_success "FFmpeg installed via yum"
            else
                print_error "Package manager not found. Please install FFmpeg manually."
                exit 1
            fi
        else
            print_error "Unsupported operating system. Please install FFmpeg manually."
            exit 1
        fi
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    print_success "Virtual environment activated"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    $PIP_CMD install --upgrade pip
    $PIP_CMD install -r requirements.txt
    print_success "Dependencies installed"
}

# Install system dependencies for PocketSphinx (Linux/macOS)
install_system_deps() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_status "Installing system dependencies for PocketSphinx..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y portaudio19-dev python3-pyaudio
            print_success "System dependencies installed"
        else
            print_warning "Could not install system dependencies automatically"
            print_warning "You may need to install portaudio19-dev and python3-pyaudio manually"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        print_status "Installing system dependencies for PocketSphinx..."
        if command -v brew &> /dev/null; then
            brew install portaudio
            print_success "System dependencies installed"
        else
            print_warning "Could not install system dependencies automatically"
            print_warning "You may need to install portaudio manually"
        fi
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    $PYTHON_CMD -c "
import speech_recognition as sr
import pydub
from flask import Flask
print('✅ All imports successful')
"
    print_success "Installation test passed"
}

# Create startup script
create_startup_script() {
    print_status "Creating startup script..."
    cat > start_service.sh << 'EOF'
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
EOF

    chmod +x start_service.sh
    print_success "Startup script created: start_service.sh"
}

# Main setup process
main() {
    echo ""
    print_status "Starting setup process..."
    echo ""
    
    check_python
    check_pip
    check_ffmpeg
    create_venv
    activate_venv
    install_dependencies
    install_system_deps
    test_installation
    create_startup_script
    
    echo ""
    print_success "🎉 Setup completed successfully!"
    echo ""
    echo "To start the service:"
    echo "  ./start_service.sh"
    echo ""
    echo "Or manually:"
    echo "  source venv/bin/activate  # (or venv\\Scripts\\activate on Windows)"
    echo "  python audio_to_text_service.py"
    echo ""
    echo "Then open your browser to: http://localhost:5000"
    echo ""
}

# Run main function
main "$@"
