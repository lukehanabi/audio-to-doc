# 🚀 Deployment Guide - Audio to Text Service

This guide covers deploying the Audio to Text Conversion Service to Render.com using Docker.

## 📋 Prerequisites

- GitHub repository with the service code
- Render.com account
- Docker installed locally (for testing)

## 🐳 Local Docker Testing

### 1. Build and Test Locally

```bash
# Build the Docker image
docker build -t audio-to-text-service .

# Run the container
docker run -p 5000:5000 audio-to-text-service
```

### 2. Test with Docker Compose

```bash
# Start the service
docker-compose up --build

# The service will be available at http://localhost:5000
```

## 🌐 Deploy to Render.com

### Method 1: Using render.yaml (Recommended)

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Connect to Render**: 
   - Go to [Render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
3. **Configure Service**:
   - Name: `audio-to-text-service`
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`
   - Docker Context: `.`
   - Plan: Choose based on your needs:
     - **Starter**: $7/month, 0.1 CPU, 512MB RAM
     - **Standard**: $25/month, 0.5 CPU, 2GB RAM
     - **Pro**: $85/month, 2 CPU, 8GB RAM
4. **Deploy**: Click "Create Web Service"

### Method 2: Manual Configuration

If you prefer manual setup:

1. **Create Web Service**:
   - Environment: `Docker`
   - Dockerfile Path: `./Dockerfile`
   - Docker Context: `.`

2. **Environment Variables**:
   ```
   FLASK_ENV=production
   MAX_CONTENT_LENGTH=100000000
   PORT=5000
   ```

3. **Advanced Settings**:
   - Health Check Path: `/api/health`
   - Auto-Deploy: `Yes`

## ⚙️ Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FLASK_ENV` | `production` | Flask environment |
| `MAX_CONTENT_LENGTH` | `100000000` | Max file size in bytes (100MB) |
| `PORT` | `5000` | Port for the service |
| `UPLOAD_FOLDER` | `/tmp` | Temporary file storage |
| `SECRET_KEY` | `dev-secret-key` | Flask secret key |

### Render.com Plan Recommendations

| Plan | CPU | RAM | Best For |
|------|-----|-----|----------|
| Starter | 0.1 | 512MB | Testing, small files |
| Standard | 0.5 | 2GB | Production, medium files |
| Pro | 2 | 8GB | High volume, large files |

## 🔧 Customization

### Custom Domain

1. In Render dashboard, go to your service
2. Click "Settings" → "Custom Domains"
3. Add your domain and configure DNS

### SSL Certificate

Render automatically provides SSL certificates for custom domains.

### Scaling

- **Horizontal**: Render handles this automatically
- **Vertical**: Upgrade your plan for more resources

## 📊 Monitoring

### Health Checks

The service includes a health check endpoint:
```
GET /api/health
```

### Logs

Access logs in Render dashboard:
1. Go to your service
2. Click "Logs" tab
3. View real-time logs

### Metrics

Render provides basic metrics:
- CPU usage
- Memory usage
- Response times
- Request counts

## 🚨 Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Dockerfile syntax
   - Verify all dependencies in requirements.txt
   - Ensure FFmpeg is properly installed

2. **Service Won't Start**:
   - Check logs for error messages
   - Verify PORT environment variable
   - Ensure health check endpoint is working

3. **Audio Processing Errors**:
   - Check file size limits
   - Verify supported audio formats
   - Check FFmpeg installation

### Debug Mode

For debugging, temporarily set:
```
FLASK_ENV=development
```

## 🔒 Security Considerations

1. **File Upload Limits**: Configured via `MAX_CONTENT_LENGTH`
2. **Temporary Files**: Automatically cleaned up
3. **CORS**: Configure if needed for cross-origin requests
4. **Rate Limiting**: Consider adding for production use

## 📈 Performance Optimization

### For High Volume

1. **Upgrade Plan**: Use Standard or Pro plan
2. **Caching**: Consider adding Redis for caching
3. **CDN**: Use Render's CDN for static assets
4. **Database**: Add PostgreSQL for storing results

### For Large Files

1. **Increase Limits**: Set higher `MAX_CONTENT_LENGTH`
2. **Streaming**: Consider streaming for very large files
3. **Chunking**: Process audio in chunks

## 🔄 CI/CD

### Automatic Deployments

Render automatically deploys when you push to your main branch.

### Manual Deployments

1. Go to your service dashboard
2. Click "Manual Deploy"
3. Select branch and commit

## 📞 Support

- **Render Documentation**: [https://render.com/docs](https://render.com/docs)
- **Service Logs**: Check Render dashboard
- **Health Check**: Use `/api/health` endpoint

---

**Your audio-to-text service is now ready for production! 🎉**
