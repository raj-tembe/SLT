# Quick Config Presets

Use these preset configurations to quickly switch between performance modes.

## 1. Maximum FPS Mode

Edit your `src/config.py` and update these lines:

```python
# =========== PERFORMANCE OPTIMIZATION ===========
FRAME_SKIP = 2
PREDICTION_SKIP = 2
USE_GPU = True
USE_MIXED_PRECISION = True
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 360
JPEG_QUALITY = 25
```

**Expected Results:**
- FPS: 25-35 FPS
- Accuracy: Medium (good for real-time but may miss some signs)
- Best for: Live demos, performance testing

---

## 2. Balanced Mode (Recommended)

Edit your `src/config.py` and update these lines:

```python
# =========== PERFORMANCE OPTIMIZATION ===========
FRAME_SKIP = 1
PREDICTION_SKIP = 1
USE_GPU = True
USE_MIXED_PRECISION = True
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
JPEG_QUALITY = 35
```

**Expected Results:**
- FPS: 15-25 FPS
- Accuracy: Good
- Best for: General use, balanced performance

---

## 3. Maximum Accuracy Mode

Edit your `src/config.py` and update these lines:

```python
# =========== PERFORMANCE OPTIMIZATION ===========
FRAME_SKIP = 1
PREDICTION_SKIP = 1
USE_GPU = True
USE_MIXED_PRECISION = True
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
JPEG_QUALITY = 60
```

**Expected Results:**
- FPS: 10-15 FPS
- Accuracy: Very Good (higher quality video)
- Best for: Training, improving accuracy

---

## 4. Ultra Speed Mode (Extreme)

Edit your `src/config.py` and update these lines:

```python
# =========== PERFORMANCE OPTIMIZATION ===========
FRAME_SKIP = 3
PREDICTION_SKIP = 3
USE_GPU = True
USE_MIXED_PRECISION = True
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
JPEG_QUALITY = 15
```

**Expected Results:**
- FPS: 40-50+ FPS
- Accuracy: Low (sparse predictions)
- Best for: Testing camera, pure FPS benchmarking

---

## 5. CPU Mode (No GPU)

If your GPU is unavailable or not working:

```python
# =========== PERFORMANCE OPTIMIZATION ===========
FRAME_SKIP = 2
PREDICTION_SKIP = 2
USE_GPU = False
USE_MIXED_PRECISION = False
CAMERA_WIDTH = 480
CAMERA_HEIGHT = 360
JPEG_QUALITY = 25
```

**Expected Results:**
- FPS: 8-12 FPS
- Accuracy: Good
- Best for: When GPU unavailable

---

## How to Apply Presets

1. Open `src/config.py`
2. Find the `# =========== PERFORMANCE OPTIMIZATION ===========` section (around line 11-23)
3. Replace those 8 lines with your chosen preset
4. Save the file
5. Run your app:
   ```bash
   python app.py
   ```

---

## Comparison Table

| Mode | FPS | Accuracy | Resolution | FRAME_SKIP | PREDICTION_SKIP | JPEG_Q |
|------|-----|----------|------------|-----------|-----------------|--------|
| Ultra Speed | 40-50+ | Low | 320x240 | 3 | 3 | 15 |
| Max FPS | 25-35 | Medium | 480x360 | 2 | 2 | 25 |
| **Balanced** | 15-25 | Good | 640x480 | 1 | 1 | 35 |
| Max Accuracy | 10-15 | Very Good | 640x480 | 1 | 1 | 60 |
| CPU Mode | 8-12 | Good | 480x360 | 2 | 2 | 25 |

---

## Fine Tuning

### If FPS is too low:
1. Try the next "faster" preset
2. OR increase FRAME_SKIP by 1
3. OR decrease CAMERA resolution
4. OR decrease JPEG_QUALITY by 10

### If accuracy is too low:
1. Try the next "slower" preset
2. OR decrease FRAME_SKIP to 1
3. OR decrease PREDICTION_SKIP to 1
4. OR increase CAMERA resolution
5. OR increase JPEG_QUALITY by 10

---

## Which Preset to Use?

**Choose based on your priority:**

- 🚀 **Max FPS** → Gaming/Real-time demos
- ⚖️ **Balanced** → Production use (recommended)
- 🎯 **Max Accuracy** → Improving accuracy
- 🪫 **CPU Mode** → When GPU unavailable
- 💨 **Ultra Speed** → Testing/Benchmarking

---

## Test Each Preset

After applying a preset, run the benchmark:

```bash
python benchmark_fps.py
```

It will test for 10 seconds and give you the actual FPS and recommendations.

---

## Your RTX 3050 (6GB)

With your RTX 3050 6GB GPU, you should achieve:
- **Balanced mode**: 18-25 FPS ✓ (recommended)
- **Max FPS mode**: 25-35 FPS (possible)
- **Max Accuracy**: 12-18 FPS

If you're getting lower FPS, check:
1. Is GPU being used? (See PERFORMANCE_TUNING.md)
2. Is laptop too hot? (thermal throttling)
3. Are other apps using GPU? (close them)

