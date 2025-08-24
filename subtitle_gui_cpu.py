#!/usr/bin/env python3
"""
💻 CPU GUI Wrapper
Force sử dụng CPU cho GUI version
"""

import os
import sys

# Force CPU environment
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['FORCE_CUDA'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

# Import và chạy GUI
if __name__ == "__main__":
    from subtitle_gui import main
    main()
