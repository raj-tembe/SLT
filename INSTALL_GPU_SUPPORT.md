# Enable GPU Support for RTX 3050 - Complete Guide

## Current Status ❌
```
TensorFlow Version: 2.13.1
GPUs detected: 0 (should be 1)
PyTorch CUDA: False (should be True)
Current FPS: 8 (expected: 20-30+)
```

You have RTX 3050 6GB but CUDA drivers are not installed. Follow these steps to enable GPU support.

---

## Option 1: Quick Fix (Recommended) - 5 minutes

### Step 1: Uninstall current TensorFlow
```bash
pip uninstall tensorflow -y
```

### Step 2: Install TensorFlow with GPU support
```bash
pip install tensorflow[and-cuda]
```

This will:
- Download TensorFlow with CUDA/cuDNN dependencies
- Automatically configure everything
- NO separate CUDA installation needed!

### Step 3: Verify GPU is detected
```bash
python -c "import tensorflow as tf; print('GPUs:', len(tf.config.list_physical_devices('GPU')), 'devices detected')"
```

**Expected output:**
```
GPUs: 1 devices detected
```

### Step 4: Test FPS
```bash
python benchmark_fps.py
```

**Expected FPS**: 20-30+ (compared to 8 now)

---

## Option 2: Manual Installation (If Option 1 fails)

### Prerequisites Check
First, verify your setup:
```bash
# Check GPU
nvidia-smi
```

**Expected output should show your RTX 3050**

If `nvidia-smi` command not found:
1. Download NVIDIA drivers: https://www.nvidia.com/Download/driverDetails.aspx
2. Install latest driver for RTX 3050
3. Reboot
4. Try `nvidia-smi` again

### Step 1: Install CUDA Toolkit 12.1
```bash
# Option A: Using pip (easiest)
pip install nvidia-cuda-toolkit

# Option B: Download from NVIDIA
# https://developer.nvidia.com/cuda-12-1-0-download-archive
```

### Step 2: Install cuDNN
```bash
# Option A: Using pip (easiest)  
pip install nvidia-cudnn

# Option B: Download from NVIDIA
# https://developer.nvidia.com/cudnn
```

### Step 3: Install CUDA-enabled TensorFlow
```bash
pip uninstall tensorflow -y
pip install tensorflow[and-cuda]==2.13.1
```

### Step 4: Verify
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

---

## Option 3: Using Conda (If you use Anaconda)

```bash
# Create new environment with GPU support
conda create -n asl-gpu python=3.11 cuda-core cuda-cudart cudnn tensorflow-gpu

# Activate it
conda activate asl-gpu

# Run app
python app.py
```

---

## Troubleshooting

### Problem: "tensorflow-intel" is blocking GPU
**Solution**:
```bash
pip uninstall tensorflow tensorflow-intel -y
pip install tensorflow[and-cuda]
```

### Problem: CUDA version mismatch
**Solution**: Use compatible versions
```bash
pip install tensorflow[and-cuda]==2.13.1 --force-reinstall
```

### Problem: nvidia-smi not found
**Solution**:
1. Update GPU drivers from NVIDIA website
2. Restart computer
3. Try again

### Problem: Still no GPU after install
**Check**:
```bash
# Detailed TensorFlow info
python -c "import tensorflow as tf; print(tf.sysconfig.get_build_info()['cuda_version'])"

# Check CUDA is installed
nvcc --version

# Check cuDNN
pip show nvidia-cudnn
```

---

## Quick Diagnostic Script

Create file `diagnose_gpu.py`:

