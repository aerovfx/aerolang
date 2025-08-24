# 🎬 Video Subtitle Generator - MacBook Pro M2 Optimized

Tạo phụ đề (.srt) và nội dung (.txt) từ video sử dụng OpenAI Whisper, được tối ưu đặc biệt cho MacBook Pro M2 với 16GB RAM.

## 🚀 Đặc điểm chính

- ✅ **Tối ưu cho M2**: Sử dụng MPS (Metal Performance Shaders) cho hiệu suất tối đa
- ✅ **Không cần GUI**: Chạy hoàn toàn qua command line
- ✅ **Memory management**: Quản lý bộ nhớ thông minh cho 16GB RAM
- ✅ **Fallback mechanism**: Tự động chuyển sang CPU nếu MPS lỗi
- ✅ **Batch processing**: Xử lý nhiều thư mục cùng lúc
- ✅ **Progress tracking**: Theo dõi tiến độ real-time

## 🛠️ Cài đặt

### Bước 1: Clone và setup
```bash
# Clone repository
git clone <repository-url>
cd <repository-folder>

# Setup môi trường
chmod +x setup_m2.sh
./setup_m2.sh
```

### Bước 2: Activate virtual environment
```bash
source venv/bin/activate
```

## 🎯 Cách sử dụng

### **Cách 1: Interactive Mode (Khuyến nghị)**
```bash
python3 run_subtitle.py
```
- Hướng dẫn từng bước
- Chọn thư mục, ngôn ngữ, model
- Hiển thị kết quả chi tiết

### **Cách 2: Direct Command**
```bash
python3 subtitle_m2_optimized.py /path/to/video/folder --lang vi --model medium
```

**Options:**
- `--lang`: Ngôn ngữ đích (vi, en, auto)
- `--model`: Kích thước model (tiny, base, small, medium, large)
- `--workers`: Số luồng xử lý (1-4, default: 2)
- `--verbose`: Hiển thị thông tin chi tiết

### **Cách 3: Batch Processing**
```bash
python3 batch_subtitle.py /path/to/root/folder --lang vi --model medium
```

**Options:**
- `--max-depth`: Độ sâu tìm kiếm (default: 3)
- `--dry-run`: Chỉ hiển thị thư mục sẽ xử lý

## 📊 Hiệu suất MacBook Pro M2

### Model Performance
| Model | Speed | Accuracy | Memory | Khuyến nghị |
|-------|-------|----------|--------|-------------|
| tiny | ⚡⚡⚡ | ⭐⭐ | 💾💾 | Test nhanh |
| base | ⚡⚡ | ⭐⭐⭐ | 💾💾💾 | Xử lý nhanh |
| small | ⚡ | ⭐⭐⭐⭐ | 💾💾💾💾 | Cân bằng |
| medium | ⚡ | ⭐⭐⭐⭐⭐ | 💾💾💾💾💾 | **Khuyến nghị** |
| large | 🐌 | ⭐⭐⭐⭐⭐ | 💾💾💾💾💾💾 | Chất lượng cao |

### Thời gian xử lý (video 5 phút)
- **tiny**: ~30 giây
- **base**: ~1 phút
- **small**: ~2 phút
- **medium**: ~3-5 phút ⭐
- **large**: ~8-10 phút

## 📁 Định dạng file đầu ra

### File .txt
```
Nội dung văn bản được trích xuất từ video, không có timestamp.
```

### File .srt
```
1
00:00:00,000 --> 00:00:03,500
Đây là dòng phụ đề đầu tiên

2
00:00:03,500 --> 00:00:07,200
Đây là dòng phụ đề thứ hai
```

## 🎬 Video formats hỗ trợ

- MP4 (.mp4)
- MOV (.mov)
- MKV (.mkv)
- AVI (.avi)
- FLV (.flv)
- M4V (.m4v)
- WebM (.webm)

## ⚙️ Tối ưu hóa M2

### Memory Management
- Tự động cleanup MPS cache
- Garbage collection sau mỗi video
- Memory monitoring real-time

### MPS Optimization
- Sử dụng float32 thay vì fp16
- Fallback to CPU nếu MPS lỗi
- Tối ưu model loading

### Performance Tips
- Sử dụng model medium cho cân bằng tốt nhất
- Đóng các ứng dụng khác khi xử lý
- Xử lý video ngắn (< 10 phút) để tránh lỗi memory

## 🔧 Troubleshooting

### Lỗi MPS
```bash
# Kiểm tra MPS
python3 -c "import torch; print('MPS:', torch.backends.mps.is_available())"

# Nếu lỗi, script sẽ tự động fallback sang CPU
```

### Lỗi Memory
```bash
# Giảm số workers
python3 subtitle_m2_optimized.py /path/to/folder --workers 1

# Sử dụng model nhỏ hơn
python3 subtitle_m2_optimized.py /path/to/folder --model small
```

### Lỗi Dependencies
```bash
# Reinstall dependencies
pip install --upgrade torch torchaudio openai-whisper tqdm psutil
```

## 📋 Ví dụ sử dụng

### Xử lý một thư mục
```bash
# Interactive mode
python3 run_subtitle.py

# Direct command
python3 subtitle_m2_optimized.py ~/Videos/MyVideos --lang vi --model medium
```

### Xử lý batch
```bash
# Tìm và xử lý tất cả video trong thư mục
python3 batch_subtitle.py ~/Videos --lang vi --model medium

# Dry run để xem sẽ xử lý gì
python3 batch_subtitle.py ~/Videos --dry-run
```

### Xử lý với cài đặt tùy chỉnh
```bash
# Sử dụng model large cho chất lượng cao nhất
python3 subtitle_m2_optimized.py ~/Videos --model large --workers 1

# Xử lý nhanh với model tiny
python3 subtitle_m2_optimized.py ~/Videos --model tiny --workers 4
```

## 🎉 Kết quả

Sau khi xử lý thành công, bạn sẽ có:
1. **File .txt**: Nội dung văn bản từ video
2. **File .srt**: Phụ đề với timestamp chính xác
3. **Log chi tiết**: Thông tin quá trình xử lý
4. **Performance metrics**: Thời gian xử lý và memory usage

## 💡 Tips

1. **Bắt đầu với model tiny** để test nhanh
2. **Sử dụng model medium** cho kết quả tốt nhất
3. **Xử lý video ngắn** trước khi xử lý video dài
4. **Đóng các ứng dụng khác** khi xử lý
5. **Sử dụng batch processing** cho nhiều thư mục

## 🆘 Hỗ trợ

### Kiểm tra nhanh
```bash
# Test installation
python3 -c "import torch, whisper; print('All good!')"

# Test MPS
python3 -c "import torch; print('MPS:', torch.backends.mps.is_available())"
```

### Log files
- Script sẽ hiển thị log chi tiết trong terminal
- Theo dõi memory usage và progress
- Hiển thị lỗi chi tiết nếu có

---

**🎬 Chúc bạn sử dụng hiệu quả!**










