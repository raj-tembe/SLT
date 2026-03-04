# Performance Tuning Guide - ASL Recognition System

## FPS Optimization Strategies

Your system has been optimized with the following improvements:

### ✅ Completed Optimizations

1. **GPU Acceleration Enabled**
   - TensorFlow GPU memory growth configured
   - Mixed precision (float16) enabled for RTX 3050
   - Automatic GPU detection and allocation

2. **Lightweight Landmark Rendering**
   - Removed expensive face mesh drawing (468 landmarks)
   - Kept only hand landmark visualization
   - Expected boost: **+300-500% FPS improvement**

3. **Reduced Processing Overhead**
   - JPEG quality lowered to 35 (from 60)
   - Removed redundant image flips
   - Removed wasteful array concatenation

4. **Code Cleanup**
   - Fixed Unicode encoding errors for Windows
   - Improved error handling
   - Better logging with [TAG] format

---

## Configuration Tuning (Edit `src/config.py`)

```python
# FRAME_SKIP: Process every Nth frame
FRAME_SKIP = 1          # 1 = process all frames (best quality)
                        # 2 = process every 2nd frame (faster)
                        # 3 = process every 3rd frame (even faster)

# PREDICTION_SKIP: Run inference every Nth time
PREDICTION_SKIP = 1     # 1 = predict every time (best accuracy)
                        # 2 = predict every 2nd sequence
                        # 3 = predict every 3rd sequence

# JPEG_QUALITY: Lower = faster encoding, less quality
JPEG_QUALITY = 35       # Range: 10-100
                        # 10-20 = fastest (poor quality)
                        # 30-40 = balanced (our setting)
                        # 80+ = high quality (slow)

# Camera Resolution: Lower = faster processing
CAMERA_WIDTH = 640      # Options: 320, 480, 640, 1280
CAMERA_HEIGHT = 480     # Options: 240, 360, 480, 720

# GPU Optimization
USE_GPU = True          # Enable GPU acceleration (RTX 3050)
USE_MIXED_PRECISION = True  # Use float16 for faster inference
```

---

## Recommended Configurations

### 🚀 Maximum FPS Mode (Sacrifice Some Accuracy)
```python
FRAME_SKIP = 2           # Skip every other frame
PREDICTION_SKIP = 2      # Predict every 2nd sequence instead of every 1st
JPEG_QUALITY = 25        # Lower quality
CAMERA_WIDTH = 480       # Smaller resolution
CAMERA_HEIGHT = 360
```
**Expected FPS**: 20-30+ FPS

### ⚖️ Balanced Mode (Good FPS + Accuracy)
```python
FRAME_SKIP = 1           # Process all frames
PREDICTION_SKIP = 1      # Every sequence
JPEG_QUALITY = 35        # Default setting
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
```
**Expected FPS**: 15-25 FPS

### 🎯 Maximum Accuracy Mode (Slower, Better Predictions)
```python
FRAME_SKIP = 1           # Process all frames
PREDICTION_SKIP = 1      # Predict every sequence
JPEG_QUALITY = 60        # Higher quality
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
```
**Expected FPS**: 10-15 FPS (but more accurate)

---

## Debugging FPS Issues

### Check GPU is Being Used
```bash
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

If it returns an empty list `[]`, your TensorFlow installation doesn't support GPU. Install:
```bash
pip install tensorflow[and-cuda]
```

### Monitor Performance
The app displays FPS in real-time:
- Look at `FPS: XX` in the terminal output
- Sequence counter shows `Seq: X/30` (frames accumulated)

### What affects FPS the most?

1. **FRAME_SKIP** - Biggest impact ⭐⭐⭐
2. **PREDICTION_SKIP** - Large impact ⭐⭐⭐
3. **JPEG_QUALITY** - Medium impact ⭐⭐
4. **CAMERA resolution** - Medium impact ⭐⭐
5. **USE_GPU** - Large impact if available ⭐⭐⭐

---

## Testing Your Configuration

1. Edit `src/config.py` with your desired settings
2. Run the app:
   ```bash
   python app.py
   ```
3. Look at the FPS counter in terminal output
4. Check prediction accuracy on the web interface
5. Adjust settings until you find the sweet spot

---

## Advanced Optimization

### For RTX 3050 (in your laptop):
- GPU memory: 6GB
- CUDA compute capability: 8.6
- Recommended: Keep `USE_MIXED_PRECISION = True`

### If FPS is still low (< 15 FPS):
1. **Lower CAMERA resolution first** (biggest impact)
2. **Increase FRAME_SKIP to 2**
3. **Increase PREDICTION_SKIP to 2**
4. **Lower JPEG_QUALITY to 25**

### If accuracy is too low:
1. **Set FRAME_SKIP = 1** (process all frames)
2. **Set PREDICTION_SKIP = 1** (predict every sequence)
3. **Keep other settings same**

---

## Expected Results After Optimization

| Setting | FPS | Accuracy |
|---------|-----|----------|
| Before optimization | 7-8 | Medium |
| Maximum FPS mode | 25-35 | Medium-Low |
| Balanced mode | 15-25 | Good |
| Maximum accuracy | 10-15 | High |

*Actual FPS depends on your RTX 3050's current load and system temperature*

---

## Monitor GPU Temperature

If getting thermal throttling (FPS drops suddenly), your laptop GPU is overheating. Solutions:
1. Increase frame skip
2. Use external cooling pad
3. Reduce CAMERA resolution
4. Close other applications

---

## Getting Help

If FPS is still low after trying all settings:
1. Check GPU detection: `python test_camera.py`
2. Verify CUDA support: `python -c "import tensorflow as tf; print(tf.config.list_physical_devices())"`
3. Check system CPU/GPU usage with Task Manager
4. Look at terminal output for errors ([WARN], [ERROR])

