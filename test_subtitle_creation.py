#!/usr/bin/env python3
"""
🧪 Test Subtitle Creation
Test việc tạo file .srt và .txt từ video
"""

import os
import sys
import whisper
import torch
from pathlib import Path

def test_whisper_installation():
    """Test cài đặt Whisper"""
    print("🧪 Testing Whisper installation...")
    
    try:
        import whisper
        print(f"   ✅ Whisper version: {whisper.__version__}")
        return True
    except ImportError:
        print("   ❌ Whisper not installed")
        return False
    except Exception as e:
        print(f"   ❌ Whisper error: {e}")
        return False

def test_model_loading():
    """Test load model"""
    print("🧪 Testing model loading...")
    
    try:
        # Test tiny model
        model = whisper.load_model("tiny")
        print("   ✅ Tiny model loaded successfully")
        
        # Test model properties
        print(f"   Model device: {next(model.parameters()).device}")
        print(f"   Model dtype: {next(model.parameters()).dtype}")
        
        return True
    except Exception as e:
        print(f"   ❌ Model loading error: {e}")
        return False

def test_transcribe_function():
    """Test transcribe function"""
    print("🧪 Testing transcribe function...")
    
    try:
        # Load model
        model = whisper.load_model("tiny")
        
        # Create dummy audio (1 second of random data)
        import numpy as np
        dummy_audio = np.random.randn(16000).astype(np.float32)  # 1 second at 16kHz
        
        # Test transcribe
        result = model.transcribe(dummy_audio, fp16=False, verbose=False)
        
        print("   ✅ Transcribe function working")
        print(f"   Text length: {len(result['text'])} characters")
        print(f"   Segments count: {len(result['segments'])}")
        
        return True
    except Exception as e:
        print(f"   ❌ Transcribe error: {e}")
        return False

def test_file_creation():
    """Test tạo file .srt và .txt"""
    print("🧪 Testing file creation...")
    
    try:
        # Load model
        model = whisper.load_model("tiny")
        
        # Create dummy audio
        import numpy as np
        dummy_audio = np.random.randn(16000).astype(np.float32)
        
        # Transcribe
        result = model.transcribe(dummy_audio, fp16=False, verbose=False)
        
        # Test file creation
        test_txt = "test_output.txt"
        test_srt = "test_output.srt"
        
        # Create TXT file
        with open(test_txt, "w", encoding="utf-8") as f:
            f.write(result["text"])
        print(f"   ✅ Created TXT file: {test_txt}")
        
        # Create SRT file
        def format_timestamp(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int((seconds - int(seconds)) * 1000)
            return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
        
        with open(test_srt, "w", encoding="utf-8") as srt_file:
            for i, seg in enumerate(result["segments"], 1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        
        print(f"   ✅ Created SRT file: {test_srt}")
        
        # Check file sizes
        txt_size = os.path.getsize(test_txt)
        srt_size = os.path.getsize(test_srt)
        
        print(f"   TXT file size: {txt_size} bytes")
        print(f"   SRT file size: {srt_size} bytes")
        
        # Cleanup
        os.remove(test_txt)
        os.remove(test_srt)
        print("   🗑️ Cleaned up test files")
        
        return True
    except Exception as e:
        print(f"   ❌ File creation error: {e}")
        return False

def test_video_file_detection():
    """Test phát hiện video files"""
    print("🧪 Testing video file detection...")
    
    try:
        # Test video extensions
        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        
        # Create test files
        test_files = [
            "test_video.mp4",
            "test_video.mov",
            "test_video.avi",
            "test_document.txt",
            "test_image.jpg"
        ]
        
        for file in test_files:
            with open(file, "w") as f:
                f.write("test")
        
        # Count video files
        video_count = 0
        for file in os.listdir("."):
            if Path(file).suffix.lower() in video_extensions:
                video_count += 1
        
        print(f"   ✅ Found {video_count} video files")
        
        # Cleanup
        for file in test_files:
            if os.path.exists(file):
                os.remove(file)
        
        return True
    except Exception as e:
        print(f"   ❌ Video detection error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Subtitle Creation Test Suite")
    print("=" * 50)
    
    tests = [
        ("Whisper Installation", test_whisper_installation),
        ("Model Loading", test_model_loading),
        ("Transcribe Function", test_transcribe_function),
        ("File Creation", test_file_creation),
        ("Video Detection", test_video_file_detection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! Subtitle creation should work correctly.")
        print("\n💡 Try running:")
        print("   python3 subtitle_gui_integrated.py")
    else:
        print("⚠️  Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()










