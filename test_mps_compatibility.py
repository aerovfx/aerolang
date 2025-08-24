#!/usr/bin/env python3
"""
🧪 MPS Compatibility Test
Test MPS compatibility với Whisper models
"""

import os
import sys
import torch
import whisper
import time

def test_mps_basic():
    """Test MPS basic functionality"""
    print("🧪 Testing MPS basic functionality...")
    
    try:
        # Test MPS availability
        mps_available = torch.backends.mps.is_available()
        print(f"   MPS available: {mps_available}")
        
        if not mps_available:
            print("   ❌ MPS not available")
            return False
        
        # Test device creation
        device = torch.device("mps")
        print(f"   MPS device: {device}")
        
        # Test basic tensor operations
        test_tensor = torch.tensor([1, 2, 3], device=device)
        print(f"   ✅ Basic tensor: {test_tensor}")
        
        # Test matrix operations
        matrix = torch.randn(3, 3, device=device)
        result = torch.mm(matrix, matrix)
        print(f"   ✅ Matrix multiplication: {result.shape}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ MPS basic test failed: {e}")
        return False

def test_whisper_mps():
    """Test Whisper với MPS"""
    print("\n🧪 Testing Whisper với MPS...")
    
    try:
        # Load tiny model với MPS
        print("   Loading tiny model với MPS...")
        model = whisper.load_model("tiny", device="mps")
        print("   ✅ Model loaded với MPS")
        
        # Test model properties
        print(f"   Model device: {next(model.parameters()).device}")
        print(f"   Model dtype: {next(model.parameters()).dtype}")
        
        # Test transcribe với dummy audio (nếu có)
        print("   Testing transcribe...")
        
        # Tạo dummy audio tensor
        dummy_audio = torch.randn(16000, device="mps")  # 1 second at 16kHz
        
        # Test transcribe
        result = model.transcribe(dummy_audio, fp16=False, verbose=False)
        print("   ✅ Transcribe test successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Whisper MPS test failed: {e}")
        return False

def test_whisper_cpu_fallback():
    """Test Whisper với CPU fallback"""
    print("\n🧪 Testing Whisper với CPU fallback...")
    
    try:
        # Load tiny model với CPU
        print("   Loading tiny model với CPU...")
        model = whisper.load_model("tiny", device="cpu")
        print("   ✅ Model loaded với CPU")
        
        # Test transcribe
        dummy_audio = torch.randn(16000, device="cpu")
        result = model.transcribe(dummy_audio, fp16=False, verbose=False)
        print("   ✅ CPU transcribe test successful")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Whisper CPU test failed: {e}")
        return False

def test_model_sizes():
    """Test các model sizes khác nhau"""
    print("\n🧪 Testing different model sizes...")
    
    model_sizes = ["tiny", "base", "small"]
    
    for size in model_sizes:
        print(f"   Testing {size} model...")
        try:
            # Test với CPU trước
            model = whisper.load_model(size, device="cpu")
            print(f"   ✅ {size} model loaded với CPU")
            
            # Test với MPS nếu có thể
            try:
                model_mps = whisper.load_model(size, device="mps")
                print(f"   ✅ {size} model loaded với MPS")
            except Exception as e:
                print(f"   ⚠️  {size} model MPS failed: {e}")
                
        except Exception as e:
            print(f"   ❌ {size} model failed: {e}")

def benchmark_performance():
    """Benchmark performance"""
    print("\n📊 Performance benchmark...")
    
    # Test CPU performance
    print("   Testing CPU performance...")
    start_time = time.time()
    model_cpu = whisper.load_model("tiny", device="cpu")
    cpu_load_time = time.time() - start_time
    print(f"   CPU load time: {cpu_load_time:.2f}s")
    
    # Test MPS performance nếu có thể
    if torch.backends.mps.is_available():
        print("   Testing MPS performance...")
        start_time = time.time()
        try:
            model_mps = whisper.load_model("tiny", device="mps")
            mps_load_time = time.time() - start_time
            print(f"   MPS load time: {mps_load_time:.2f}s")
            
            if mps_load_time < cpu_load_time:
                print("   ✅ MPS faster than CPU")
            else:
                print("   ⚠️  CPU faster than MPS")
                
        except Exception as e:
            print(f"   ❌ MPS benchmark failed: {e}")

def main():
    """Main function"""
    print("🧪 MPS Compatibility Test Suite")
    print("=" * 50)
    
    # Test 1: Basic MPS
    mps_basic = test_mps_basic()
    
    # Test 2: Whisper MPS
    whisper_mps = False
    if mps_basic:
        whisper_mps = test_whisper_mps()
    
    # Test 3: Whisper CPU
    whisper_cpu = test_whisper_cpu_fallback()
    
    # Test 4: Model sizes
    test_model_sizes()
    
    # Test 5: Performance
    benchmark_performance()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    print(f"MPS Basic: {'✅' if mps_basic else '❌'}")
    print(f"Whisper MPS: {'✅' if whisper_mps else '❌'}")
    print(f"Whisper CPU: {'✅' if whisper_cpu else '❌'}")
    
    if whisper_mps:
        print("\n🎉 MPS fully compatible!")
        print("💡 Sử dụng MPS cho hiệu suất tốt nhất")
    elif whisper_cpu:
        print("\n⚠️  MPS có vấn đề, sử dụng CPU fallback")
        print("💡 Code sẽ tự động fallback về CPU")
    else:
        print("\n❌ Cả MPS và CPU đều có vấn đề")
        print("💡 Kiểm tra cài đặt PyTorch và Whisper")

if __name__ == "__main__":
    main()




