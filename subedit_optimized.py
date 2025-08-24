#!/usr/bin/env python3
"""
🎬 Video Subtitle Generator - Optimized for MacBook Pro M2
Tối ưu cho Apple Silicon M2 với 16GB RAM
"""

import os
import sys
import whisper
import torch
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import gc
from typing import List, Tuple, Optional
import argparse
from tqdm import tqdm
import psutil
import tkinter as tk
from tkinter import filedialog, messagebox

class VideoProcessor:
    def __init__(self, model_size: str = "base", max_workers: int = 2):
        """
        Khởi tạo processor với tối ưu cho M2
        
        Args:
            model_size: Kích thước model (tiny, base, small, medium, large)
            max_workers: Số luồng tối đa (khuyến nghị 2 cho M2)
        """
        self.max_workers = max_workers
        self.device = self._setup_device()
        self.model = self._load_model(model_size)
        self.memory_monitor = MemoryMonitor()
        
    def _setup_device(self) -> str:
        """Thiết lập device tối ưu cho Apple Silicon"""
        if torch.backends.mps.is_available():
            device = "mps"
            # Tối ưu MPS settings - kiểm tra tương thích
            try:
                if hasattr(torch.backends.mps, 'empty_cache'):
                    torch.backends.mps.empty_cache()
                else:
                    print("⚠️  MPS empty_cache không khả dụng, bỏ qua")
            except Exception as e:
                print(f"⚠️  Lỗi MPS cache cleanup: {e}")
        elif torch.cuda.is_available():
            device = "cuda"
        else:
            device = "cpu"
            
        print(f"💻 Sử dụng device: {device}")
        return device
    
    def _load_model(self, model_size: str):
        """Load model với tối ưu bộ nhớ"""
        print(f"📦 Đang load model {model_size}...")
        
        # Tối ưu cho M2 với fallback mechanism
        if self.device == "mps":
            try:
                # Thử load với MPS
                model = whisper.load_model(model_size, device=self.device)
                print(f"✅ Model {model_size} loaded với MPS")
                
                # Tối ưu memory usage
                if hasattr(model, 'encoder'):
                    model.encoder = model.encoder.to(dtype=torch.float32)
                    
            except Exception as e:
                print(f"⚠️  MPS load failed: {e}")
                print("🔄 Fallback to CPU...")
                self.device = "cpu"
                model = whisper.load_model(model_size, device="cpu")
                print(f"✅ Model {model_size} loaded với CPU fallback")
        else:
            model = whisper.load_model(model_size, device=self.device)
            
        print(f"✅ Model {model_size} đã sẵn sàng trên {self.device}")
        return model
    
    def format_timestamp(self, seconds: float) -> str:
        """Format timestamp cho SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
    
    def transcribe_video(self, video_path: str, output_txt_path: str, 
                        output_srt_path: str, target_lang: str = "vi") -> bool:
        """
        Transcribe video với tối ưu bộ nhớ
        """
        try:
            print(f"🎬 Đang xử lý: {Path(video_path).name}")
            
            # Kiểm tra bộ nhớ trước khi xử lý
            self.memory_monitor.check_memory()
            
            # Transcribe với tối ưu cho M2 và fallback mechanism
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
                if "SparseMPS" in str(e) or "MPS" in str(e):
                    print(f"⚠️  MPS error: {e}")
                    print("🔄 Retrying với CPU...")
                    
                    # Fallback to CPU
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
            
            # Lưu file TXT
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            
            # Lưu file SRT
            if "segments" in result:
                with open(output_srt_path, "w", encoding="utf-8") as srt_file:
                    for i, seg in enumerate(result["segments"], 1):
                        start = self.format_timestamp(seg["start"])
                        end = self.format_timestamp(seg["end"])
                        text = seg["text"].strip()
                        srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")
            
            # Cleanup memory
            if self.device == "mps":
                try:
                    if hasattr(torch.backends.mps, 'empty_cache'):
                        torch.backends.mps.empty_cache()
                except Exception as e:
                    print(f"⚠️  Lỗi MPS cache cleanup: {e}")
            elif self.device == "cuda":
                torch.cuda.empty_cache()
            
            gc.collect()
            
            print(f"✅ Hoàn thành: {Path(video_path).name}")
            return True
            
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {Path(video_path).name}: {str(e)}")
            return False
    
    def process_video_batch(self, video_files: List[str], folder_path: str, 
                           target_lang: str = "vi") -> None:
        """Xử lý batch video với đa luồng"""
        total_files = len(video_files)
        
        print(f"🚀 Bắt đầu xử lý {total_files} video với {self.max_workers} luồng")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Tạo futures
            futures = []
            for filename in video_files:
                video_path = os.path.join(folder_path, filename)
                base = os.path.splitext(video_path)[0]
                txt_path = base + "_translated.txt"
                srt_path = base + "_translated.srt"
                
                future = executor.submit(
                    self.transcribe_video, 
                    video_path, txt_path, srt_path, target_lang
                )
                futures.append(future)
            
            # Theo dõi tiến độ
            completed = 0
            failed = 0
            
            with tqdm(total=total_files, desc="🎬 Xử lý video") as pbar:
                for future in as_completed(futures):
                    try:
                        success = future.result()
                        if success:
                            completed += 1
                        else:
                            failed += 1
                    except Exception as e:
                        print(f"❌ Lỗi: {str(e)}")
                        failed += 1
                    
                    pbar.update(1)
                    pbar.set_postfix({
                        'Completed': completed,
                        'Failed': failed,
                        'Memory': f"{self.memory_monitor.get_memory_usage():.1f}%"
                    })
        
        print(f"\n📊 Kết quả: {completed} thành công, {failed} thất bại")
    
    def process_folder(self, folder_path: str, target_lang: str = "vi") -> None:
        """Xử lý toàn bộ thư mục"""
        folder = Path(folder_path)
        if not folder.exists():
            print("❌ Thư mục không tồn tại")
            return
        
        # Tìm video files
        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        video_files = [
            f.name for f in folder.iterdir()
            if f.is_file() and f.suffix.lower() in video_extensions
        ]
        
        if not video_files:
            print("❗ Không tìm thấy video hợp lệ trong thư mục")
            return
        
        print(f"📁 Tìm thấy {len(video_files)} video files")
        
        # Xử lý batch
        self.process_video_batch(video_files, folder_path, target_lang)


class MemoryMonitor:
    """Monitor bộ nhớ hệ thống"""
    
    def __init__(self):
        self.warning_threshold = 80  # 80% RAM usage
        self.critical_threshold = 90  # 90% RAM usage
    
    def get_memory_usage(self) -> float:
        """Lấy tỷ lệ sử dụng RAM"""
        return psutil.virtual_memory().percent
    
    def check_memory(self):
        """Kiểm tra và cảnh báo bộ nhớ"""
        usage = self.get_memory_usage()
        if usage > self.critical_threshold:
            print(f"⚠️  CẢNH BÁO: RAM usage {usage:.1f}% - Quá cao!")
            gc.collect()
            time.sleep(1)
        elif usage > self.warning_threshold:
            print(f"⚠️  RAM usage: {usage:.1f}%")


def get_optimal_model_size(ram_gb: int = 16) -> str:
    """Chọn model size phù hợp với RAM"""
    if ram_gb >= 32:
        return "large"
    elif ram_gb >= 16:
        return "medium"  # Tối ưu cho M2 16GB
    elif ram_gb >= 8:
        return "small"
    else:
        return "base"


def select_folder_gui():
    """Chọn thư mục bằng GUI dialog"""
    # Tạo root window ẩn
    root = tk.Tk()
    root.withdraw()  # Ẩn window chính
    
    # Hiển thị dialog chọn thư mục
    folder_path = filedialog.askdirectory(
        title="🎬 Chọn thư mục chứa video",
        initialdir=os.path.expanduser("~/Desktop")  # Bắt đầu từ Desktop
    )
    
    root.destroy()  # Đóng window
    return folder_path

def main():
    parser = argparse.ArgumentParser(description="🎬 Video Subtitle Generator - M2 Optimized")
    parser.add_argument("folder", nargs='?', help="Đường dẫn thư mục chứa video (tùy chọn)")
    parser.add_argument("--lang", "-l", default="vi", help="Ngôn ngữ đầu ra (mặc định: vi)")
    parser.add_argument("--model", "-m", default="auto", 
                       choices=["tiny", "base", "small", "medium", "large", "auto"],
                       help="Kích thước model (mặc định: auto)")
    parser.add_argument("--workers", "-w", type=int, default=2,
                       help="Số luồng tối đa (mặc định: 2)")
    parser.add_argument("--gui", "-g", action="store_true", 
                       help="Sử dụng GUI để chọn thư mục")
    
    args = parser.parse_args()
    
    # Xác định thư mục
    folder_path = args.folder
    
    # Nếu không có thư mục được chỉ định hoặc có flag --gui
    if not folder_path or args.gui:
        print("🎬 Video Subtitle Generator - MacBook Pro M2 Optimized")
        print("=" * 50)
        
        if not folder_path:
            print("📁 Chưa chọn thư mục. Mở dialog chọn thư mục...")
        
        # Hiển thị dialog chọn thư mục
        folder_path = select_folder_gui()
        
        if not folder_path:
            print("❌ Không có thư mục nào được chọn. Thoát chương trình.")
            return
        
        print(f"✅ Đã chọn thư mục: {folder_path}")
    
    # Kiểm tra thư mục tồn tại
    if not os.path.isdir(folder_path):
        print(f"❌ Thư mục không tồn tại: {folder_path}")
        return
    
    # Chọn model size
    if args.model == "auto":
        model_size = get_optimal_model_size()
        print(f"🤖 Tự động chọn model: {model_size}")
    else:
        model_size = args.model
    
    # Khởi tạo processor
    processor = VideoProcessor(model_size=model_size, max_workers=args.workers)
    
    # Xử lý thư mục
    processor.process_folder(folder_path, args.lang)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  Đã dừng bởi người dùng")
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")
        sys.exit(1)
