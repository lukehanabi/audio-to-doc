# 🎵 Audio to Text Conversion Service

A comprehensive **offline-only** web service that converts audio files to text with support for multiple audio formats and languages. **Dockerized and optimized for deployment on Render.com with multithreading support!**

## ✨ Features

- **🎯 Offline-Only Processing**: Uses Vosk for speech recognition - no internet required
- **📄 Word Document Output**: Generates professional .docx files with transcribed text
- **🔄 Audio Format Conversion**: Convert between different audio formats (MP3, WAV, AAC, etc.)
- **🌍 Multi-Language Support**: Spanish, English with auto-detection
- **⚡ Multithreading**: Handles up to 5 concurrent requests with smart queue management
- **🎨 Modern Web Interface**: Clean, minimalist UI with drag-and-drop support
- **📊 Real-time Monitoring**: Queue status and health check endpoints
- **🐳 Docker Ready**: Optimized for cloud deployment with memory efficiency
- **📱 Responsive Design**: Works on desktop and mobile devices

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

### Option 2: Deploy to Render.com

1. **Push to GitHub** (if not already done)
2. **Connect to Render.com:**
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
3. **Configure:**
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`
   - Plan: Choose based on your needs (512MB+ recommended)
4. **Deploy!**

## 📁 Project Structure

```
audio-to-text-service/
├── audio_to_text_service.py    # Main Flask application
├── templates/
│   └── index.html             # Web interface
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker configuration
├── docker-compose.yml         # Docker Compose for local development
├── README.md                  # This file
└── static/                   # Static files (created automatically)
```

## 🎯 Usage

### Web Interface

1. **Upload Audio File**: Drag and drop or click to select an audio file
2. **Select Language**: Choose Spanish, English, or Auto-detect
3. **Choose Action**:
   - **Convert to Word Document**: Transcribe audio and download as .docx
   - **Convert Audio Format Only**: Convert between audio formats
4. **Download Result**: Get your Word document or converted audio file

### API Endpoints

#### Convert Audio to Word Document
```http
POST /api/convert
Content-Type: multipart/form-data

Parameters:
- audio_file: Audio file (required)
- language: Language (optional: 'spanish', 'english', 'auto')
```

**Example using curl:**
```bash
curl -X POST -F "audio_file=@example.mp3" -F "language=spanish" \
  http://localhost:5000/api/convert \
  --output transcription.docx
```

#### Convert Audio Format Only
```http
POST /api/convert-audio
Content-Type: multipart/form-data

Parameters:
- audio_file: Audio file (required)
- output_format: Output format (required: 'wav', 'mp3', 'aac', 'm4a', 'ogg', 'flac')
```

**Example using curl:**
```bash
curl -X POST -F "audio_file=@example.wav" -F "output_format=mp3" \
  http://localhost:5000/api/convert-audio \
  --output converted.mp3
