#!/usr/bin/env python3
"""
🎬 Simple GUI Test
GUI đơn giản để test và debug
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class SimpleGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎬 Simple GUI Test")
        self.root.geometry("500x400")
        
        # Biến lưu trữ
        self.folder_path = tk.StringVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện đơn giản"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text="🎬 Video Subtitle Generator", 
                              font=("Arial", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        subtitle_label = tk.Label(main_frame, text="Simple GUI Test", 
                                 font=("Arial", 10))
        subtitle_label.pack(pady=(0, 20))
        
        # Folder selection
        folder_frame = tk.LabelFrame(main_frame, text="📁 Chọn thư mục video", padx=10, pady=10)
        folder_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(folder_frame, text="Thư mục chứa video:").pack(anchor=tk.W)
        
        # Entry và button trong frame
        entry_frame = tk.Frame(folder_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 0))
        
        folder_entry = tk.Entry(entry_frame, textvariable=self.folder_path, width=40)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(entry_frame, text="Duyệt...", command=self.browse_folder)
        browse_btn.pack(side=tk.RIGHT)
        
        # Settings
        settings_frame = tk.LabelFrame(main_frame, text="⚙️ Cài đặt", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Language
        lang_frame = tk.Frame(settings_frame)
        lang_frame.pack(fill=tk.X, pady=5)
        tk.Label(lang_frame, text="Ngôn ngữ:", width=15).pack(side=tk.LEFT)
        lang_var = tk.StringVar(value="vi")
        lang_combo = ttk.Combobox(lang_frame, textvariable=lang_var, 
                                 values=["vi", "en", "auto"], state="readonly", width=15)
        lang_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Model
        model_frame = tk.Frame(settings_frame)
        model_frame.pack(fill=tk.X, pady=5)
        tk.Label(model_frame, text="Model:", width=15).pack(side=tk.LEFT)
        model_var = tk.StringVar(value="medium")
        model_combo = ttk.Combobox(model_frame, textvariable=model_var,
                                  values=["tiny", "base", "small", "medium", "large"], 
                                  state="readonly", width=15)
        model_combo.pack(side=tk.LEFT, padx=(10, 0))
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(pady=20)
        
        start_btn = tk.Button(button_frame, text="🚀 Bắt đầu xử lý", 
                             command=self.start_processing, bg="green", fg="white")
        start_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        test_btn = tk.Button(button_frame, text="🧪 Test", command=self.test_system)
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        exit_btn = tk.Button(button_frame, text="❌ Thoát", command=self.root.quit)
        exit_btn.pack(side=tk.LEFT)
        
        # Status
        self.status_label = tk.Label(main_frame, text="Sẵn sàng", fg="blue")
        self.status_label.pack(pady=(20, 0))
        
    def browse_folder(self):
        """Mở dialog chọn thư mục"""
        folder = filedialog.askdirectory(
            title="🎬 Chọn thư mục chứa video",
            initialdir=os.path.expanduser("~/Desktop")
        )
        if folder:
            self.folder_path.set(folder)
            self.status_label.config(text=f"Đã chọn: {folder}")
            
            # Kiểm tra video files
            video_count = self.count_video_files(folder)
            if video_count > 0:
                self.status_label.config(text=f"Tìm thấy {video_count} video files")
            else:
                self.status_label.config(text="Không tìm thấy video files")
    
    def count_video_files(self, folder_path):
        """Đếm số video files trong thư mục"""
        video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
        count = 0
        try:
            for file in os.listdir(folder_path):
                if os.path.splitext(file)[1].lower() in video_extensions:
                    count += 1
        except Exception:
            pass
        return count
    
    def start_processing(self):
        """Bắt đầu xử lý"""
        folder = self.folder_path.get()
        if not folder:
            messagebox.showerror("Lỗi", "Vui lòng chọn thư mục chứa video!")
            return
        
        if not os.path.isdir(folder):
            messagebox.showerror("Lỗi", "Thư mục không tồn tại!")
            return
        
        video_count = self.count_video_files(folder)
        if video_count == 0:
            result = messagebox.askyesno("Cảnh báo", 
                                       "Không tìm thấy video files trong thư mục.\nBạn có muốn tiếp tục?")
            if not result:
                return
        
        self.status_label.config(text="Đang xử lý...")
        messagebox.showinfo("Thông báo", f"Bắt đầu xử lý {video_count} video files")
    
    def test_system(self):
        """Test hệ thống"""
        self.status_label.config(text="Đang test hệ thống...")
        messagebox.showinfo("Test", "Test hệ thống thành công!")
        self.status_label.config(text="Test hoàn thành")
    
    def run(self):
        """Chạy GUI"""
        self.root.mainloop()

def main():
    """Main function"""
    try:
        app = SimpleGUI()
        app.run()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()










