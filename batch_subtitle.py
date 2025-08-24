#!/usr/bin/env python3
"""
🎬 Batch Subtitle Generator - MacBook Pro M2
Xử lý nhiều thư mục video cùng lúc
Tối ưu cho MacBook Pro M2 với 16GB RAM
"""

import os
import sys
import argparse
import time
from pathlib import Path
from subtitle_m2_optimized import M2SubtitleGenerator

def find_video_folders(root_path, max_depth=3):
    """
    Tìm tất cả thư mục chứa video files
    
    Args:
        root_path: Thư mục gốc để tìm kiếm
        max_depth: Độ sâu tối đa để tìm kiếm
    """
    video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
    video_folders = []
    
    for root, dirs, files in os.walk(root_path):
        # Kiểm tra độ sâu
        depth = root.replace(root_path, '').count(os.sep)
        if depth > max_depth:
            continue
        
        # Kiểm tra có video files không
        has_videos = any(
            Path(file).suffix.lower() in video_extensions 
            for file in files
        )
        
        if has_videos:
            video_count = sum(
                1 for file in files 
                if Path(file).suffix.lower() in video_extensions
            )
            video_folders.append((root, video_count))
    
    return video_folders

def process_batch(folders, language="vi", model="medium", workers=2):
    """
    Xử lý batch các thư mục
    
    Args:
        folders: List of (folder_path, video_count) tuples
        language: Ngôn ngữ đích
        model: Kích thước model
        workers: Số workers
    """
    print(f"🎬 Batch Processing - {len(folders)} folders")
    print("=" * 60)
    
    # Tạo generator
    generator = M2SubtitleGenerator(model_size=model, max_workers=workers)
    
    # Load model một lần
    if not generator.load_model():
        print("❌ Failed to load model")
        return False
    
    total_start_time = time.time()
    success_count = 0
    
    for i, (folder_path, video_count) in enumerate(folders, 1):
        print(f"\n📁 Processing folder {i}/{len(folders)}: {folder_path}")
        print(f"📹 Videos: {video_count}")
        print("-" * 50)
        
        try:
            success = generator.process_folder(folder_path, language)
            if success:
                success_count += 1
                print(f"✅ Folder {i} completed successfully")
            else:
                print(f"❌ Folder {i} failed")
        except Exception as e:
            print(f"❌ Error processing folder {i}: {e}")
    
    total_time = time.time() - total_start_time
    
    print("\n" + "=" * 60)
    print(f"🎉 Batch processing completed!")
    print(f"✅ Success: {success_count}/{len(folders)} folders")
    print(f"⏱️ Total time: {total_time:.2f} seconds")
    
    return success_count > 0

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="🎬 Batch Subtitle Generator")
    
    parser.add_argument("root_path", help="Thư mục gốc để tìm kiếm video")
    parser.add_argument("--lang", default="vi", choices=["vi", "en", "auto"], 
                       help="Ngôn ngữ đích (default: vi)")
    parser.add_argument("--model", default="medium", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Kích thước model (default: medium)")
    parser.add_argument("--workers", type=int, default=2,
                       help="Số luồng xử lý (default: 2)")
    parser.add_argument("--max-depth", type=int, default=3,
                       help="Độ sâu tối đa tìm kiếm (default: 3)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Chỉ hiển thị thư mục sẽ xử lý, không chạy thực")
    
    args = parser.parse_args()
    
    # Validate root path
    if not os.path.isdir(args.root_path):
        print(f"❌ Root path not found: {args.root_path}")
        sys.exit(1)
    
    print("🎬 Batch Subtitle Generator - MacBook Pro M2")
    print("=" * 60)
    print(f"📁 Root path: {args.root_path}")
    print(f"🌍 Language: {args.lang}")
    print(f"📦 Model: {args.model}")
    print(f"🔧 Workers: {args.workers}")
    print(f"🔍 Max depth: {args.max_depth}")
    print("=" * 60)
    
    # Tìm video folders
    print("🔍 Searching for video folders...")
    video_folders = find_video_folders(args.root_path, args.max_depth)
    
    if not video_folders:
        print("❌ No video folders found")
        sys.exit(1)
    
    print(f"📁 Found {len(video_folders)} video folders:")
    for i, (folder, count) in enumerate(video_folders, 1):
        print(f"   {i:2d}. {folder} ({count} videos)")
    
    if args.dry_run:
        print("\n🔍 Dry run completed. No processing done.")
        return
    
    # Confirm processing
    total_videos = sum(count for _, count in video_folders)
    print(f"\n📊 Summary:")
    print(f"   Folders: {len(video_folders)}")
    print(f"   Total videos: {total_videos}")
    
    response = input("\n🚀 Start batch processing? (y/n): ").lower().strip()
    if response != 'y':
        print("👋 Cancelled")
        sys.exit(0)
    
    # Process batch
    success = process_batch(video_folders, args.lang, args.model, args.workers)
    
    if success:
        print(f"\n🎉 Batch processing completed successfully!")
    else:
        print(f"\n❌ Batch processing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()










