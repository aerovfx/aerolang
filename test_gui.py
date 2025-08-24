#!/usr/bin/env python3
"""
🧪 GUI Test Script
Test giao diện GUI cho Video Subtitle Generator
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import subprocess
from pathlib import Path

def test_folder_dialog():
    """Test folder dialog"""
    print("🧪 Testing folder dialog...")
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        folder = filedialog.askdirectory(
            title="🎬 Test - Chọn thư mục chứa video",
            initialdir=os.path.expanduser("~/Desktop")
        )
        
        if folder:
            print(f"✅ Folder selected: {folder}")
            
            # Kiểm tra video files
            video_extensions = {'.mp4', '.mov', '.mkv', '.avi', '.flv', '.m4v', '.webm'}
            video_files = []
            
            for file in os.listdir(folder):
                if Path(file).suffix.lower() in video_extensions:
                    video_files.append(file)
            
            print(f"📁 Found {len(video_files)} video files")
            for video in video_files[:3]:
                print(f"   - {video}")
                
        else:
            print("❌ No folder selected")
            
    except Exception as e:
        print(f"❌ Dialog error: {e}")
    finally:
        root.destroy()

def test_gui_components():
    """Test GUI components"""
    print("🧪 Testing GUI components...")
    
    root = tk.Tk()
    root.withdraw()
    
    try:
        # Test message box
        result = messagebox.askyesno("Test", "Đây là test message box")
        print(f"✅ Message box result: {result}")
        
        # Test combobox
        combo = ttk.Combobox(root, values=["vi", "en", "auto"])
        combo.set("vi")
        print(f"✅ Combobox value: {combo.get()}")
        
        # Test progress bar
        progress = ttk.Progressbar(root, maximum=100)
        progress['value'] = 50
        print(f"✅ Progress bar value: {progress['value']}")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI components error: {e}")
        return False
    finally:
        root.destroy()

def test_subprocess():
    """Test subprocess functionality"""
    print("🧪 Testing subprocess...")
    
    try:
        # Test simple command
        result = subprocess.run(["python3", "--version"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"✅ Subprocess working: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Subprocess failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Subprocess error: {e}")
        return False

def test_threading():
    """Test threading functionality"""
    print("🧪 Testing threading...")
    
    def test_function():
        import time
        time.sleep(1)
        print("   ✅ Thread executed successfully")
    
    try:
        thread = threading.Thread(target=test_function)
        thread.daemon = True
        thread.start()
        thread.join(timeout=5)
        
        if thread.is_alive():
            print("   ❌ Thread timeout")
            return False
        else:
            print("   ✅ Threading working")
            return True
            
    except Exception as e:
        print(f"   ❌ Threading error: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("🧪 Testing file operations...")
    
    try:
        # Test file creation
        test_file = "test_gui_temp.txt"
        with open(test_file, "w") as f:
            f.write("Test content")
        
        # Test file reading
        with open(test_file, "r") as f:
            content = f.read()
        
        # Cleanup
        os.remove(test_file)
        
        if content == "Test content":
            print("✅ File operations working")
            return True
        else:
            print("❌ File operations failed")
            return False
            
    except Exception as e:
        print(f"❌ File operations error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 GUI Test Suite")
    print("=" * 40)
    
    tests = [
        ("Folder Dialog", test_folder_dialog),
        ("GUI Components", test_gui_components),
        ("Subprocess", test_subprocess),
        ("Threading", test_threading),
        ("File Operations", test_file_operations)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} passed")
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} error: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All tests passed! GUI should work correctly.")
    else:
        print("⚠️  Some tests failed. Check the issues above.")
    
    print("\n💡 Next steps:")
    print("1. Run: python3 subtitle_gui.py")
    print("2. Test folder selection")
    print("3. Test video processing")

if __name__ == "__main__":
    main()
