#!/usr/bin/env python3
"""
🧪 Quick Test for MacBook Pro M2
Test nhanh cho subtitle generator
"""

import os
import sys
import time
import subprocess

def test_imports():
    """Test imports"""
    print("🔍 Testing imports...")
    
    try:
        import torch
        print(f"   ✅ PyTorch: {torch.__version__}")
    except ImportError as e:
        print(f"   ❌ PyTorch: {e}")
        return False
    
    try:
        import whisper
        print(f"   ✅ Whisper: {whisper.__version__}")
    except ImportError as e:
        print(f"   ❌ Whisper: {e}")
        return False
    
    try:
        import psutil
        print("   ✅ psutil")
    except ImportError as e:
        print(f"   ❌ psutil: {e}")
        return False
    
    return True

def test_mps():
    """Test MPS availability"""
    print("🔍 Testing MPS...")
    
    try:
        import torch
        
        if torch.backends.mps.is_available():
            print("   ✅ MPS available")
            
            # Test basic MPS operations
            try:
                device = torch.device("mps")
                x = torch.randn(3, 3, device=device)
                y = x + x
                print("   ✅ MPS operations working")
                return True
            except Exception as e:
                print(f"   ⚠️ MPS operations failed: {e}")
                return False
        else:
            print("   ⚠️ MPS not available")
            return False
            
    except Exception as e:
        print(f"   ❌ MPS test error: {e}")
        return False

def test_whisper_model():
    """Test Whisper model loading"""
    print("🔍 Testing Whisper model...")
    
    try:
        import whisper
        
        # Test tiny model
        print("   📦 Loading tiny model...")
        start_time = time.time()
        model = whisper.load_model("tiny")
        load_time = time.time() - start_time
        
        print(f"   ✅ Model loaded in {load_time:.2f}s")
        
        # Test device
        device = next(model.parameters()).device
        print(f"   📱 Model device: {device}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Model test error: {e}")
        return False

def test_subtitle_generator():
    """Test subtitle generator"""
    print("🔍 Testing subtitle generator...")
    
    try:
        from subtitle_m2_optimized import M2SubtitleGenerator
        
        # Create generator
        generator = M2SubtitleGenerator(model_size="tiny", max_workers=1)
        print("   ✅ Generator created")
        
        # Test device setup
        print(f"   📱 Device: {generator.device}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Generator test error: {e}")
        return False

def test_file_creation():
    """Test file creation"""
    print("🔍 Testing file creation...")
    
    try:
        # Create test files
        test_txt = "test_output.txt"
        test_srt = "test_output.srt"
        
        # Test TXT creation
        with open(test_txt, "w", encoding="utf-8") as f:
            f.write("Test content")
        print("   ✅ TXT file creation")
        
        # Test SRT creation
        with open(test_srt, "w", encoding="utf-8") as f:
            f.write("1\n00:00:00,000 --> 00:00:03,500\nTest subtitle\n\n")
        print("   ✅ SRT file creation")
        
        # Cleanup
        os.remove(test_txt)
        os.remove(test_srt)
        print("   🗑️ Test files cleaned up")
        
        return True
        
    except Exception as e:
        print(f"   ❌ File creation error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 MacBook Pro M2 Quick Test")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("MPS", test_mps),
        ("Whisper Model", test_whisper_model),
        ("Subtitle Generator", test_subtitle_generator),
        ("File Creation", test_file_creation)
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
        print("🎉 All tests passed! System is ready.")
        print("\n💡 Try running:")
        print("   python3 run_subtitle.py")
    else:
        print("⚠️ Some tests failed. Check the issues above.")
        
        if passed < 3:
            print("\n🔧 Suggested fixes:")
            print("   1. Run: ./setup_m2.sh")
            print("   2. Activate virtual environment: source venv/bin/activate")
            print("   3. Reinstall dependencies: pip install torch whisper psutil")

if __name__ == "__main__":
    main()










