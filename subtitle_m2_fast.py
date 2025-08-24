#!/usr/bin/env python3
"""
🎬 Fast Video Subtitle Generator - MacBook Pro M2
Phiên bản nhanh với progress tracking tốt hơn
"""

import os
import sys
import argparse
import whisper
import torch
import gc
import time
import psutil
from pathlib import Path
from tqdm import tqdm

class FastM2SubtitleGenerator:
    def __init__(self, model_size="tiny", max_workers=1):
        """
        Khởi tạo subtitle generator nhanh cho M2
        
        Args:
            model_size: Kích thước model (tiny, base, small, medium, large)
            max_workers: Số luồng xử lý (khuyến nghị 1 cho nhanh)
        """
        self.model_size = model_size
        self.max_workers = max_workers
        self.model = None
        self.device = None
        
        # Setup device
        self._setup_device()
        
        print(f"🎬 Fast M2 Subtitle Generator - Model: {model_size}")
        print(f"💻 Device: {self.device}")
        print(f"🔧 Workers: {self.max_workers}")
    
    def _setup_device(self):
        """Setup device tối ưu cho M2"""
        try:
            if torch.backends.mps.is_available():
                self.device = "mps"
                print("✅ Sử dụng MPS (Apple Silicon GPU)")
                
                # Tối ưu MPS settings
                try:
                    if hasattr(torch.backends.mps, 'empty_cache'):
                        torch.backends.mps.empty_cache()
                except Exception as e:
                    print(f"⚠️ MPS cache cleanup warning: {e}")
                
            elif torch.cuda.is_available():
                self.device = "cuda"
                print("✅ Sử dụng CUDA")
                
            else:
                self.device = "cpu"
                print("✅ Sử dụng CPU")
                
        except Exception as e:
            print(f"⚠️ Device setup error: {e}")
            self.device = "cpu"
            print("🔄 Fallback to CPU")
    
    def load_model(self):
        """Load Whisper model với tối ưu M2"""
        print(f"📦 Loading model {self.model_size}...")
        
        try:
            # Load model với device tối ưu
            self.model = whisper.load_model(self.model_size, device=self.device)
            
            # Tối ưu model cho M2
            if self.device == "mps":
                # Sử dụng float32 cho MPS
                self.model = self.model.float()
                
                # Clear cache
                try:
                    if hasattr(torch.backends.mps, 'empty_cache'):
                        torch.backends.mps.empty_cache()
                except Exception as e:
                    print(f"⚠️ MPS cache cleanup warning: {e}")
            
            print(f"✅ Model {self.model_size} loaded successfully")
            return True
            
        except Exception as e:
            print(f"❌ Model loading error: {e}")
            
            # Fallback to CPU nếu MPS lỗi
            if self.device == "mps":
                print("🔄 Retrying with CPU...")
                self.device = "cpu"
                self.model = whisper.load_model(self.model_size, device="cpu")
                print("✅ Model loaded on CPU")
                return True
            
            return False
    
    def format_timestamp(self, seconds):
        """Format timestamp cho SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
    
    def transcribe_video(self, video_path, output_txt_path, output_srt_path, target_lang="vi"):
        """
        Transcribe video và tạo file .srt và .txt
        
        Args:
            video_path: Đường dẫn video
            output_txt_path: Đường dẫn file .txt output
            output_srt_path: Đường dẫn file .srt output
            target_lang: Ngôn ngữ đích (vi, en, auto)
        """
        try:
            video_name = Path(video_path).name
            
            # Transcribe với tối ưu M2
            start_time = time.time()
            
            try:
                if target_lang == "en":
                    result = self.model.transcribe(
                        video_path,
                        task="translate",
                        fp16=False,  # Sử dụng float32 cho MPS
                        verbose=False
                    )
                else:
                    result = self.model.transcribe(
                        video_path,
                        language=target_lang,
                        fp16=False,
                        verbose=False
                    )
                    
            except Exception as e:
                # Fallback mechanism cho MPS errors
                if "SparseMPS" in str(e) or "MPS" in str(e):
                    print(f"⚠️ MPS error: {e}")
                    print("🔄 Retrying with CPU...")
                    
                    # Switch to CPU
                    self.device = "cpu"
                    self.model = self.model.to("cpu")
                    
                    if target_lang == "en":
                        result = self.model.transcribe(
                            video_path,
                            task="translate",
                            fp16=False,
                            verbose=False
                        )
                    else:
                        result = self.model.transcribe(
                            video_path,
                            language=target_lang,
                            fp16=False,
                            verbose=False
                        )
                else:
                    raise e
            
            transcribe_time = time.time() - start_time
            
            # Tạo file TXT
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            # Tạo file SRT
            if "segments" in result:
                with open(output_srt_path, "w", encoding="utf-8") as srt_file:
                    for i, seg in enumerate(result["segments"], 1):
                        start = self.format_timestamp(seg["start"])
                        end = self.format_timestamp(seg["end"])
                        text = seg["text"].strip()
                        srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            
            # Memory cleanup
            self._cleanup_memory()
            
            return True, transcribe_time
            
        except Exception as e:
            return False, 0
    
    def _cleanup_memory(self):
        """Cleanup memory tối ưu cho M2"""
        try:
            if self.device == "mps":
                try:
                    if hasattr(torch.backends.mps, 'empty_cache'):
                        torch.backends.mps.empty_cache()
                except Exception as e:
                    pass
            elif self.device == "cuda":
                torch.cuda.empty_cache()
            
            gc.collect()
            
        except Exception as e:
            pass
    
    def process_folder(self, folder_path, target_lang="vi"):
        """
        Xử lý tất cả video trong thư mục với progress bar
        
        Args:
            folder_path: Đường dẫn thư mục chứa video
            target_lang: Ngôn ngữ đích
        """
        print(f"📁 Processing folder: {folder_path}")
        
        # Tìm video files
        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        video_files = []
        
        for file in os.listdir(folder_path):
            if Path(file).suffix.lower() in video_extensions:
                video_files.append(file)
        
        if not video_files:
            print("❌ No video files found")
            return False
        
        print(f"📹 Found {len(video_files)} video files")
        
        # Load model nếu chưa load
        if not self.model:
            if not self.load_model():
                return False
        
        # Xử lý từng video với progress bar
        success_count = 0
        total_time = 0
        
        with tqdm(total=len(video_files), desc="🎬 Processing videos", unit="video") as pbar:
            for filename in video_files:
                video_path = os.path.join(folder_path, filename)
                base = os.path.splitext(video_path)[0]
                txt_path = base + "_translated.txt"
                srt_path = base + "_translated.srt"
                
                # Update progress bar description
                pbar.set_description(f"🎬 Processing {filename}")
                
                success, transcribe_time = self.transcribe_video(video_path, txt_path, srt_path, target_lang)
                
                if success:
                    success_count += 1
                    total_time += transcribe_time
                    pbar.set_postfix({
                        'Success': f"{success_count}/{len(video_files)}",
                        'Time': f"{transcribe_time:.1f}s"
                    })
                else:
                    pbar.set_postfix({
                        'Error': filename,
                        'Success': f"{success_count}/{len(video_files)}"
                    })
                
                pbar.update(1)
        
        print(f"\n🎉 Processing completed!")
        print(f"✅ Success: {success_count}/{len(video_files)}")
        print(f"⏱️ Total time: {total_time:.2f} seconds")
        print(f"📊 Average time per video: {total_time/len(video_files):.2f} seconds")
        
        return success_count > 0

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="🎬 Fast M2 Subtitle Generator")
    
    parser.add_argument("folder", help="Thư mục chứa video files")
    parser.add_argument("--lang", default="vi", choices=["vi", "en", "auto"], 
                       help="Ngôn ngữ đích (default: vi)")
    parser.add_argument("--model", default="tiny", 
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Kích thước model (default: tiny for speed)")
    parser.add_argument("--workers", type=int, default=1,
                       help="Số luồng xử lý (default: 1 for speed)")
    parser.add_argument("--verbose", action="store_true",
                       help="Hiển thị thông tin chi tiết")
    
    args = parser.parse_args()
    
    # Validate folder
    if not os.path.isdir(args.folder):
        print(f"❌ Folder not found: {args.folder}")
        sys.exit(1)
    
    print("🎬 Fast Video Subtitle Generator - MacBook Pro M2")
    print("=" * 60)
    print(f"📁 Folder: {args.folder}")
    print(f"🌍 Language: {args.lang}")
    print(f"📦 Model: {args.model}")
    print(f"🔧 Workers: {args.workers}")
    print("=" * 60)
    
    # Create generator
    generator = FastM2SubtitleGenerator(
        model_size=args.model,
        max_workers=args.workers
    )
    
    # Process folder
    start_time = time.time()
    success = generator.process_folder(args.folder, args.lang)
    total_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    if success:
        print(f"🎉 Processing completed successfully!")
        print(f"⏱️ Total time: {total_time:.2f} seconds")
    else:
        print("❌ Processing failed")
        sys.exit(1)

if __name__ == "__main__":
    main()


