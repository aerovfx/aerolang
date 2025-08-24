#!/bin/bash
"""
🎬 Setup Script for MacBook Pro M2
Cài đặt môi trường cho Video Subtitle Generator
"""

echo "🎬 Video Subtitle Generator - MacBook Pro M2 Setup"
echo "=================================================="

# Kiểm tra Python
echo "🔍 Checking Python..."
if command -v python3 &> /dev/null; then
    python_version=$(python3 --version)
    echo "✅ Python found: $python_version"
else
    echo "❌ Python3 not found. Please install Python 3.8+"
    exit 1
fi

# Tạo virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Cài đặt PyTorch nightly cho MPS support tốt hơn
echo "📦 Installing PyTorch nightly for MPS support..."
pip install --pre torch torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

# Cài đặt các dependencies khác
echo "📦 Installing other dependencies..."
pip install openai-whisper tqdm psutil

# Kiểm tra cài đặt
echo "🧪 Testing installation..."
python3 -c "
import torch
import whisper
import psutil
print('✅ PyTorch version:', torch.__version__)
print('✅ Whisper version:', whisper.__version__)
print('✅ MPS available:', torch.backends.mps.is_available())
print('✅ CUDA available:', torch.cuda.is_available())
"

# Tạo file permissions
echo "🔐 Setting file permissions..."
chmod +x subtitle_m2_optimized.py
chmod +x run_subtitle.py
chmod +x batch_subtitle.py

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📋 Usage:"
echo "  1. Single folder: python3 run_subtitle.py"
echo "  2. Direct command: python3 subtitle_m2_optimized.py /path/to/folder"
echo "  3. Batch processing: python3 batch_subtitle.py /path/to/root"
echo ""
echo "💡 Tips:"
echo "  - Use model 'medium' for best balance on M2"
echo "  - Use 2 workers for optimal performance"
echo "  - Close other apps when processing large videos"
echo ""
echo "🚀 Ready to generate subtitles!"










