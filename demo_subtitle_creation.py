#!/usr/bin/env python3
"""
🎬 Demo Subtitle Creation
Demo tạo file .srt và .txt từ video thực tế
"""

import os
import sys
import whisper
import torch
from pathlib import Path
import time

def create_sample_video():
    """Tạo video sample để test"""
    print("🎬 Creating sample video for testing...")
    
    try:
        # Sử dụng ffmpeg để tạo video test
        import subprocess
        
        # Tạo audio test với ffmpeg
        cmd = [
            "ffmpeg", "-f", "lavfi", "-i", "sine=frequency=1000:duration=5", 
            "-f", "lavfi", "-i", "testsrc=duration=5:size=320x240:rate=1", 
            "-c:v", "libx264", "-c:a", "aac", "-shortest", "sample_video.mp4", "-y"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample video created: sample_video.mp4")
            return True
        else:
            print("⚠️ Could not create sample video with ffmpeg")
            print("Creating dummy video file instead...")
            
            # Tạo file dummy
            with open("sample_video.mp4", "wb") as f:
                f.write(b"dummy video content")
            return True
            
    except Exception as e:
        print(f"⚠️ Error creating sample video: {e}")
        print("Creating dummy video file instead...")
        
        # Tạo file dummy
        with open("sample_video.mp4", "wb") as f:
            f.write(b"dummy video content")
        return True

def demo_subtitle_creation():
    """Demo tạo subtitle"""
    print("🎬 Demo Subtitle Creation")
    print("=" * 50)
    
    # Tạo video sample
    if not create_sample_video():
        print("❌ Could not create sample video")
        return False
    
    try:
        print("📦 Loading Whisper model...")
        
        # Load model
        model = whisper.load_model("tiny")  # Sử dụng tiny để test nhanh
        
        # Setup device
        if torch.backends.mps.is_available():
            device = "mps"
            print("💻 Using MPS (Apple Silicon)")
        elif torch.cuda.is_available():
            device = "cuda"
            print("💻 Using CUDA")
        else:
            device = "cpu"
            print("💻 Using CPU")
        
        print(f"✅ Model loaded on {device}")
        
        # Test với video sample
        video_path = "sample_video.mp4"
        
        if not os.path.exists(video_path):
            print("❌ Sample video not found")
            return False
        
        print(f"🎬 Processing video: {video_path}")
        start_time = time.time()
        
        # Transcribe
        result = model.transcribe(
            video_path,
            language="vi",  # Vietnamese
            fp16=False,
            verbose=False
        )
        
        end_time = time.time()
        print(f"⏱️ Processing time: {end_time - start_time:.2f} seconds")
        
        # Tạo file TXT
        txt_path = "sample_video_translated.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(result["text"])
        
        print(f"📄 Created TXT file: {txt_path}")
        print(f"   Text content: {result['text'][:100]}...")
        
        # Tạo file SRT
        srt_path = "sample_video_translated.srt"
        
        def format_timestamp(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int((seconds - int(seconds)) * 1000)
            return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
        
        with open(srt_path, "w", encoding="utf-8") as srt_file:
            for i, seg in enumerate(result["segments"], 1):
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                text = seg["text"].strip()
                srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
        
        print(f"🎬 Created SRT file: {srt_path}")
        print(f"   Segments count: {len(result['segments'])}")
        
        # Hiển thị nội dung SRT
        print("\n📝 SRT Content preview:")
        with open(srt_path, "r", encoding="utf-8") as f:
            content = f.read()
            lines = content.split('\n')
            for i, line in enumerate(lines[:10]):  # Hiển thị 10 dòng đầu
                print(f"   {i+1:2d}: {line}")
            if len(lines) > 10:
                print("   ...")
        
        # File sizes
        txt_size = os.path.getsize(txt_path)
        srt_size = os.path.getsize(srt_path)
        
        print(f"\n📊 File sizes:")
        print(f"   TXT: {txt_size} bytes")
        print(f"   SRT: {srt_size} bytes")
        
        print("\n✅ Demo completed successfully!")
        print(f"📁 Files created in current directory:")
        print(f"   - {txt_path}")
        print(f"   - {srt_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo error: {e}")
        return False

def cleanup_files():
    """Dọn dẹp files"""
    files_to_clean = [
        "sample_video.mp4",
        "sample_video_translated.txt",
        "sample_video_translated.srt"
    ]
    
    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Removed: {file}")

def main():
    """Main function"""
    print("🎬 Subtitle Creation Demo")
    print("=" * 50)
    
    try:
        # Run demo
        success = demo_subtitle_creation()
        
        if success:
            print("\n🎉 Demo successful!")
            print("\n💡 Next steps:")
            print("   1. Try with your own video files")
            print("   2. Run: python3 subtitle_gui_integrated.py")
            print("   3. Use the GUI to process multiple videos")
            
            # Ask if user wants to keep files
            response = input("\n❓ Keep demo files? (y/n): ").lower().strip()
            if response != 'y':
                cleanup_files()
                print("🗑️ Demo files cleaned up")
        else:
            print("\n❌ Demo failed")
            
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
        cleanup_files()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        cleanup_files()

if __name__ == "__main__":
    main()










