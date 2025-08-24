#!/usr/bin/env python3
"""
💻 Force CPU Script
Force sử dụng CPU thay vì MPS để tránh lỗi
"""

import os
import sys
import subprocess

def set_cpu_environment():
    """Thiết lập environment để force CPU"""
    print("💻 Thiết lập environment để force CPU...")
    
    # Set environment variables
    os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
    os.environ['FORCE_CUDA'] = '0'
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    
    # Disable MPS
    os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'
    
    print("✅ Environment variables set")

def create_cpu_wrapper():
    """Tạo wrapper script để force CPU"""
    print("\n📝 Tạo CPU wrapper script...")
    
    wrapper_content = '''#!/usr/bin/env python3
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
'''
    
    with open("subedit_cpu.py", "w") as f:
        f.write(wrapper_content)
    
    os.chmod("subedit_cpu.py", 0o755)
    print("✅ Created subedit_cpu.py")

def create_cpu_gui_wrapper():
    """Tạo GUI wrapper cho CPU"""
    print("\n📝 Tạo CPU GUI wrapper...")
    
    gui_wrapper_content = '''#!/usr/bin/env python3
"""
💻 CPU GUI Wrapper
Force sử dụng CPU cho GUI version
"""

import os
import sys

# Force CPU environment
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['FORCE_CUDA'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

# Import và chạy GUI
if __name__ == "__main__":
    from subtitle_gui import main
    main()
'''
    
    with open("subtitle_gui_cpu.py", "w") as f:
        f.write(gui_wrapper_content)
    
    os.chmod("subtitle_gui_cpu.py", 0o755)
    print("✅ Created subtitle_gui_cpu.py")

def modify_main_script():
    """Sửa đổi main script để force CPU"""
    print("\n🔧 Sửa đổi main script để force CPU...")
    
    try:
        with open("subedit_optimized.py", "r") as f:
            content = f.read()
        
        # Thêm environment variables ở đầu file
        env_vars = '''import os
# Force CPU environment
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'
os.environ['FORCE_CUDA'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['PYTORCH_MPS_HIGH_WATERMARK_RATIO'] = '0.0'

'''
        
        # Tìm vị trí import đầu tiên
        import_pos = content.find("import os")
        if import_pos != -1:
            # Thay thế import os
            new_content = content[:import_pos] + env_vars + content[import_pos:]
        else:
            # Thêm vào đầu file
            new_content = env_vars + content
        
        with open("subedit_optimized_cpu.py", "w") as f:
            f.write(new_content)
        
        os.chmod("subedit_optimized_cpu.py", 0o755)
        print("✅ Created subedit_optimized_cpu.py")
        
    except Exception as e:
        print(f"❌ Error modifying script: {e}")

def test_cpu_mode():
    """Test CPU mode"""
    print("\n🧪 Testing CPU mode...")
    
    try:
        # Set environment
        set_cpu_environment()
        
        # Test import
        import torch
        print(f"   PyTorch version: {torch.__version__}")
        
        # Test device
        device = torch.device("cpu")
        print(f"   Using device: {device}")
        
        # Test tensor
        test_tensor = torch.tensor([1, 2, 3], device=device)
        print(f"   ✅ CPU tensor: {test_tensor}")
        
        # Test Whisper
        import whisper
        model = whisper.load_model("tiny", device="cpu")
        print("   ✅ Whisper CPU model loaded")
        
        return True
        
    except Exception as e:
        print(f"   ❌ CPU test failed: {e}")
        return False

def main():
    """Main function"""
    print("💻 Force CPU Script")
    print("=" * 40)
    
    # Test CPU mode
    if test_cpu_mode():
        print("\n✅ CPU mode working")
        
        # Tạo wrapper scripts
        create_cpu_wrapper()
        create_cpu_gui_wrapper()
        modify_main_script()
        
        print("\n📋 Cách sử dụng CPU mode:")
        print("1. Command line: python3 subedit_cpu.py --gui")
        print("2. GUI: python3 subtitle_gui_cpu.py")
        print("3. Modified: python3 subedit_optimized_cpu.py --gui")
        
        print("\n💡 Hoặc set environment variables trước khi chạy:")
        print("export PYTORCH_ENABLE_MPS_FALLBACK=1")
        print("export FORCE_CUDA=0")
        print("python3 subedit_optimized.py --gui")
        
    else:
        print("\n❌ CPU mode có vấn đề")

if __name__ == "__main__":
    main()