```

#### Get Service Status
```http
GET /api/status
```

**Response:**
```json
{
  "status": "running",
  "active_requests": 2,
  "max_concurrent_requests": 5,
  "queue_size": 0,
  "can_accept_requests": true
}
```

#### Health Check
```http
GET /api/health
```

#### Get Supported Formats
```http
GET /api/formats
```

## 🌍 Supported Languages

| Language | Code | Status | Model |
|----------|------|--------|-------|
| Spanish | es-ES | ✅ | vosk-model-small-es-0.42 |
| English (US) | en-US | ✅ | vosk-model-small-en-us-0.15 |
| Auto-detect | auto | ✅ | Based on selection |

## 🎵 Supported Audio Formats

### Input Formats
- **MP3** - Most common audio format
- **WAV** - Uncompressed audio
- **AAC** - Advanced Audio Coding
- **M4A** - iTunes audio format
- **OGG** - Open source audio format
- **FLAC** - Lossless audio compression
- **WMA** - Windows Media Audio
- **MP4** - Video container with audio
- **WebM** - Web-optimized format

### Output Formats (Audio Conversion)
- **WAV** - Uncompressed audio
- **MP3** - Compressed audio
- **AAC** - Advanced Audio Coding
- **M4A** - iTunes audio format
- **OGG** - Open source audio format
- **FLAC** - Lossless audio compression

## ⚡ Performance & Multithreading

### Current Configuration
- **3 Gunicorn Workers** with **2 threads each**
- **Maximum 5 concurrent requests**
- **600-second timeout** for large files
- **Smart queue management** with overload protection
- **Request recycling** (workers restart after 100 requests)

### Memory Optimization
- **Offline-only processing** (no internet dependencies)
- **Optimized Vosk models** (Spanish + English only)
- **Efficient audio processing** with direct format support
- **25MB file size limit** to prevent memory issues

## ⚙️ Configuration

### Environment Variables

```bash
export MAX_CONTENT_LENGTH=26214400    # Max file size (25MB)
export UPLOAD_FOLDER=/tmp/uploads     # Upload directory
export SECRET_KEY=your-secret-key     # Flask secret key
```

### Multithreading Settings

You can adjust these values in `audio_to_text_service.py`:

```python
max_concurrent_requests = 5  # Maximum concurrent requests
```

And in `Dockerfile`:

```dockerfile
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--threads", "2", ...]
```

## 🔧 Troubleshooting

### Common Issues

1. **"Server is busy" error (503):**
   - The service is handling maximum concurrent requests
   - Wait a few moments and try again
   - Check `/api/status` for current queue status

2. **"File too large" error:**
   - Maximum file size is 25MB
   - Compress your audio file or use a shorter recording

3. **"No speech detected" error:**
   - Ensure audio contains clear speech
   - Check audio quality and volume
   - Try a different audio file

4. **"Unsupported format" error:**
   - Check if your audio format is supported
   - Convert to a supported format first

### Performance Tips

- **File Size**: Keep files under 25MB for optimal performance
- **Audio Quality**: Use clear, high-quality audio for better recognition
- **Language**: Specify the correct language for better accuracy
- **Format**: WAV files generally provide the best results
- **Concurrent Requests**: Monitor `/api/status` to avoid queue overload

## 🚀 Deployment

### Production Deployment

The service is optimized for cloud deployment with:

1. **Docker Containerization**:
   - Multi-stage build for smaller image size
   - Health checks for container monitoring
   - Optimized for Render.com deployment

2. **Gunicorn Configuration**:
   - Multiple workers for concurrent processing
   - Threading support for better performance
   - Request recycling for memory management

3. **Memory Management**:
   - Offline-only processing (no internet dependencies)
   - Optimized model loading
   - Efficient audio processing

### Render.com Deployment

1. **Repository Setup**:
   ```bash
   git clone https://github.com/lukehanabi/audio-to-doc.git
   cd audio-to-doc
   ```

2. **Render.com Configuration**:
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`
   - Plan: 512MB+ recommended
   - Health Check: `/api/health`

3. **Environment Variables** (optional):
   - `MAX_CONTENT_LENGTH`: File size limit
   - `UPLOAD_FOLDER`: Upload directory
   - `SECRET_KEY`: Flask secret key

## 📊 Monitoring

### Health Check
```bash
curl http://your-service-url/api/health
```

### Status Monitoring
```bash
curl http://your-service-url/api/status
```

### Logs
Check your deployment platform's logs for detailed information about:
- Request processing
- Queue status
- Error messages
- Performance metrics

## 🔄 Recent Updates

### Version 2.0 Features
- ✅ **Offline-only processing** with Vosk
- ✅ **Word document output** (.docx files)
- ✅ **Audio format conversion** functionality
- ✅ **Multithreading support** (5 concurrent requests)
- ✅ **Memory optimization** for cloud deployment
- ✅ **Queue management** with overload protection
- ✅ **Real-time monitoring** endpoints
- ✅ **Simplified UI** with Spanish as default

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Monitor the `/api/status` endpoint for service health
3. Check the service logs for detailed error messages
4. Ensure your audio file meets the requirements

---

**Happy transcribing! 🎤➡️📝**

*Built with ❤️ using Flask, Vosk, and Docker*