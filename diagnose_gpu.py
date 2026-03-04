#!/usr/bin/env python3
"""
GPU Diagnostic Tool - Check if GPU is properly installed
"""

import sys

print("=" * 70)
print("GPU DIAGNOSTIC REPORT")
print("=" * 70)
print()

# Check TensorFlow
print("[1] TensorFlow Configuration")
print("-" * 70)
try:
    import tensorflow as tf
    print(f"Version: {tf.__version__}")
    print(f"Built with CUDA: {'✓ Yes' if tf.test.is_built_with_cuda() else '✗ No'}")
    
    gpus = tf.config.list_physical_devices('GPU')
    print(f"GPUs detected: {len(gpus)}")
    if gpus:
        for i, gpu in enumerate(gpus):
            print(f"  GPU {i}: {gpu.name}")
    else:
        print("  ⚠ No GPUs detected!")
except Exception as e:
    print(f"Error: {e}")

print()

# Check CUDA/cuDNN
print("[2] CUDA & cuDNN")
print("-" * 70)
try:
    print(f"CUDA installed: {'✓ Yes' if tf.test.is_built_with_cuda() else '✗ No'}")
    
    # Try to get CUDA version
    try:
        import nvidia.cuda_runtime.lib as cuda_rt
        print(f"CUDA runtime available: ✓ Yes")
    except:
        print(f"CUDA runtime: Check with 'nvcc --version'")
    
    # Check cuDNN
    try:
        import nvidia.cudnn
        print(f"cuDNN installed: ✓ Yes")
    except:
        print(f"cuDNN: Not installed or not in path")
        
except Exception as e:
    print(f"Error: {e}")

print()

# Test GPU inference
print("[3] GPU Inference Test")
print("-" * 70)
try:
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        with tf.device('/GPU:0'):
            a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
            b = tf.constant([[1.0, 2.0], [3.0, 4.0]])
            c = tf.matmul(a, b)
            print(f"✓ GPU inference works!")
            print(f"  Result: {c.numpy()}")
    else:
        print("✗ No GPU available for testing")
except Exception as e:
    print(f"✗ GPU inference failed: {e}")

print()

# Check PyTorch
print("[4] PyTorch (Optional)")
print("-" * 70)
try:
    import torch
    print(f"Version: {torch.__version__}")
    print(f"CUDA available: {'✓ Yes' if torch.cuda.is_available() else '✗ No'}")
    if torch.cuda.is_available():
        print(f"GPU Name: {torch.cuda.get_device_name(0)}")
        print(f"CUDA Version: {torch.version.cuda}")
except ImportError:
    print("PyTorch not installed (optional)")
except Exception as e:
    print(f"Error: {e}")

print()

# Check nvidia-smi
print("[5] NVIDIA Driver")
print("-" * 70)
try:
    import subprocess
    result = subprocess.run(['nvidia-smi', '-q'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        # Extract GPU info
        lines = result.stdout.split('\n')
        for i, line in enumerate(lines[:20]):
            if 'Product Name' in line or 'CUDA Capability' in line or 'Driver Version' in line:
                print(f"✓ {line.strip()}")
        print("✓ NVIDIA drivers installed")
    else:
        print("✗ nvidia-smi not found - drivers may not be installed")
except FileNotFoundError:
    print("⚠ nvidia-smi not found in PATH")
    print("  Install NVIDIA drivers from https://www.nvidia.com/download/")
except Exception as e:
    print(f"Error checking nvidia-smi: {e}")

print()

# Recommendations
print("[6] Recommendations")
print("=" * 70)

gpus = tf.config.list_physical_devices('GPU')
cuda_available = tf.test.is_built_with_cuda()

if len(gpus) > 0 and cuda_available:
    print("✓ GPU is properly configured!")
    print()
    print("Your system is ready for GPU acceleration.")
    print("Expected FPS: 25-35 with RTX 3050")
    
elif len(gpus) == 0 and not cuda_available:
    print("✗ GPU not available - CUDA not installed")
    print()
    print("Installation steps (copy & paste):")
    print()
    print("  1. Uninstall current TensorFlow:")
    print("     pip uninstall tensorflow -y")
    print()
    print("  2. Install TensorFlow with GPU support:")
    print("     pip install tensorflow[and-cuda]")
    print()
    print("  3. Verify installation:")
    print("     python diagnose_gpu.py")
    print()
    print("This will take 10-15 minutes and download ~5GB")
    
elif len(gpus) == 0 and cuda_available:
    print("⚠ CUDA installed but GPU not detected")
    print()
    print("Try:")
    print("  1. Update TensorFlow:")
    print("     pip install --upgrade tensorflow[and-cuda]")
    print()
    print("  2. Check NVIDIA drivers:")
    print("     nvidia-smi")
    print()
    print("  3. Restart Python and try again")
    
else:
    print("⚠ Unexpected state - Mixed configuration detected")

print()
print("=" * 70)
