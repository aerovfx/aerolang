#!/usr/bin/env python3
"""
💻 CPU Wrapper Script
Force sử dụng CPU cho Video Subtitle Generator
"""

import os
import sys

# Force CPU environment
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['FORCE_CUDA'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

# Import và chạy main script
if __name__ == "__main__":
    # Import main script
    from subedit_optimized import main
    main()
