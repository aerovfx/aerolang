#!/usr/bin/env python3
"""
⚡ Quick GUI Test
Test nhanh giao diện GUI
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

def quick_test():
    """Quick test GUI functionality"""
    print("⚡ Quick GUI Test")
    print("=" * 30)
    
    # Test 1: Tkinter import
    print("1. Testing tkinter import...")
    try:
        import tkinter
        print("   ✅ Tkinter available")
    except ImportError:
        print("   ❌ Tkinter not available")
        return False
    
    # Test 2: Folder dialog
    print("2. Testing folder dialog...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        folder = filedialog.askdirectory(
            title="🎬 Quick Test - Chọn thư mục",
            initialdir=os.path.expanduser("~/Desktop")
        )
        
        if folder:
            print(f"   ✅ Folder selected: {folder}")
            
            # Check for video files
            video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
            video_count = 0
            
            for file in os.listdir(folder):
                if os.path.splitext(file)[1].lower() in video_extensions:
                    video_count += 1
            
            print(f"   📁 Found {video_count} video files")
            
        else:
            print("   ⚠️  No folder selected (user cancelled)")
            
    except Exception as e:
        print(f"   ❌ Dialog error: {e}")
        return False
    finally:
        root.destroy()
    
    # Test 3: Message box
    print("3. Testing message box...")
    root = tk.Tk()
    root.withdraw()
    
    try:
        result = messagebox.askyesno("Quick Test", "Đây là test message box")
        print(f"   ✅ Message box result: {result}")
    except Exception as e:
        print(f"   ❌ Message box error: {e}")
        return False
    finally:
        root.destroy()
    
    print("\n✅ Quick test completed!")
    print("💡 GUI should work correctly.")
    return True

if __name__ == "__main__":
    quick_test()










