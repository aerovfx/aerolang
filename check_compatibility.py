#!/usr/bin/env python3
"""
🔍 Compatibility Check Script
Kiểm tra tương thích PyTorch và MPS cho MacBook Pro M2
"""

import sys
import os

def check_python_version():
    """Kiểm tra phiên bản Python"""
    print("🐍 Kiểm tra Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("   ❌ Python 3.8+ required")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def check_torch_installation():
    """Kiểm tra cài đặt PyTorch"""
    print("\n🔥 Kiểm tra PyTorch...")
    
    try:
        import torch
        print(f"   ✅ PyTorch version: {torch.__version__}")
        
        # Kiểm tra build info
        if hasattr(torch, 'version'):
            print(f"   Build: {torch.version.cuda if torch.version.cuda else 'CPU'}")
        
        return True, torch
    except ImportError:
        print("   ❌ PyTorch not installed")
        return False, None
    except Exception as e:
        print(f"   ❌ Lỗi import PyTorch: {e}")
        return False, None

def check_mps_support(torch):
    """Kiểm tra MPS support"""
    print("\n🍎 Kiểm tra MPS (Apple Silicon) support...")
    
    try:
        # Kiểm tra MPS availability
        mps_available = torch.backends.mps.is_available()
        print(f"   MPS available: {mps_available}")
        
        if mps_available:
            # Kiểm tra MPS device
            try:
                device = torch.device("mps")
                print(f"   MPS device: {device}")
                
                # Test tensor creation
                test_tensor = torch.tensor([1, 2, 3], device=device)
                print(f"   ✅ MPS tensor creation: {test_tensor}")
                
                # Kiểm tra empty_cache
                if hasattr(torch.backends.mps, 'empty_cache'):
                    print("   ✅ MPS empty_cache available")
                    try:
                        torch.backends.mps.empty_cache()
                        print("   ✅ MPS empty_cache working")
                    except Exception as e:
                        print(f"   ⚠️  MPS empty_cache error: {e}")
                else:
                    print("   ⚠️  MPS empty_cache not available")
                
                return True
            except Exception as e:
                print(f"   ❌ MPS device error: {e}")
                return False
        else:
            print("   ⚠️  MPS not available - using CPU")
            return False
            
    except Exception as e:
        print(f"   ❌ MPS check error: {e}")
        return False

def check_cuda_support(torch):
    """Kiểm tra CUDA support"""
    print("\n🖥️  Kiểm tra CUDA support...")
    
    try:
        cuda_available = torch.cuda.is_available()
        print(f"   CUDA available: {cuda_available}")
        
        if cuda_available:
            print(f"   CUDA version: {torch.version.cuda}")
            print(f"   GPU count: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                print(f"   GPU {i}: {torch.cuda.get_device_name(i)}")
            return True
        else:
            print("   ⚠️  CUDA not available")
            return False
            
    except Exception as e:
        print(f"   ❌ CUDA check error: {e}")
        return False

def check_whisper_installation():
    """Kiểm tra cài đặt Whisper"""
    print("\n🎤 Kiểm tra Whisper...")
    
    try:
        import whisper
        print(f"   ✅ Whisper version: {whisper.__version__}")
        
        # Test model loading
        print("   🔄 Testing model loading...")
        model = whisper.load_model("tiny")
        print("   ✅ Whisper model loading OK")
        
        return True
    except ImportError:
        print("   ❌ Whisper not installed")
        return False
    except Exception as e:
        print(f"   ❌ Whisper error: {e}")
        return False

def check_dependencies():
    """Kiểm tra các dependencies khác"""
    print("\n📦 Kiểm tra dependencies...")
    
    dependencies = [
        ("tqdm", "Progress tracking"),
        ("psutil", "System monitoring"),
        ("tkinter", "GUI support")
    ]
    
    all_ok = True
    for dep, desc in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep}: {desc}")
        except ImportError:
            print(f"   ❌ {dep}: {desc} - not installed")
            all_ok = False
    
    return all_ok

def check_system_info():
    """Kiểm tra thông tin hệ thống"""
    print("\n💻 Thông tin hệ thống...")
    
    import platform
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Processor: {platform.processor()}")
    
    # Kiểm tra RAM
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"   RAM: {memory.total / (1024**3):.1f}GB total, {memory.available / (1024**3):.1f}GB available")
    except:
        print("   RAM: Unable to get memory info")

def main():
    """Main function"""
    print("🔍 PyTorch & MPS Compatibility Check")
    print("=" * 50)
    
    # Kiểm tra Python
    if not check_python_version():
        print("\n❌ Python version không tương thích")
        return
    
    # Kiểm tra PyTorch
    torch_ok, torch = check_torch_installation()
    if not torch_ok:
        print("\n❌ PyTorch không được cài đặt đúng cách")
        return
    
    # Kiểm tra MPS
    mps_ok = check_mps_support(torch)
    
    # Kiểm tra CUDA
    cuda_ok = check_cuda_support(torch)
    
    # Kiểm tra Whisper
    whisper_ok = check_whisper_installation()
    
    # Kiểm tra dependencies
    deps_ok = check_dependencies()
    
    # Thông tin hệ thống
    check_system_info()
    
    # Tổng kết
    print("\n" + "=" * 50)
    print("📊 TỔNG KẾT")
    print("=" * 50)
    
    print(f"Python: {'✅' if check_python_version() else '❌'}")
    print(f"PyTorch: {'✅' if torch_ok else '❌'}")
    print(f"MPS: {'✅' if mps_ok else '❌'}")
    print(f"CUDA: {'✅' if cuda_ok else '❌'}")
    print(f"Whisper: {'✅' if whisper_ok else '❌'}")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    
    if torch_ok and whisper_ok:
        print("\n🎉 Hệ thống sẵn sàng để chạy Video Subtitle Generator!")
        
        if mps_ok:
            print("🍎 Apple Silicon MPS support: ✅")
            print("💡 Khuyến nghị: Sử dụng MPS cho hiệu suất tốt nhất")
        elif cuda_ok:
            print("🖥️  CUDA support: ✅")
            print("💡 Khuyến nghị: Sử dụng CUDA cho hiệu suất tốt nhất")
        else:
            print("💻 CPU mode: ✅")
            print("💡 Khuyến nghị: Cài đặt PyTorch với MPS support cho MacBook Pro M2")
    else:
        print("\n❌ Cần cài đặt thêm dependencies")
        print("💡 Chạy: ./setup.sh")

if __name__ == "__main__":
    main()




