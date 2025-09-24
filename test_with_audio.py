#!/usr/bin/env python3
"""
Test script for Audio to Text Service with actual audio file testing
"""

import os
import sys
import subprocess
import tempfile

def create_test_audio():
    """Create a simple test audio file using system tools"""
    try:
        # Create a simple WAV file with a tone (1 second, 440Hz)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_file = f.name
        
        # Use sox to create a test audio file (if available)
        try:
            subprocess.run([
                'sox', '-n', temp_file, 
                'synth', '1', 'sine', '440', 'vol', '0.1'
            ], check=True, capture_output=True)
            print(f"✅ Created test audio file: {temp_file}")
            return temp_file
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If sox is not available, create a minimal WAV file
            print("⚠️  Sox not available, creating minimal WAV file...")
            # Create a minimal WAV header (44 bytes) + some data
            wav_data = bytearray([
                # WAV header
                0x52, 0x49, 0x46, 0x46,  # "RIFF"
                0x24, 0x00, 0x00, 0x00,  # File size - 8
                0x57, 0x41, 0x56, 0x45,  # "WAVE"
                0x66, 0x6D, 0x74, 0x20,  # "fmt "
                0x10, 0x00, 0x00, 0x00,  # Format chunk size
                0x01, 0x00,              # Audio format (PCM)
                0x01, 0x00,              # Number of channels
                0x44, 0xAC, 0x00, 0x00,  # Sample rate (44100)
                0x88, 0x58, 0x01, 0x00,  # Byte rate
                0x02, 0x00,              # Block align
                0x10, 0x00,              # Bits per sample
                0x64, 0x61, 0x74, 0x61,  # "data"
                0x00, 0x00, 0x00, 0x00,  # Data size
            ])
            
            with open(temp_file, 'wb') as f:
                f.write(wav_data)
            
            print(f"✅ Created minimal test audio file: {temp_file}")
            return temp_file
            
    except Exception as e:
        print(f"❌ Error creating test audio: {e}")
        return None

def test_audio_conversion(audio_file):
    """Test the audio conversion endpoint"""
    if not audio_file or not os.path.exists(audio_file):
        print("❌ No valid audio file provided")
        return False
    
    try:
        import requests
        
        print(f"🎵 Testing audio conversion with file: {os.path.basename(audio_file)}")
        
        with open(audio_file, 'rb') as f:
            files = {'audio_file': f}
            data = {'language': 'english'}
            
            response = requests.post('http://localhost:5000/api/convert', 
                                   files=files, data=data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Audio conversion successful!")
                print(f"   Text: {result.get('text', '')[:100]}...")
                print(f"   Confidence: {result.get('confidence', 0)}")
                print(f"   Service used: {result.get('service_used', 'unknown')}")
                return True
            else:
                print(f"❌ Audio conversion failed: {result.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except ImportError:
        print("❌ requests library not available. Install with: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Error testing audio conversion: {e}")
        return False

def test_with_curl(audio_file):
    """Test using curl command"""
    if not audio_file or not os.path.exists(audio_file):
        print("❌ No valid audio file provided")
        return False
    
    try:
        print(f"🎵 Testing with curl: {os.path.basename(audio_file)}")
        
        # Use curl to test the endpoint
        cmd = [
            'curl', '-s', '-X', 'POST',
            '-F', f'audio_file=@{audio_file}',
            '-F', 'language=english',
            'http://localhost:5000/api/convert'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Curl test completed")
            print(f"   Response: {result.stdout[:200]}...")
            return True
        else:
            print(f"❌ Curl test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error with curl test: {e}")
        return False

def main():
    print("🎵 Audio to Text Service - Audio File Testing")
    print("=" * 50)
    
    # Check if service is running
    try:
        import requests
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code != 200:
            print("❌ Service is not running or not healthy")
            return False
    except:
        print("❌ Cannot connect to service. Make sure it's running on localhost:5000")
        return False
    
    print("✅ Service is running and healthy")
    
    # Create test audio file
    audio_file = create_test_audio()
    if not audio_file:
        print("❌ Could not create test audio file")
        return False
    
    try:
        # Test with requests (if available)
        success1 = test_audio_conversion(audio_file)
        
        # Test with curl
        success2 = test_with_curl(audio_file)
        
        print("\n" + "=" * 50)
        if success1 or success2:
            print("🎉 Audio conversion testing completed!")
            print("\nTo test with your own audio files:")
            print("1. Use the web interface at http://localhost:5000")
            print("2. Or use curl:")
            print(f"   curl -X POST -F 'audio_file=@your_file.mp3' -F 'language=spanish' http://localhost:5000/api/convert")
        else:
            print("⚠️  Audio conversion tests had issues")
            print("   This might be normal for test audio files")
            print("   Try with a real audio file containing speech")
        
    finally:
        # Clean up test file
        if audio_file and os.path.exists(audio_file):
            os.unlink(audio_file)
            print(f"🧹 Cleaned up test file: {audio_file}")

if __name__ == "__main__":
    main()
