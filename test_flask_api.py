#!/usr/bin/env python3
"""
Flask API Test Script
Tests if Flask endpoints are responding
"""

import requests
import time
import sys
import json

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("Flask API Test")
print("=" * 60)
print()

# Test 1: Health check
print("🏥 Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Health check passed")
        print(f"  Status: {data.get('status')}")
        print(f"  Running: {data.get('running')}")
        print(f"  FPS: {data.get('fps')}")
    else:
        print(f"✗ Health check failed: {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"✗ Connection error: {e}")
    print(f"  Is Flask running on {BASE_URL}?")
    sys.exit(1)

print()

# Test 2: Get signs
print("📚 Testing signs endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/signs", timeout=5)
    if response.status_code == 200:
        signs = response.json()
        print(f"✓ Signs endpoint working")
        print(f"  Total signs: {len(signs)}")
        print(f"  Sample: {signs[:5]}")
    else:
        print(f"✗ Signs endpoint failed: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 3: Start detection
print("▶️  Testing start detection...")
try:
    response = requests.post(f"{BASE_URL}/api/start_detection", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Detection started")
        print(f"  Status: {data.get('status')}")
        time.sleep(2)
    else:
        print(f"✗ Failed to start: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 4: Get detected signs
print("👋 Testing detected signs endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/detected_signs", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Detected signs endpoint working")
        print(f"  Running: {data.get('running')}")
        print(f"  FPS: {data.get('fps')}")
        print(f"  Detected: {data.get('signs', [])}")
    else:
        print(f"✗ Failed: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Stop detection
print("⏹️  Testing stop detection...")
try:
    response = requests.post(f"{BASE_URL}/api/stop_detection", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Detection stopped")
        print(f"  Status: {data.get('status')}")
    else:
        print(f"✗ Failed to stop: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()
print("=" * 60)
print("✓ All API tests completed")
print("=" * 60)
