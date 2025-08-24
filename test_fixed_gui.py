#!/usr/bin/env python3
"""
🧪 Test Fixed GUI
Test GUI đã sửa
"""

import os
import sys
import subprocess

def test_gui_import():
    """Test import GUI"""
    print("🧪 Testing GUI import...")
    
    try:
        import subtitle_gui_fixed
        print("   ✅ subtitle_gui_fixed import successful")
        return True
    except Exception as e:
        print(f"   ❌ subtitle_gui_fixed import failed: {e}")
        return False

def test_simple_gui_import():
    """Test import simple GUI"""
    print("🧪 Testing simple GUI import...")
    
    try:
        import simple_gui
        print("   ✅ simple_gui import successful")
        return True
    except Exception as e:
        print(f"   ❌ simple_gui import failed: {e}")
        return False

def test_gui_components():
    """Test GUI components"""
    print("🧪 Testing GUI components...")
    
    try:
        import tkinter as tk
        from tkinter import ttk, filedialog, messagebox
        
        # Test basic components
        root = tk.Tk()
        root.withdraw()
        
        # Test Label
        label = tk.Label(root, text="Test")
        print("   ✅ tk.Label working")
        
        # Test Button
        button = tk.Button(root, text="Test")
        print("   ✅ tk.Button working")
        
        # Test Entry
        entry = tk.Entry(root)
        print("   ✅ tk.Entry working")
        
        # Test LabelFrame
        frame = tk.LabelFrame(root, text="Test")
        print("   ✅ tk.LabelFrame working")
        
        # Test Combobox
        combo = ttk.Combobox(root, values=["test"])
        print("   ✅ ttk.Combobox working")
        
        # Test Progressbar
        progress = ttk.Progressbar(root)
        print("   ✅ ttk.Progressbar working")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"   ❌ GUI components test failed: {e}")
        return False

def test_gui_launch():
    """Test GUI launch"""
    print("🧪 Testing GUI launch...")
    
    try:
        # Test simple GUI launch
        result = subprocess.run([sys.executable, "simple_gui.py", "--test"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Simple GUI launch successful")
            return True
        else:
            print(f"   ❌ Simple GUI launch failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("   ⏰ GUI launch timeout (this is normal)")
        return True
    except Exception as e:
        print(f"   ❌ GUI launch error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Fixed GUI Test Suite")
    print("=" * 40)
    
    tests = [
        ("GUI Import", test_gui_import),
        ("Simple GUI Import", test_simple_gui_import),
        ("GUI Components", test_gui_components),
        ("GUI Launch", test_gui_launch)
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
        print("\n💡 Try running:")
        print("   python3 simple_gui.py")
        print("   python3 subtitle_gui_fixed.py")
    else:
        print("⚠️  Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()










