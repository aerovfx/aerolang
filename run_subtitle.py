#!/usr/bin/env python3
"""
🎬 Run Subtitle Generator - Simple Wrapper
Script đơn giản để chạy subtitle generator cho MacBook Pro M2
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Kiểm tra dependencies"""
    print("🔍 Checking dependencies...")
    
    try:
        import whisper
        print("✅ Whisper installed")
    except ImportError:
        print("❌ Whisper not installed")
        print("💡 Run: pip install openai-whisper")
        return False
    
    try:
        import torch
        print("✅ PyTorch installed")
    except ImportError:
        print("❌ PyTorch not installed")
        print("💡 Run: pip install torch torchaudio")
        return False
    
    try:
        import psutil
        print("✅ psutil installed")
    except ImportError:
        print("❌ psutil not installed")
        print("💡 Run: pip install psutil")
        return False
    
    return True

def get_video_folder():
    """Lấy thư mục video từ user"""
    print("\n📁 Video Folder Selection")
    print("=" * 40)
    
    while True:
        folder = input("Enter video folder path (or 'q' to quit): ").strip()
        
        if folder.lower() == 'q':
            print("👋 Goodbye!")
            sys.exit(0)
        
        if not folder:
            print("⚠️ Please enter a folder path")
            continue
        
        if not os.path.isdir(folder):
            print("❌ Folder not found. Please check the path")
            continue
        
        # Kiểm tra có video files không
        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        video_count = 0
        
        for file in os.listdir(folder):
            if Path(file).suffix.lower() in video_extensions:
                video_count += 1
        
        if video_count == 0:
            print("⚠️ No video files found in this folder")
            response = input("Continue anyway? (y/n): ").lower().strip()
            if response != 'y':
                continue
        else:
            print(f"✅ Found {video_count} video files")
        
        return folder

def get_settings():
    """Lấy cài đặt từ user"""
    print("\n⚙️ Settings")
    print("=" * 40)
    
    # Language selection
    print("🌍 Language options:")
    print("   1. Vietnamese (vi)")
    print("   2. English (en)")
    print("   3. Auto detect (auto)")
    
    while True:
        lang_choice = input("Select language (1-3, default: 1): ").strip()
        if not lang_choice:
            lang_choice = "1"
        
        if lang_choice == "1":
            language = "vi"
            break
        elif lang_choice == "2":
            language = "en"
            break
        elif lang_choice == "3":
            language = "auto"
            break
        else:
            print("⚠️ Please select 1, 2, or 3")
    
    # Model selection
    print("\n📦 Model options:")
    print("   1. Tiny (fastest, lowest accuracy)")
    print("   2. Base (fast, medium accuracy)")
    print("   3. Small (balanced)")
    print("   4. Medium (high accuracy, recommended for M2)")
    print("   5. Large (highest accuracy, slowest)")
    
    while True:
        model_choice = input("Select model (1-5, default: 4): ").strip()
        if not model_choice:
            model_choice = "4"
        
        models = {
            "1": "tiny",
            "2": "base", 
            "3": "small",
            "4": "medium",
            "5": "large"
        }
        
        if model_choice in models:
            model = models[model_choice]
            break
        else:
            print("⚠️ Please select 1-5")
    
    # Workers selection
    print("\n🔧 Workers (parallel processing):")
    print("   Recommended: 2 for MacBook Pro M2 16GB")
    
    while True:
        workers_input = input("Number of workers (1-4, default: 2): ").strip()
        if not workers_input:
            workers = 2
            break
        
        try:
            workers = int(workers_input)
            if 1 <= workers <= 4:
                break
            else:
                print("⚠️ Please enter 1-4")
        except ValueError:
            print("⚠️ Please enter a number")
    
    return language, model, workers

def run_subtitle_generator(folder, language, model, workers):
    """Chạy subtitle generator"""
    print(f"\n🚀 Starting subtitle generation...")
    print("=" * 60)
    
    cmd = [
        sys.executable, "subtitle_m2_optimized.py",
        folder,
        "--lang", language,
        "--model", model,
        "--workers", str(workers)
    ]
    
    print(f"Command: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("\n🎉 Subtitle generation completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Subtitle generation failed: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⏹️ Process interrupted by user")
        return False

def show_results(folder):
    """Hiển thị kết quả"""
    print(f"\n📁 Results in folder: {folder}")
    print("=" * 40)
    
    txt_files = []
    srt_files = []
    
    for file in os.listdir(folder):
        if file.endswith("_translated.txt"):
            txt_files.append(file)
        elif file.endswith("_translated.srt"):
            srt_files.append(file)
    
    if txt_files:
        print("📄 Text files (.txt):")
        for file in sorted(txt_files):
            file_path = os.path.join(folder, file)
            size = os.path.getsize(file_path)
            print(f"   📄 {file} ({size} bytes)")
    
    if srt_files:
        print("\n🎬 Subtitle files (.srt):")
        for file in sorted(srt_files):
            file_path = os.path.join(folder, file)
            size = os.path.getsize(file_path)
            print(f"   🎬 {file} ({size} bytes)")
    
    if not txt_files and not srt_files:
        print("❌ No output files found")

def main():
    """Main function"""
    print("🎬 Video Subtitle Generator - MacBook Pro M2")
    print("=" * 50)
    print("Tạo phụ đề .srt và nội dung .txt từ video")
    print("Tối ưu cho MacBook Pro M2 với 16GB RAM")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies")
        sys.exit(1)
    
    # Get video folder
    folder = get_video_folder()
    
    # Get settings
    language, model, workers = get_settings()
    
    # Show summary
    print(f"\n📋 Summary")
    print("=" * 40)
    print(f"📁 Folder: {folder}")
    print(f"🌍 Language: {language}")
    print(f"📦 Model: {model}")
    print(f"🔧 Workers: {workers}")
    
    # Confirm
    response = input("\n🚀 Start processing? (y/n): ").lower().strip()
    if response != 'y':
        print("👋 Cancelled")
        sys.exit(0)
    
    # Run processing
    success = run_subtitle_generator(folder, language, model, workers)
    
    if success:
        show_results(folder)
        print(f"\n🎉 All done! Check the output files in: {folder}")
    else:
        print(f"\n❌ Processing failed. Check the error messages above.")

if __name__ == "__main__":
    main()
