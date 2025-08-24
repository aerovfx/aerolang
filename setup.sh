#!/bin/bash

# 🚀 Setup Script cho Video Subtitle Generator
# Tối ưu cho MacBook Pro M2 với 16GB RAM

echo "🎬 Bắt đầu setup Video Subtitle Generator cho MacBook Pro M2..."

# Kiểm tra Python version
echo "🐍 Kiểm tra Python version..."
python3 --version

# Tạo virtual environment
echo "📦 Tạo virtual environment..."
python3 -m venv whisper_env

# Kích hoạt virtual environment
echo "🔧 Kích hoạt virtual environment..."
source whisper_env/bin/activate

# Upgrade pip
echo "⬆️  Upgrade pip..."
pip install --upgrade pip

# Cài đặt PyTorch cho Apple Silicon
echo "🔥 Cài đặt PyTorch cho Apple Silicon M2..."
# Sử dụng nightly build để có MPS support tốt nhất
pip install --pre torch torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Cài đặt các dependencies khác
echo "📚 Cài đặt dependencies..."
pip install -r requirements.txt

# Kiểm tra cài đặt
echo "✅ Kiểm tra cài đặt..."
python3 -c "import torch; print(f'PyTorch version: {torch.__version__}')"
python3 -c "import torch; print(f'MPS available: {torch.backends.mps.is_available()}')"
python3 -c "import whisper; print('Whisper installed successfully')"

echo ""
echo "🎉 Setup hoàn thành!"
echo ""
echo "📖 Cách sử dụng:"
echo "1. Kích hoạt môi trường: source whisper_env/bin/activate"
echo ""
echo "🎯 Các cách chạy:"
echo "  GUI hoàn toàn:     python3 subtitle_gui.py"
echo "  Giao diện đơn giản: python3 run_subtitle.py"
echo "  Command line:       python3 subedit_optimized.py /path/to/video/folder"
echo "  Với GUI picker:     python3 subedit_optimized.py --gui"
echo ""
echo "🔧 Các tùy chọn:"
echo "  --lang vi          : Ngôn ngữ đầu ra (mặc định: vi)"
echo "  --model medium     : Kích thước model (tiny, base, small, medium, large)"
echo "  --workers 2        : Số luồng tối đa (mặc định: 2)"
echo "  --gui              : Sử dụng GUI để chọn thư mục"
echo ""
echo "🧪 Test GUI:"
echo "  python3 test_gui.py"
echo ""
echo "💡 Tips cho M2:"
echo "- Sử dụng model 'medium' cho chất lượng tốt và tốc độ cân bằng"
echo "- Giữ workers = 2 để tối ưu hiệu suất"
echo "- Đảm bảo có ít nhất 8GB RAM trống khi chạy"
