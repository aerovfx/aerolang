# 🎬 Video Subtitle Generator - Hướng dẫn sử dụng

## 📋 Tổng quan

Ứng dụng tạo phụ đề (.srt) và nội dung (.txt) từ video sử dụng OpenAI Whisper, được tối ưu cho MacBook Pro M2 với 16GB RAM.

## 🚀 Các phiên bản GUI

### 1. **GUI Tích hợp (Khuyến nghị)** - `subtitle_gui_integrated.py`
- ✅ Tích hợp trực tiếp với Whisper
- ✅ Tạo file .srt và .txt thực tế
- ✅ Xử lý video trực tiếp trong GUI
- ✅ Hiển thị tiến độ real-time
- ✅ Log chi tiết

### 2. **GUI Đơn giản** - `simple_gui.py`
- ✅ Giao diện đơn giản để test
- ✅ Chọn thư mục video
- ✅ Cài đặt cơ bản

### 3. **GUI Đã sửa** - `subtitle_gui_fixed.py`
- ✅ Sửa lỗi hiển thị GUI
- ✅ Gọi script bên ngoài

## 🛠️ Cài đặt

### Bước 1: Cài đặt dependencies
```bash
# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 2: Kiểm tra hệ thống
```bash
# Test compatibility
python3 check_compatibility.py

# Test subtitle creation
python3 test_subtitle_creation.py
```

## 🎯 Cách sử dụng

### **Cách 1: GUI Tích hợp (Khuyến nghị)**

```bash
python3 subtitle_gui_integrated.py
```

**Các bước:**
1. **Chọn thư mục video**: Click "Duyệt..." để chọn thư mục chứa video
2. **Load Model**: Click "📦 Load Model" để tải Whisper model
3. **Cài đặt**:
   - **Ngôn ngữ**: vi (Tiếng Việt), en (Tiếng Anh), auto (Tự động)
   - **Model size**: tiny, base, small, medium, large
4. **Bắt đầu xử lý**: Click "🚀 Bắt đầu xử lý"

**Kết quả:**
- File `.txt`: Nội dung văn bản
- File `.srt`: Phụ đề với timestamp

### **Cách 2: Command Line**

```bash
# Xử lý thư mục video
python3 subedit_optimized.py /path/to/video/folder --lang vi --model medium

# Với GUI chọn thư mục
python3 subedit_optimized.py --gui
```

### **Cách 3: Demo**

```bash
# Demo tạo subtitle
python3 demo_subtitle_creation.py
```

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

3
00:00:07,200 --> 00:00:10,800
Và đây là dòng phụ đề cuối cùng
```

## ⚙️ Cài đặt nâng cao

### Model sizes
- **tiny**: Nhanh nhất, độ chính xác thấp
- **base**: Nhanh, độ chính xác trung bình
- **small**: Cân bằng tốt
- **medium**: Độ chính xác cao (Khuyến nghị cho M2)
- **large**: Độ chính xác cao nhất, chậm nhất

### Ngôn ngữ
- **vi**: Tiếng Việt
- **en**: Tiếng Anh
- **auto**: Tự động phát hiện

## 🔧 Troubleshooting

### Lỗi MPS
```bash
# Fix MPS issues
python3 fix_mps.py

# Force CPU mode
python3 force_cpu.py
```

### Lỗi GUI
```bash
# Test GUI
python3 test_fixed_gui.py

# Quick GUI test
python3 quick_gui_test.py
```

### Lỗi Whisper
```bash
# Check compatibility
python3 check_compatibility.py

# Test MPS compatibility
python3 test_mps_compatibility.py
```

## 📊 Hiệu suất

### MacBook Pro M2 16GB RAM
- **Model tiny**: ~30 giây/video 5 phút
- **Model base**: ~1 phút/video 5 phút
- **Model small**: ~2 phút/video 5 phút
- **Model medium**: ~3-5 phút/video 5 phút (Khuyến nghị)
- **Model large**: ~8-10 phút/video 5 phút

### Tối ưu hóa
- Sử dụng model medium cho cân bằng tốt nhất
- Xử lý video ngắn (< 10 phút) để tránh lỗi memory
- Đóng các ứng dụng khác khi xử lý

## 🎬 Video formats hỗ trợ

- MP4 (.mp4)
- MOV (.mov)
- MKV (.mkv)
- AVI (.avi)
- FLV (.flv)
- M4V (.m4v)
- WebM (.webm)

## 📝 Log và Debug

### GUI Log
- Hiển thị trong GUI real-time
- Lưu thông tin xử lý
- Hiển thị lỗi chi tiết

### Command Line Log
```bash
# Verbose mode
python3 subedit_optimized.py /path/to/folder --verbose

# Debug mode
python3 subedit_optimized.py /path/to/folder --debug
```

## 🆘 Hỗ trợ

### Các script hỗ trợ
- `solve_all_issues.py`: Giải quyết tất cả vấn đề
- `demo_workflow.py`: Demo toàn bộ workflow
- `run_gui.sh`: Script chạy GUI với environment variables

### Kiểm tra nhanh
```bash
# Quick fix
./quick_fix.sh

# Summary
./summary.sh
```

## 🎉 Kết quả mong đợi

Sau khi xử lý thành công, bạn sẽ có:
1. **File .txt**: Nội dung văn bản từ video
2. **File .srt**: Phụ đề với timestamp chính xác
3. **Log chi tiết**: Thông tin quá trình xử lý
4. **Tiến độ real-time**: Theo dõi quá trình xử lý

## 💡 Tips

1. **Bắt đầu với model tiny** để test nhanh
2. **Sử dụng model medium** cho kết quả tốt nhất
3. **Xử lý video ngắn** trước khi xử lý video dài
4. **Kiểm tra log** để debug vấn đề
5. **Sử dụng GUI tích hợp** để dễ dàng nhất

---

**🎬 Chúc bạn sử dụng hiệu quả!**










