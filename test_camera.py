#!/usr/bin/env python3
"""
Camera Test Script
Tests if camera and MediaPipe are working correctly
"""

import cv2
import mediapipe as mp
import time
import sys

print("=" * 60)
print("Camera & MediaPipe Test")
print("=" * 60)
print()

# Test 1: Camera
print("📷 Testing camera access...")
try:
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        print(f"✓ Camera working! Frame size: {frame.shape}")
        cap.release()
    else:
        print("✗ Camera opened but failed to read frame")
        sys.exit(1)
except Exception as e:
    print(f"✗ Camera error: {e}")
    sys.exit(1)

print()

# Test 2: MediaPipe
print("🤖 Testing MediaPipe Holistic...")
try:
    mp_holistic = mp.solutions.holistic
    holistic = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=0
    )
    print("✓ MediaPipe Holistic initialized")
    holistic.close()
except Exception as e:
    print(f"✗ MediaPipe error: {e}")
    sys.exit(1)

print()

# Test 3: Real-time capture
print("🎬 Testing real-time capture (5 seconds)...")
try:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    holistic = mp_holistic.Holistic(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        model_complexity=0
    )
    
    start_time = time.time()
    frame_count = 0
    
    while time.time() - start_time < 5:
        ret, frame = cap.read()
        if not ret:
            print("⚠ Failed to read frame")
            continue
        
        # Process with MediaPipe
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_rgb.flags.writeable = False
        results = holistic.process(frame_rgb)
        frame_rgb.flags.writeable = True
        
        frame_count += 1
        
        if frame_count % 30 == 0:
            elapsed = time.time() - start_time
            fps = frame_count / elapsed
            print(f"  Frame {frame_count} - FPS: {fps:.1f}")
    
    elapsed = time.time() - start_time
    fps = frame_count / elapsed
    
    print(f"✓ Processed {frame_count} frames in {elapsed:.2f}s")
    print(f"✓ Average FPS: {fps:.1f}")
    
    cap.release()
    holistic.close()
    
except Exception as e:
    print(f"✗ Real-time capture error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print()
print("=" * 60)
print("✓ All tests passed! Camera and MediaPipe are working.")
print("=" * 60)
