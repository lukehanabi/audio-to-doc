# 🎵 Audio to Text Conversion Service

A comprehensive web service that converts audio files to text with support for multiple audio formats and languages including Spanish, English, and many others. **Dockerized and ready for deployment on Render.com!**

## ✨ Features

- **Multiple Audio Formats**: Supports MP3, WAV, AAC, M4A, OGG, FLAC, WMA, MP4, WebM
- **Multi-Language Support**: Spanish, English, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and more
- **Auto-Detection**: Automatic language detection when language is set to "auto"
- **Multiple Recognition Engines**: Google Speech Recognition (online) and PocketSphinx (offline)
- **Modern Web Interface**: Beautiful, responsive web UI with drag-and-drop support
- **REST API**: Full API endpoints for integration with other applications
- **Progress Tracking**: Real-time upload and processing progress
- **Error Handling**: Comprehensive error handling and user feedback

## 🚀 Quick Start

### Option 1: Docker (Recommended)

1. **Build and run with Docker:**
   ```bash
   # Build the image
   docker build -t audio-to-text-service .
   
   # Run the container
   docker run -p 5000:5000 audio-to-text-service
   ```

2. **Or use Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Open your browser:**
   Navigate to [http://localhost:5000](http://localhost:5000)

### Option 2: Local Development

1. **Prerequisites:**
   - Python 3.7+
   - FFmpeg installed

2. **Install FFmpeg:**
   ```bash
   # macOS
   brew install ffmpeg
   
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   ```

3. **Setup:**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run the service
   python audio_to_text_service.py
   ```

### Option 3: Deploy to Render.com

1. **Push to GitHub** (if not already done)
2. **Connect to Render.com:**
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
3. **Configure:**
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`
   - Plan: Choose based on your needs
4. **Deploy!**

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

## 📁 Project Structure

```
audio-to-text-service/
├── audio_to_text_service.py    # Main Flask application
├── templates/
│   └── index.html             # Web interface
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose for local development
├── render.yaml               # Render.com deployment configuration
├── .dockerignore             # Docker ignore file
├── test_service.py           # Test script
├── DEPLOYMENT.md             # Detailed deployment guide
├── README.md                 # This file
└── static/                   # Static files (created automatically)
```

## 🎯 Usage

### Web Interface

1. **Upload Audio File**: Drag and drop or click to select an audio file
2. **Select Language**: Choose the language of the audio (or "Auto" for detection)
3. **Convert**: Click "Convert to Text" and wait for processing
4. **Copy Result**: Use the copy button to copy the transcribed text

### API Endpoints

#### Convert Audio to Text
```http
POST /api/convert
Content-Type: multipart/form-data

Parameters:
- audio_file: Audio file (required)
- language: Language code (optional, default: 'auto')
```

**Example using curl:**
```bash
curl -X POST -F "audio_file=@example.mp3" -F "language=spanish" http://localhost:5000/api/convert
```

**Response:**
```json
{
  "success": true,
  "text": "Transcribed text here...",
  "confidence": 0.8,
  "language_detected": "es-ES",
  "service_used": "google",
  "filename": "example.mp3",
  "file_size": 1024000,
  "language_requested": "spanish"
}
```

#### Get Supported Formats
```http
GET /api/formats
```

#### Health Check
```http
GET /api/health
```

## 🌍 Supported Languages

| Language | Code | Status |
|----------|------|--------|
| Spanish | es-ES | ✅ |
| English (US) | en-US | ✅ |
| English (UK) | en-GB | ✅ |
| French | fr-FR | ✅ |
| German | de-DE | ✅ |
| Italian | it-IT | ✅ |
| Portuguese | pt-PT | ✅ |
| Russian | ru-RU | ✅ |
| Chinese | zh-CN | ✅ |
| Japanese | ja-JP | ✅ |
| Korean | ko-KR | ✅ |
| Arabic | ar-SA | ✅ |
| Hindi | hi-IN | ✅ |
| Auto-detect | auto | ✅ |

## 🎵 Supported Audio Formats

- **MP3** - Most common audio format
- **WAV** - Uncompressed audio
- **AAC** - Advanced Audio Coding
- **M4A** - iTunes audio format
- **OGG** - Open source audio format
- **FLAC** - Lossless audio compression
- **WMA** - Windows Media Audio
- **MP4** - Video container with audio
- **WebM** - Web-optimized format

## ⚙️ Configuration

### Environment Variables

You can customize the service using environment variables:

```bash
export FLASK_ENV=production          # Set to production mode
export MAX_CONTENT_LENGTH=50000000   # Max file size (50MB)
export UPLOAD_FOLDER=/tmp/uploads    # Upload directory
```

### Speech Recognition Settings

The service uses multiple recognition engines:

1. **Google Speech Recognition** (Primary)
   - Requires internet connection
   - Supports all languages
   - Higher accuracy

2. **PocketSphinx** (Fallback)
   - Works offline
   - English only
   - Lower accuracy but faster

## 🔧 Troubleshooting

### Common Issues

1. **"FFmpeg not found" error:**
   - Install FFmpeg and ensure it's in your system PATH
   - Restart the service after installation

2. **"No module named 'pocketsphinx'" error:**
   - Install system dependencies: `sudo apt-get install portaudio19-dev python3-pyaudio`
   - Then: `pip install pocketsphinx`

3. **Audio format not supported:**
   - Ensure FFmpeg is installed with all codecs
   - Check if the file is corrupted

4. **Recognition fails:**
   - Check internet connection (for Google Speech Recognition)
   - Try a different audio file
   - Ensure audio quality is good (clear speech, minimal background noise)

### Performance Tips

- **File Size**: Keep files under 100MB for best performance
- **Audio Quality**: Use clear, high-quality audio for better recognition
- **Language**: Specify the correct language for better accuracy
- **Format**: WAV files generally provide the best results

## 🚀 Deployment

### Production Deployment

For production deployment, consider using:

1. **Gunicorn** (WSGI server):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 audio_to_text_service:app
   ```

2. **Docker** (containerized deployment):
   ```dockerfile
   FROM python:3.9-slim
   RUN apt-get update && apt-get install -y ffmpeg
   COPY . /app
   WORKDIR /app
   RUN pip install -r requirements.txt
   EXPOSE 5000
   CMD ["python", "audio_to_text_service.py"]
   ```

3. **Nginx** (reverse proxy):
   Configure Nginx to proxy requests to the Flask application

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Ensure all dependencies are properly installed
3. Verify your audio file format and quality
4. Check the service logs for detailed error messages

---

**Happy transcribing! 🎤➡️📝**
