#!/bin/bash

# 🔧 Quick Fix Script - Giải quyết lỗi MPS ngay lập tức
# Dành cho MacBook Pro M2

echo "🔧 Quick Fix cho lỗi MPS..."
echo "=" * 40

# Thiết lập environment variables
export TK_SILENCE_DEPRECATION=1
export PYTORCH_ENABLE_MPS_FALLBACK=1

echo "✅ Đã thiết lập environment variables"

# Kiểm tra PyTorch version
echo "📊 Kiểm tra PyTorch..."
python3 -c "
import torch
print(f'PyTorch version: {torch.__version__}')
print(f'MPS available: {torch.backends.mps.is_available()}')
if torch.backends.mps.is_available():
    print('✅ MPS working')
else:
    print('❌ MPS not available')
"

echo ""
echo "🎯 Bây giờ thử chạy lại:"
echo "python3 subedit_optimized.py --gui"
echo ""
echo "💡 Nếu vẫn lỗi, chạy: python3 fix_mps.py"




