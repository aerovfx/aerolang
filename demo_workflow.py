#!/usr/bin/env python3
"""
🎬 Demo Workflow Script
Demo toàn bộ workflow của Video Subtitle Generator
"""

import os
import sys
import subprocess
import time

def print_header():
    """In header"""
    print("🎬 Video Subtitle Generator - Demo Workflow")
    print("=" * 50)
    print("Demo toàn bộ workflow từ setup đến sử dụng")
    print("=" * 50)

def check_system():
    """Kiểm tra hệ thống"""
    print("💻 Kiểm tra hệ thống...")
    
    import platform
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

def run_command(cmd, description, timeout=60):
    """Chạy command với timeout"""
    print(f"\n🔄 {description}...")
    print(f"   Command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        
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

def demo_workflow():
    """Demo toàn bộ workflow"""
    print("\n🚀 Bắt đầu demo workflow...")
    
    # Step 1: Check compatibility
    print("\n📊 Step 1: Kiểm tra tương thích...")
    if not run_command([sys.executable, "check_compatibility.py"], "Compatibility check"):
        print("   ⚠️  Compatibility check failed, tiếp tục...")
    
    # Step 2: Test GUI
    print("\n🧪 Step 2: Test GUI...")
    if not run_command([sys.executable, "quick_gui_test.py"], "GUI test"):
        print("   ❌ GUI test failed")
        return False
    
    # Step 3: Test MPS compatibility
    print("\n🍎 Step 3: Test MPS compatibility...")
    if not run_command([sys.executable, "test_mps_compatibility.py"], "MPS compatibility test"):
        print("   ⚠️  MPS test failed, sẽ sử dụng CPU fallback")
    
    # Step 4: Create test folder
    print("\n📁 Step 4: Tạo test folder...")
    test_folder = "demo_test_folder"
    if not os.path.exists(test_folder):
        os.makedirs(test_folder)
        print(f"   ✅ Created test folder: {test_folder}")
    
    # Step 5: Demo command line
    print("\n💻 Step 5: Demo command line...")
    print("   💡 Command line demo:")
    print("   python3 subedit_optimized.py --gui")
    print("   python3 subedit_cpu.py --gui")
    print("   python3 run_subtitle.py")
    
    # Step 6: Demo GUI
    print("\n🖥️  Step 6: Demo GUI...")
    print("   💡 GUI demo:")
    print("   python3 subtitle_gui.py")
    print("   ./run_gui.sh")
    
    return True

def show_usage_examples():
    """Hiển thị các ví dụ sử dụng"""
    print("\n📋 CÁC CÁCH SỬ DỤNG")
    print("=" * 30)
    
    print("\n🎯 Cách 1: GUI hoàn toàn (Khuyến nghị)")
    print("   ./run_gui.sh")
    print("   python3 subtitle_gui.py")
    
    print("\n🎯 Cách 2: GUI đơn giản")
    print("   python3 run_subtitle.py")
    
    print("\n🎯 Cách 3: Command line với GUI picker")
    print("   python3 subedit_optimized.py --gui")
    
    print("\n🎯 Cách 4: Command line truyền thống")
    print("   python3 subedit_optimized.py /path/to/videos --lang vi --model medium")
    
    print("\n🎯 Cách 5: CPU-only mode")
    print("   python3 subedit_cpu.py --gui")
    print("   python3 subtitle_gui_cpu.py")

def show_troubleshooting():
    """Hiển thị troubleshooting"""
    print("\n🔧 TROUBLESHOOTING")
    print("=" * 30)
    
    print("\n❌ Nếu có lỗi MPS:")
    print("   python3 fix_mps.py")
    print("   python3 force_cpu.py")
    
    print("\n❌ Nếu GUI không hoạt động:")
    print("   python3 quick_gui_test.py")
    print("   python3 test_gui.py")
    
    print("\n❌ Nếu có lỗi dependencies:")
    print("   ./setup.sh")
    print("   pip install -r requirements.txt --force-reinstall")
    
    print("\n❌ Nếu cần giải quyết tất cả vấn đề:")
    print("   python3 solve_all_issues.py")

def main():
    """Main function"""
    print_header()
    
    # Kiểm tra hệ thống
    if not check_system():
        print("\n❌ Script này chỉ dành cho MacBook Apple Silicon")
        return
    
    # Demo workflow
    if demo_workflow():
        print("\n🎉 Demo workflow thành công!")
    else:
        print("\n❌ Demo workflow thất bại")
    
    # Hiển thị usage examples
    show_usage_examples()
    
    # Hiển thị troubleshooting
    show_troubleshooting()
    
    print("\n" + "=" * 50)
    print("🎬 Demo hoàn thành!")
    print("💡 Bây giờ bạn có thể sử dụng Video Subtitle Generator")
    print("=" * 50)

if __name__ == "__main__":
    main()