```python
import tensorflow as tf
import sys

print("=" * 60)
print("GPU DIAGNOSTIC REPORT")
print("=" * 60)
print()

# Check TensorFlow
print("[TensorFlow]")
print(f"Version: {tf.__version__}")
print(f"Build with CUDA: {'Yes' if tf.test.is_built_with_cuda() else 'No'}")
print()

# Check GPUs
print("[GPU Detection]")
gpus = tf.config.list_physical_devices('GPU')
print(f"GPUs found: {len(gpus)}")
if gpus:
    for gpu in gpus:
        print(f"  - {gpu}")
else:
    print("  ⚠ No GPUs detected!")
print()

# Check CUDA
print("[CUDA Support]")
try:
    print(f"CUDA available: {tf.test.is_built_with_cuda()}")
except:
    print("CUDA check failed")
print()

# Try GPU inference
print("[GPU Inference Test]")
try:
    with tf.device('/GPU:0'):
        a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
        b = tf.constant([[1.0, 2.0], [3.0, 4.0]])
        c = tf.matmul(a, b)
        print(f"✓ GPU inference works!")
        print(f"Result shape: {c.shape}")
except Exception as e:
    print(f"✗ GPU inference failed: {e}")
    print("  This means GPU is not properly set up")

print()
print("=" * 60)

# Recommendations
if len(gpus) == 0:
    print("⚠ RECOMMENDATION: Install CUDA support")
    print("Run: pip install tensorflow[and-cuda]")
elif tf.test.is_built_with_cuda():
    print("✓ GPU is properly configured!")
else:
    print("⚠ GPU detected but CUDA not working")
    print("Try: pip install --upgrade tensorflow[and-cuda]")

print("=" * 60)
```

Run it:
```bash
python diagnose_gpu.py
```

---

## Performance Comparison

After enabling GPU support:

| Metric | CPU Only (Now) | GPU Enabled (Expected) | Improvement |
|--------|--------|--------|-----------|
| FPS | 8 | 25-35 | **+300%** |
| Inference time | ~200ms | ~50ms | **4x faster** |
| GPU usage | 0% | 30-60% | Full |
| Power consumption | Normal | +2-3W | Minor |

---

## RTX 3050 Performance Chart

Your RTX 3050 should achieve:

| Task | FPS | Inference Time |
|------|-----|-----------------|
| MediaPipe detection (640x480) | 120+ FPS | <5ms |
| TensorFlow inference (30 frames) | 50+ FPS | 18-25ms |
| Full pipeline | **25-35 FPS** | ~50ms |

---

## Verify After Installation

1. **Check GPU is detected**:
   ```bash
   python diagnose_gpu.py
   ```
   Should show your RTX 3050

2. **Run benchmark**:
   ```bash
   python benchmark_fps.py
   ```
   Should show 25-35 FPS

3. **Monitor in app**:
   ```bash
   python app.py
   ```
   Terminal should show `[GPU] 1 GPU(s) detected`

---

## If Still Getting Low FPS After GPU Install

Check these:

1. **Is GPU being used?**
   ```bash
   python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
   ```
   Must show `PhysicalDevice(name='/physical_device:GPU:0'...)`

2. **Is laptop thermal throttling?**
   - Run `nvidia-smi` during app execution
   - If temp > 85°C, use cooling pad or lower FRAME_SKIP

3. **Is another app using GPU?**
   - Check Task Manager → GPU tab
   - Close other GPU apps

4. **Are config settings wrong?**
   - Check `src/config.py` for:
   - `FRAME_SKIP = 1` (not higher)
   - `PREDICTION_SKIP = 1` (not higher)
   - `CAMERA_WIDTH/HEIGHT = 640/480` (not lower)

---

## Next Steps

1. **Install**: `pip install tensorflow[and-cuda]`
2. **Verify**: `python diagnose_gpu.py`
3. **Test**: `python benchmark_fps.py`
4. **Run**: `python app.py`

Expected results: **25-35 FPS** ✓

---

## Support

If you're still having issues:

1. Post output of:
   ```bash
   python diagnose_gpu.py
   ```

2. Check NVIDIA driver version:
   ```bash
   nvidia-smi
   ```
   Should be 500+ for RTX 3050

3. Verify Python version:
   ```bash
   python --version
   ```
   Should be 3.8-3.11

---

**Time to install: 5 minutes**  
**Time to GPU-enabled 25-35 FPS: ~10 minutes total** ⚡

Let me know when you've installed and I'll help verify!
