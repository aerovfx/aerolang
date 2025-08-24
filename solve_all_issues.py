#!/usr/bin/env python3
"""
🔧 Solve All Issues Script
Giải quyết tất cả các vấn đề MPS và tương thích
"""

import os
import sys
import subprocess
import platform

def print_header():
    """In header"""
    print("🔧 Solve All Issues - Video Subtitle Generator")
    print("=" * 60)
    print("Giải quyết tất cả các vấn đề MPS và tương thích")
    print("=" * 60)

def check_system():
    """Kiểm tra hệ thống"""
    print("💻 Kiểm tra hệ thống...")
    
    system = platform.system()
    machine = platform.machine()
    
    print(f"   OS: {system}")
    print(f"   Architecture: {machine}")
    
    if system == "Darwin" and machine == "arm64":
        print("   ✅ MacBook Apple Silicon detected")
        return True
    else:
        print("   ⚠️  Không phải MacBook Apple Silicon")
        return False

def run_script(script_name, description):
    """Chạy script với error handling"""
    print(f"\n🔄 {description}...")
    print(f"   Chạy: {script_name}")
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"   ✅ {description} thành công")
            return True
        else:
            print(f"   ❌ {description} thất bại")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"   ⏰ {description} timeout")
        return False
    except Exception as e:
        print(f"   ❌ {description} error: {e}")
        return False

def interactive_choice():
    """Cho phép người dùng chọn giải pháp"""
    print("\n🎯 Chọn giải pháp:")
    print("1. Auto-fix (khuyến nghị)")
    print("2. Test compatibility trước")
    print("3. Force CPU mode")
    print("4. Manual fix")
    
    choice = input("Chọn (1-4, mặc định: 1): ").strip()
    return choice

def auto_fix():
    """Auto-fix tất cả vấn đề"""
    print("\n🚀 Bắt đầu auto-fix...")
    
    # Step 1: Check compatibility
    print("\n📊 Step 1: Kiểm tra tương thích...")
    if not run_script("check_compatibility.py", "Compatibility check"):
        print("   ⚠️  Compatibility check failed, tiếp tục...")
    
    # Step 2: Test MPS
    print("\n🧪 Step 2: Test MPS compatibility...")
    if not run_script("test_mps_compatibility.py", "MPS compatibility test"):
        print("   ⚠️  MPS test failed, sẽ force CPU...")
    
    # Step 3: Fix MPS
    print("\n🔧 Step 3: Fix MPS issues...")
    if not run_script("fix_mps.py", "MPS fix"):
        print("   ⚠️  MPS fix failed, sẽ force CPU...")
    
    # Step 4: Force CPU nếu cần
    print("\n💻 Step 4: Force CPU mode...")
    if not run_script("force_cpu.py", "Force CPU"):
        print("   ❌ Force CPU failed")
        return False
    
    return True

def test_first():
    """Test trước khi fix"""
    print("\n🧪 Testing trước khi fix...")
    
    # Test compatibility
    if not run_script("check_compatibility.py", "Compatibility check"):
        print("   ❌ Compatibility issues detected")
        return False
    
    # Test MPS
    if not run_script("test_mps_compatibility.py", "MPS test"):
        print("   ⚠️  MPS issues detected")
        return False
    
    print("   ✅ All tests passed")
    return True

def force_cpu_only():
    """Chỉ force CPU"""
    print("\n💻 Force CPU mode only...")
    return run_script("force_cpu.py", "Force CPU")

def manual_fix():
    """Manual fix với hướng dẫn"""
    print("\n📋 Manual fix instructions:")
    print("1. Chạy: python3 check_compatibility.py")
    print("2. Chạy: python3 test_mps_compatibility.py")
    print("3. Nếu có lỗi MPS, chạy: python3 fix_mps.py")
    print("4. Nếu vẫn lỗi, chạy: python3 force_cpu.py")
    print("5. Test: python3 subedit_cpu.py --gui")
    
    input("\nNhấn Enter để tiếp tục...")

def create_summary():
    """Tạo summary script"""
    print("\n📝 Tạo summary script...")
    
    summary_content = '''#!/bin/bash
# Summary script - Video Subtitle Generator

echo "🎬 Video Subtitle Generator - Summary"
echo "=" * 40

echo "📋 Available scripts:"
echo "  subedit_optimized.py     - Main script (auto fallback)"
echo "  subedit_cpu.py           - CPU-only version"
echo "  subtitle_gui.py          - GUI version"
echo "  subtitle_gui_cpu.py      - GUI CPU-only version"

echo ""
echo "🔧 Troubleshooting:"
echo "  check_compatibility.py   - Check system compatibility"
echo "  test_mps_compatibility.py - Test MPS with Whisper"
echo "  fix_mps.py              - Fix MPS issues"
echo "  force_cpu.py            - Force CPU mode"

echo ""
echo "💡 Quick start:"
echo "  python3 subedit_cpu.py --gui"
echo "  python3 subtitle_gui_cpu.py"

echo ""
echo "✅ Ready to use!"
'''
    
    with open("summary.sh", "w") as f:
        f.write(summary_content)
    
    os.chmod("summary.sh", 0o755)
    print("   ✅ Created summary.sh")

def main():
    """Main function"""
    print_header()
    
    # Kiểm tra hệ thống
    if not check_system():
        print("\n❌ Script này chỉ dành cho MacBook Apple Silicon")
        return
    
    # Cho phép người dùng chọn
    choice = interactive_choice()
    
    success = False
    
    if choice == "1" or choice == "":
        success = auto_fix()
    elif choice == "2":
        success = test_first()
        if success:
            print("\n✅ Tests passed, system ready!")
        else:
            print("\n❌ Tests failed, run auto-fix")
    elif choice == "3":
        success = force_cpu_only()
    elif choice == "4":
        manual_fix()
        return
    else:
        print("❌ Lựa chọn không hợp lệ")
        return
    
    # Tạo summary
    create_summary()
    
    # Kết quả
    print("\n" + "=" * 60)
    if success:
        print("🎉 TẤT CẢ VẤN ĐỀ ĐÃ ĐƯỢC GIẢI QUYẾT!")
        print("\n📋 Cách sử dụng:")
        print("1. GUI: python3 subtitle_gui_cpu.py")
        print("2. Command line: python3 subedit_cpu.py --gui")
        print("3. Summary: ./summary.sh")
    else:
        print("❌ CÓ VẤN ĐỀ CHƯA ĐƯỢC GIẢI QUYẾT")
        print("\n💡 Thử manual fix:")
        print("1. python3 check_compatibility.py")
        print("2. python3 force_cpu.py")
        print("3. python3 subedit_cpu.py --gui")

if __name__ == "__main__":
    main()










