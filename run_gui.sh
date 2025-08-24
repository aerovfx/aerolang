#!/bin/bash

# 🎬 Run GUI Script
# Chạy GUI với environment variables đúng

echo "🎬 Video Subtitle Generator - GUI"
echo "=" * 40

# Set environment variables
export TK_SILENCE_DEPRECATION=1
export PYTORCH_ENABLE_MPS_FALLBACK=1

echo "✅ Environment variables set"
echo "   TK_SILENCE_DEPRECATION=1"
echo "   PYTORCH_ENABLE_MPS_FALLBACK=1"

# Check if virtual environment is activated
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "⚠️  Virtual environment not activated"
    echo "💡 Activating whisper_env..."
    source whisper_env/bin/activate
fi

echo ""
echo "🚀 Starting GUI..."
echo "💡 Press Ctrl+C to stop"

# Run GUI
python3 subtitle_gui.py










