#!/usr/bin/env python3
"""
🎬 Video Subtitle Generator - Fixed GUI Version
Giao diện đồ họa đã sửa cho MacBook Pro M2
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
from pathlib import Path

class SubtitleGeneratorGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎬 Video Subtitle Generator - M2 Optimized")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Biến lưu trữ
        self.folder_path = tk.StringVar()
        self.selected_lang = tk.StringVar(value="vi")
        self.selected_model = tk.StringVar(value="medium")
        self.workers_count = tk.IntVar(value=2)
        
        # Khởi tạo process
        self.process = None
        self.processing_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="🎬 Video Subtitle Generator", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(main_frame, text="MacBook Pro M2 Optimized", 
                                 font=("Arial", 10))
        subtitle_label.pack(pady=(0, 20))
        
        # Folder selection
        folder_frame = tk.LabelFrame(main_frame, text="📁 Chọn thư mục video", padx=10, pady=10)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(folder_frame, text="Thư mục chứa video:").pack(anchor=tk.W)
        
        # Entry và button trong frame
        entry_frame = tk.Frame(folder_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        folder_entry = tk.Entry(entry_frame, textvariable=self.folder_path, width=50)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(entry_frame, text="Duyệt...", command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT)
        
        # Settings frame
        settings_frame = tk.LabelFrame(main_frame, text="⚙️ Cài đặt", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Language selection
        lang_frame = tk.Frame(settings_frame)
        lang_frame.pack(fill=tk.X, pady=5)
        tk.Label(lang_frame, text="Ngôn ngữ đầu ra:", width=15).pack(side=tk.LEFT)
        lang_combo = ttk.Combobox(lang_frame, textvariable=self.selected_lang, 
                                 values=["vi", "en", "auto"], state="readonly", width=15)
        lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Model selection
        model_frame = tk.Frame(settings_frame)
        model_frame.pack(fill=tk.X, pady=5)
        tk.Label(model_frame, text="Kích thước model:", width=15).pack(side=tk.LEFT)
        model_combo = ttk.Combobox(model_frame, textvariable=self.selected_model,
                                  values=["tiny", "base", "small", "medium", "large", "auto"], 
                                  state="readonly", width=15)
        model_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Workers selection
        workers_frame = tk.Frame(settings_frame)
        workers_frame.pack(fill=tk.X, pady=5)
        tk.Label(workers_frame, text="Số luồng xử lý:", width=15).pack(side=tk.LEFT)
        workers_spin = ttk.Spinbox(workers_frame, from_=1, to=4, textvariable=self.workers_count, width=15)
        workers_spin.pack(side=tk.LEFT, padx=(10, 0))
        
        # Model info
        model_info = tk.Label(settings_frame, text="💡 Khuyến nghị: medium cho M2 16GB RAM", 
                             font=("Arial", 9), fg="blue")
        model_info.pack(anchor=tk.W, pady=(10, 0))
        
        # Quick actions
        quick_frame = tk.LabelFrame(main_frame, text="⚡ Quick Actions", padx=10, pady=10)
        quick_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Test button
        test_btn = tk.Button(quick_frame, text="🧪 Test System", command=self.test_system)
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Clear log button
        clear_btn = tk.Button(quick_frame, text="🗑️ Clear Log", command=self.clear_log)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Open folder button
        open_btn = tk.Button(quick_frame, text="📁 Open Folder", command=self.open_folder)
        open_btn.pack(side=tk.LEFT)
        
        # Buttons frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        self.start_button = tk.Button(button_frame, text="🚀 Bắt đầu xử lý", 
                                     command=self.start_processing, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = tk.Button(button_frame, text="⏹️ Dừng", 
                                    command=self.stop_processing, state="disabled")
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = tk.Button(button_frame, text="❌ Thoát", command=self.root.quit)
        exit_btn.pack(side=tk.LEFT)
        
        # Progress frame
        self.progress_frame = tk.LabelFrame(main_frame, text="📊 Tiến độ", padx=10, pady=10)
        self.progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.progress_frame, variable=self.progress_var, 
                                           maximum=100, length=400)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.status_label = tk.Label(self.progress_frame, text="Sẵn sàng")
        self.status_label.pack(anchor=tk.W)
        
        # Log frame
        log_frame = tk.LabelFrame(main_frame, text="📝 Log", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Log text với scrollbar
        log_text_frame = tk.Frame(log_frame)
        log_text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = tk.Text(log_text_frame, height=8, width=70)
        scrollbar = tk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def browse_folder(self):
        """Mở dialog chọn thư mục"""
        folder = filedialog.askdirectory(
            title="🎬 Chọn thư mục chứa video",
            initialdir=os.path.expanduser("~/Desktop")
        )
        if folder:
            self.folder_path.set(folder)
            self.log_message(f"✅ Đã chọn thư mục: {folder}")
            
            # Kiểm tra video files
            video_count = self.count_video_files(folder)
            if video_count > 0:
                self.log_message(f"📁 Tìm thấy {video_count} video files")
            else:
                self.log_message("⚠️ Không tìm thấy video files trong thư mục")
    
    def count_video_files(self, folder_path):
        """Đếm số video files trong thư mục"""
        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        count = 0
        try:
            for file in os.listdir(folder_path):
                if Path(file).suffix.lower() in video_extensions:
                    count += 1
        except Exception:
            pass
        return count
    
    def log_message(self, message):
        """Thêm message vào log"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def update_progress(self, value, status):
        """Cập nhật progress bar"""
        self.progress_var.set(value)
        self.status_label.config(text=status)
        self.root.update_idletasks()
    
    def validate_inputs(self):
        """Kiểm tra input"""
        if not self.folder_path.get():
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục chứa video!")
            return False
        
        if not os.path.isdir(self.folder_path.get()):
            messagebox.showerror("Lỗi", "Thư mục không tồn tại!")
            return False
        
        video_count = self.count_video_files(self.folder_path.get())
        if video_count == 0:
            result = messagebox.askyesno("Cảnh báo", 
                                       "Không tìm thấy video files trong thư mục.\nBạn có muốn tiếp tục?")
            if not result:
                return False
        
        return True
    
    def start_processing(self):
        """Bắt đầu xử lý video"""
        if not self.validate_inputs():
            return
        
        # Disable start button và enable stop button
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        # Start processing in separate thread
        self.processing_thread = threading.Thread(target=self.process_videos)
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def stop_processing(self):
        """Dừng xử lý video"""
        if hasattr(self, 'process') and self.process:
            self.process.terminate()
            self.log_message("⏹️ Đã dừng xử lý")
        
        # Re-enable start button và disable stop button
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
    
    def process_videos(self):
        """Xử lý video trong thread riêng"""
        try:
            self.log_message("🚀 Bắt đầu xử lý video...")
            self.update_progress(10, "Đang khởi tạo...")
            
            # Build command
            cmd = [
                "python3", "subedit_optimized.py",
                self.folder_path.get(),
                "--lang", self.selected_lang.get(),
                "--model", self.selected_model.get(),
                "--workers", str(self.workers_count.get())
            ]
            
            self.log_message(f"🔧 Lệnh: {' '.join(cmd)}")
            self.update_progress(20, "Đang chạy lệnh...")
            
            # Run subprocess
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Monitor output
            progress = 20
            for line in self.process.stdout:
                line = line.strip()
                if line:
                    self.log_message(line)
                    
                    # Update progress based on output
                    if "Đang xử lý" in line:
                        progress = min(progress + 10, 90)
                        self.update_progress(progress, "Đang xử lý video...")
                    elif "Hoàn thành" in line:
                        progress = min(progress + 5, 95)
                        self.update_progress(progress, "Hoàn thành video...")
            
            self.process.wait()
            
            if self.process.returncode == 0:
                self.update_progress(100, "✅ Hoàn thành!")
                self.log_message("🎉 Xử lý video thành công!")
                messagebox.showinfo("Thành công", "Đã xử lý video thành công!")
            else:
                self.update_progress(100, "❌ Lỗi!")
                self.log_message("❌ Có lỗi xảy ra trong quá trình xử lý")
                messagebox.showerror("Lỗi", "Có lỗi xảy ra trong quá trình xử lý video!")
                
        except Exception as e:
            self.log_message(f"❌ Lỗi: {str(e)}")
            messagebox.showerror("Lỗi", f"Lỗi: {str(e)}")
        finally:
            # Re-enable start button và disable stop button
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")
    
    def test_system(self):
        """Test hệ thống"""
        self.log_message("🧪 Testing system...")
        
        # Test trong thread riêng
        def test_thread():
            try:
                import subprocess
                result = subprocess.run([sys.executable, "check_compatibility.py"], 
                                      capture_output=True, text=True, timeout=60)
                
                if result.returncode == 0:
                    self.log_message("✅ System test passed")
                else:
                    self.log_message("❌ System test failed")
                    self.log_message(result.stderr)
                    
            except Exception as e:
                self.log_message(f"❌ Test error: {e}")
        
        thread = threading.Thread(target=test_thread)
        thread.daemon = True
        thread.start()
    
    def clear_log(self):
        """Xóa log"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🗑️ Log cleared")
    
    def open_folder(self):
        """Mở thư mục đã chọn"""
        folder = self.folder_path.get()
        if folder and os.path.isdir(folder):
            try:
                import subprocess
                subprocess.run(["open", folder])  # macOS
                self.log_message(f"📁 Opened folder: {folder}")
            except Exception as e:
                self.log_message(f"❌ Error opening folder: {e}")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn thư mục trước!")
    
    def run(self):
        """Chạy GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = SubtitleGeneratorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể khởi động GUI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()










