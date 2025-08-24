#!/usr/bin/env python3
"""
🎬 Video Subtitle Generator - MacBook Pro M2 Optimized
Tạo phụ đề .srt và nội dung .txt từ video - Không cần GUI
Hỗ trợ quét đệ quy tất cả thư mục con
Bỏ qua video đã có phụ đề
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


class M2SubtitleGenerator:
    def __init__(self, model_size="medium", max_workers=2):
        """
        Khởi tạo subtitle generator tối ưu cho M2
        
        Args:
            model_size: Kích thước model (tiny, base, small, medium, large)
            max_workers: Số luồng xử lý (khuyến nghị 2 cho M2 16GB)
        """
        self.model_size = model_size
        self.max_workers = max_workers
        self.model = None
        self.device = None

        # Memory monitor
        self.memory_monitor = MemoryMonitor()

        # Setup device
        self._setup_device()

        print(f"🎬 M2 Subtitle Generator - Model: {model_size}")
        print(f"💻 Device: {self.device}")
        print(f"🔧 Workers: {self.max_workers}")

    def _setup_device(self):
        """Setup device tối ưu cho M2"""
        try:
            if torch.backends.mps.is_available():
                self.device = "mps"
                print("✅ Sử dụng MPS (Apple Silicon GPU)")

                # Tối ưu MPS settings
                torch.backends.mps.empty_cache()

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
            self.model = whisper.load_model(self.model_size, device=self.device)

            # Tối ưu model cho M2
            if self.device == "mps":
                self.model = self.model.float()
                try:
                    if hasattr(torch.backends.mps, 'empty_cache'):
                        torch.backends.mps.empty_cache()
                except Exception as e:
                    print(f"⚠️ MPS cache cleanup warning: {e}")

            print(f"✅ Model {self.model_size} loaded successfully")
            return True

        except Exception as e:
            print(f"❌ Model loading error: {e}")

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
        """
        try:
            video_name = Path(video_path).name
            print(f"🎬 Processing: {video_name}")

            self.memory_monitor.check_memory()
            start_time = time.time()

            try:
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

            except Exception as e:
                if "SparseMPS" in str(e) or "MPS" in str(e):
                    print(f"⚠️ MPS error: {e}")
                    print("🔄 Retrying with CPU...")
                    self.device = "cpu"
                    self.model = self.model.to("cpu")
                    if target_lang == "en":
                        result = self.model.transcribe(video_path, task="translate", fp16=False, verbose=False)
                    else:
                        result = self.model.transcribe(video_path, language=target_lang, fp16=False, verbose=False)
                else:
                    raise e

            transcribe_time = time.time() - start_time
            print(f"⏱️ Transcribe time: {transcribe_time:.2f}s")

            # TXT
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(result["text"])
            print(f"📄 Saved TXT: {Path(output_txt_path).name}")

            # SRT
            if "segments" in result:
                with open(output_srt_path, "w", encoding="utf-8") as srt_file:
                    for i, seg in enumerate(result["segments"], 1):
                        start = self.format_timestamp(seg["start"])
                        end = self.format_timestamp(seg["end"])
                        text = seg["text"].strip()
                        srt_file.write(f"{i}\n{start} --> {end}\n{text}\n\n")

                print(f"🎬 Saved SRT: {Path(output_srt_path).name}")
                print(f"   Segments: {len(result['segments'])}")

            self._cleanup_memory()
            total_time = time.time() - start_time
            print(f"✅ Completed: {video_name} ({total_time:.2f}s)")

            return True

        except Exception as e:
            print(f"❌ Error processing {Path(video_path).name}: {str(e)}")
            return False

    def _cleanup_memory(self):
        """Cleanup memory"""
        try:
            if self.device == "mps":
                try:
                    if hasattr(torch.backends.mps, 'empty_cache'):
                        torch.backends.mps.empty_cache()
                except Exception as e:
                    print(f"⚠️ MPS cache cleanup warning: {e}")
            elif self.device == "cuda":
                torch.cuda.empty_cache()

            gc.collect()

        except Exception as e:
            print(f"⚠️ Memory cleanup warning: {e}")

    def process_folder(self, folder_path, target_lang="vi"):
        """
        Xử lý tất cả video trong thư mục (bao gồm cả thư mục con)
        Bỏ qua video đã có phụ đề
        """
        print(f"📁 Processing folder (recursive): {folder_path}")

        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        video_files = []

        for root, _, files in os.walk(folder_path):
            for file in files:
                if Path(file).suffix.lower() in video_extensions:
                    video_files.append(os.path.join(root, file))

        if not video_files:
            print("❌ No video files found (including subfolders)")
            return False

        print(f"📹 Found {len(video_files)} video files (including subfolders)")

        if not self.model:
            if not self.load_model():
                return False

        success_count = 0

        for i, video_path in enumerate(video_files, 1):
            filename = Path(video_path).name
            base = os.path.splitext(video_path)[0]
            txt_path = base + "_translated.txt"
            srt_path = base + "_translated.srt"

            # ⛔ Skip nếu đã có phụ đề
            if os.path.exists(txt_path) or os.path.exists(srt_path):
                print(f"⏩ Skipping {filename} (already has subtitles)")
                continue

            print(f"\n🎬 Processing {i}/{len(video_files)}: {filename}")
            success = self.transcribe_video(video_path, txt_path, srt_path, target_lang)
            if success:
                success_count += 1

            progress = (i / len(video_files)) * 100
            print(f"📊 Progress: {progress:.1f}% ({i}/{len(video_files)})")

        print(f"\n🎉 Processing completed!")
        print(f"✅ Success: {success_count}/{len(video_files)}")

        return success_count > 0


class MemoryMonitor:
    """Monitor memory usage cho M2"""

    def __init__(self):
        self.process = psutil.Process()

    def check_memory(self):
        try:
            memory_info = self.process.memory_info()
            memory_percent = self.process.memory_percent()
            print(f"💾 Memory: {memory_info.rss / 1024 / 1024:.1f}MB ({memory_percent:.1f}%)")
            if memory_percent > 80:
                print("⚠️ High memory usage detected")
        except Exception as e:
            print(f"⚠️ Memory check error: {e}")


def main():
    parser = argparse.ArgumentParser(description="🎬 M2 Optimized Subtitle Generator")

    parser.add_argument("folder", help="Thư mục chứa video files (sẽ duyệt đệ quy)")
    parser.add_argument("--lang", default="vi", choices=["vi", "en", "auto"],
                       help="Ngôn ngữ đích (default: vi)")
    parser.add_argument("--model", default="medium",
                       choices=["tiny", "base", "small", "medium", "large"],
                       help="Kích thước model (default: medium)")
    parser.add_argument("--workers", type=int, default=2,
                       help="Số luồng xử lý (default: 2)")

    args = parser.parse_args()

    if not os.path.isdir(args.folder):
        print(f"❌ Folder not found: {args.folder}")
        sys.exit(1)

    print("🎬 Video Subtitle Generator - MacBook Pro M2 Optimized")
    print("=" * 60)
    print(f"📁 Folder: {args.folder}")
    print(f"🌍 Language: {args.lang}")
    print(f"📦 Model: {args.model}")
    print(f"🔧 Workers: {args.workers}")
    print("=" * 60)

    generator = M2SubtitleGenerator(
        model_size=args.model,
        max_workers=args.workers
    )

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
