#!/usr/bin/env python3
"""
🔧 Fix MPS Script
Sửa lỗi MPS và cài đặt lại PyTorch cho Apple Silicon M2
"""

import os
import sys
import subprocess
import platform

def check_system():
    """Kiểm tra hệ thống"""
    print("💻 Kiểm tra hệ thống...")
    
    system = platform.system()
    machine = platform.machine()
    
    print(f"   OS: {system}")
    print(f"   Architecture: {machine}")
    
    if system == "Darwin" and machine == "arm64":
        print("   ✅ MacBook với Apple Silicon detected")
        return True
    else:
        print("   ⚠️  Không phải MacBook Apple Silicon")
        return False

def uninstall_torch():
    """Gỡ cài đặt PyTorch hiện tại"""
    print("\n🗑️  Gỡ cài đặt PyTorch hiện tại...")
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "torch", "torchaudio", "-y"], 
                      check=True, capture_output=True)
        print("   ✅ Đã gỡ cài đặt PyTorch")
    except subprocess.CalledProcessError as e:
        print(f"   ⚠️  Lỗi gỡ cài đặt: {e}")

def install_torch_mps():
    """Cài đặt PyTorch với MPS support"""
    print("\n🔥 Cài đặt PyTorch với MPS support...")
    
    try:
        # Cài đặt nightly build cho MPS support tốt nhất
        cmd = [
            sys.executable, "-m", "pip", "install", 
            "--pre", "torch", "torchaudio", 
            "--index-url", "https://download.pytorch.org/whl/nightly/cpu"
        ]
        
        print(f"   Chạy: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("   ✅ Cài đặt PyTorch thành công")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Lỗi cài đặt: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def test_mps():
    """Test MPS functionality"""
    print("\n🧪 Test MPS functionality...")
    
    try:
        import torch
        
        # Test MPS availability
        mps_available = torch.backends.mps.is_available()
        print(f"   MPS available: {mps_available}")
        
        if mps_available:
            # Test device creation
            device = torch.device("mps")
            print(f"   MPS device: {device}")
            
            # Test tensor creation
            test_tensor = torch.tensor([1, 2, 3], device=device)
            print(f"   ✅ MPS tensor: {test_tensor}")
            
            # Test empty_cache
            if hasattr(torch.backends.mps, 'empty_cache'):
                torch.backends.mps.empty_cache()
                print("   ✅ MPS empty_cache working")
            else:
                print("   ⚠️  MPS empty_cache not available")
            
            return True
        else:
            print("   ❌ MPS not available")
            return False
            
    except Exception as e:
        print(f"   ❌ MPS test error: {e}")
        return False

def set_environment_variables():
    """Thiết lập environment variables"""
    print("\n🔧 Thiết lập environment variables...")
    
    # Suppress Tk deprecation warning
    os.environ['TK_SILENCE_DEPRECATION'] = '1'
    print("   ✅ Set TK_SILENCE_DEPRECATION=1")
    
    # PyTorch environment variables
    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
    print("   ✅ Set PYTORCH_ENABLE_MPS_FALLBACK=1")

def create_fix_script():
    """Tạo script fix tự động"""
    print("\n📝 Tạo script fix tự động...")
    
    script_content = '''#!/bin/bash
# Auto-fix script for MPS issues

export TK_SILENCE_DEPRECATION=1
export PYTORCH_ENABLE_MPS_FALLBACK=1

echo "🔧 Running auto-fix for MPS..."
python3 fix_mps.py

echo "✅ Fix completed!"
'''
    
    with open("auto_fix.sh", "w") as f:
        f.write(script_content)
    
    os.chmod("auto_fix.sh", 0o755)
    print("   ✅ Created auto_fix.sh")

def main():
    """Main function"""
    print("🔧 MPS Fix Script for MacBook Pro M2")
    print("=" * 50)
    
    # Kiểm tra hệ thống
    if not check_system():
        print("\n❌ Script này chỉ dành cho MacBook Apple Silicon")
        return
    
    # Thiết lập environment variables
    set_environment_variables()
    
    # Gỡ cài đặt PyTorch cũ
    uninstall_torch()
    
    # Cài đặt PyTorch mới
    if not install_torch_mps():
        print("\n❌ Không thể cài đặt PyTorch")
        return
    
    # Test MPS
    if test_mps():
        print("\n🎉 MPS fix thành công!")
        print("💡 Bây giờ bạn có thể chạy Video Subtitle Generator")
    else:
        print("\n⚠️  MPS vẫn có vấn đề, thử cài đặt lại...")
        
        # Thử cài đặt stable version
        print("\n🔄 Thử cài đặt stable version...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "torch", "torchaudio", 
                "--index-url", "https://download.pytorch.org/whl/cpu"
            ], check=True)
            
            if test_mps():
                print("\n✅ MPS working với stable version")
            else:
                print("\n❌ MPS vẫn không hoạt động")
        except Exception as e:
            print(f"\n❌ Lỗi cài đặt stable version: {e}")
    
    # Tạo script fix tự động
    create_fix_script()
    
    print("\n📋 Hướng dẫn sử dụng:")
    print("1. Chạy: python3 check_compatibility.py")
    print("2. Chạy: python3 subedit_optimized.py --gui")
    print("3. Hoặc: ./auto_fix.sh")

if __name__ == "__main__":
    main()




