#!/bin/bash
# Auto-fix script for MPS issues

export TK_SILENCE_DEPRECATION=1
export PYTORCH_ENABLE_MPS_FALLBACK=1

echo "🔧 Running auto-fix for MPS..."
python3 fix_mps.py

echo "✅ Fix completed!"
