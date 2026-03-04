#!/usr/bin/env python3
"""
Quick FPS Test Script
Tests actual FPS performance with MediaPipe and TensorFlow
Run this to benchmark your system before/after optimizations
"""

import time
import cv2
import numpy as np
import mediapipe as mp
from src.backbone import TFLiteModel, get_model
from src.landmarks_extraction import mediapipe_detection, extract_coordinates
from src.config import SEQ_LEN, CAMERA_WIDTH, CAMERA_HEIGHT, FRAME_SKIP, PREDICTION_SKIP
import sys

print("=" * 70)
print("ASL RECOGNITION - FPS BENCHMARK TEST")
print("=" * 70)
print()

# Show configuration
print("[CONFIG]")
print(f"  Camera Resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
print(f"  Frame Skip: {FRAME_SKIP}")
print(f"  Prediction Skip: {PREDICTION_SKIP}")
print()

# Initialize
print("[INIT] Loading MediaPipe...")
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    model_complexity=0
)
print("[OK] MediaPipe loaded")

print("[INIT] Loading TensorFlow model...")
models = [get_model() for _ in ['./models/FINAL_ASL_250.h5']]
models[0].load_weights('./models/FINAL_ASL_250.h5')
tflite_model = TFLiteModel(islr_models=models)
print("[OK] Model loaded")

print("[INIT] Starting camera...")
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("[ERROR] Camera not available!")
    sys.exit(1)

print("[OK] Camera started")
print()

# Run benchmark
print("[TEST] Running 10-second benchmark...")
print()

start_time = time.time()
frame_count = 0
detection_count = 0
detection_time = 0
inference_count = 0
inference_time = 0
sequence_data = []
frame_idx = 0

try:
    while time.time() - start_time < 10:
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame_idx += 1
        frame_count += 1
        
        # MediaPipe detection (every FRAME_SKIP frames)
        if frame_idx % FRAME_SKIP == 0:
            start_det = time.time()
            image, results = mediapipe_detection(frame, holistic)
            detection_count += 1
            detection_time += time.time() - start_det
            
            # Extract landmarks
            try:
                if results and results.face_landmarks:
                    landmarks = extract_coordinates(results)
                else:
                    landmarks = np.zeros((468 + 21 + 33 + 21, 3))
                sequence_data.append(landmarks)
            except:
                sequence_data.append(np.zeros((468 + 21 + 33 + 21, 3)))
        
        # Inference (every SEQ_LEN * PREDICTION_SKIP frames)
        if len(sequence_data) >= SEQ_LEN and frame_count % (SEQ_LEN * PREDICTION_SKIP) == 0:
            try:
                start_inf = time.time()
                seq = np.array(sequence_data[-SEQ_LEN:], dtype=np.float32)
                pred = tflite_model(seq)["outputs"]
                inference_count += 1
                inference_time += time.time() - start_inf
                sequence_data = sequence_data[SEQ_LEN//2:]
            except:
                pass

except KeyboardInterrupt:
    print("\n[STOP] User interrupted")
except Exception as e:
    print(f"\n[ERROR] {e}")
finally:
    cap.release()
    holistic.close()

elapsed = time.time() - start_time

print("[RESULTS]")
print()
print(f"Total time: {elapsed:.2f}s")
print(f"Frames captured: {frame_count}")
print(f"Overall FPS: {frame_count/elapsed:.1f}")
print()
print(f"MediaPipe detections: {detection_count}")
print(f"Detection avg time: {(detection_time/detection_count)*1000:.2f}ms")
print(f"Detection FPS: {detection_count/elapsed:.1f}")
print()
print(f"Inferences: {inference_count}")
if inference_count > 0:
    print(f"Inference avg time: {(inference_time/inference_count)*1000:.2f}ms")
    print(f"Inference FPS: {inference_count/elapsed:.1f}")
print()

# Recommendations
print("[RECOMMENDATIONS]")
overall_fps = frame_count / elapsed

if overall_fps >= 25:
    print("✓ Excellent! Your FPS is very good.")
    print("  You can increase accuracy by:")
    print("  - Setting FRAME_SKIP = 1")
    print("  - Setting PREDICTION_SKIP = 1")
elif overall_fps >= 18:
    print("✓ Good! Your FPS is acceptable.")
    print("  Current settings are well balanced.")
elif overall_fps >= 12:
    print("⚠ Fair. You can improve FPS by:")
    print("  - Increasing FRAME_SKIP to 2 or 3")
    print("  - Increasing PREDICTION_SKIP to 2")
    print("  - Lowering CAMERA resolution")
else:
    print("⚠ Low FPS detected. Try:")
    print("  - Increasing FRAME_SKIP to 2-3")
    print("  - Increasing PREDICTION_SKIP to 2-3")
    print("  - Lowering CAMERA_WIDTH/HEIGHT to 480x360")
    print("  - Lowering JPEG_QUALITY to 25")
    print("  - Check GPU is being used (not CPU)")

print()
print("=" * 70)
print("Edit src/config.py to adjust settings and test again")
print("=" * 70)
