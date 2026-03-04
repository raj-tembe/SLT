##JAI SHREE RAM
from flask import Flask, render_template, jsonify, request, Response
from src.backbone import TFLiteModel, get_model
from src.landmarks_extraction import mediapipe_detection, draw, extract_coordinates, load_json_file
from src.config import SEQ_LEN, THRESH_HOLD, FRAME_SKIP, PREDICTION_SKIP, USE_GPU, USE_MIXED_PRECISION, CAMERA_WIDTH, CAMERA_HEIGHT, JPEG_QUALITY
import numpy as np
import cv2
import time
import mediapipe as mp
import json
import os
import threading
from collections import deque
from queue import Queue
import traceback

# =========== GPU SETUP - RUN BEFORE TF IMPORTS ===========
try:
    import tensorflow as tf
    import os
    # Suppress TF warnings
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    # Configure GPU memory growth
    gpus = tf.config.list_physical_devices('GPU')
    if gpus and USE_GPU:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"[GPU] {len(gpus)} GPU(s) detected - Memory growth enabled")
        except RuntimeError as e:
            print(f"[GPU] Memory growth error: {e}")
    else:
        print("[CPU] No GPU detected, using CPU for inference")
    
    # Enable mixed precision for faster inference (only if GPU available)
    if USE_MIXED_PRECISION and gpus:
        try:
            policy = tf.keras.mixed_precision.Policy('mixed_float16')
            tf.keras.mixed_precision.set_global_policy(policy)
            print("[GPU] Mixed precision (float16) enabled for faster inference")
        except Exception as e:
            print(f"[GPU] Mixed precision info: {e}")
    
except Exception as e:
    print(f"[GPU] TensorFlow config error: {e}")

# Initialize Flask app
app = Flask(__name__)

# MediaPipe setup
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils

# Load sign to prediction index map
with open('src/sign_to_prediction_index_map.json', 'r') as f:
    sign_map = json.load(f)

# Create mappings
s2p_map = {k.lower(): v for k, v in sign_map.items()}
p2s_map = {v: k for k, v in sign_map.items()}
encoder = lambda x: s2p_map.get(x.lower())
decoder = lambda x: p2s_map.get(x)

# Create a sorted list of signs for the learning page
signs_list = sorted(sign_map.keys())

# Load ML models
models_path = ['./models/FINAL_ASL_250.h5']
models = [get_model() for _ in models_path]

# Load weights from the weights file
for model, path in zip(models, models_path):
    try:
        model.load_weights(path)
        print(f"[OK] Model loaded successfully: {path}")
    except Exception as e:
        print(f"[ERROR] Could not load model weights: {e}")

# TFLite model wrapper
tflite_keras_model = TFLiteModel(islr_models=models)

# Global variables for video streaming
class VideoStreamHandler:
    def __init__(self):
        self.frame_queue = Queue(maxsize=3)
        self.detected_signs = deque(maxlen=15)
        self.sequence_data = []
        self.cap = None
        self.is_running = False
        self.lock = threading.Lock()
        self.fps = 0
        self.frame_count = 0
        self.last_time = time.time()
        self.camera_thread = None
        self.holistic = None
        self.frame_skip = FRAME_SKIP  # Skip frames for better FPS
        self.prediction_skip = PREDICTION_SKIP  # Skip predictions
        self.prediction_count = 0  # Counter for prediction skipping
        
    def camera_capture_thread(self):
        """Separate thread for camera capture and processing"""
        try:
            print("[CAMERA] Thread started...")
            self.cap = cv2.VideoCapture(0)
            
            if not self.cap.isOpened():
                print("[ERROR] Camera not available")
                self.is_running = False
                return
            
            # Set camera resolution - LOWER for better FPS
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            print("[INIT] Initializing MediaPipe holistic...")
            try:
                # Initialize MediaPipe holistic - model_complexity=0 for speed
                self.holistic = mp_holistic.Holistic(
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5,
                    model_complexity=0
                )
                print("[OK] MediaPipe holistic initialized")
            except Exception as e:
                print(f"[ERROR] Failed to initialize MediaPipe: {e}")
                self.is_running = False
                return
            
            print("[OK] Camera initialized, processing frames...")
            frame_idx = 0
            
            while self.is_running:
                try:
                    ret, frame = self.cap.read()
                    if not ret:
                        print("[WARN] Failed to read frame")
                        time.sleep(0.01)
                        continue
                    
                    frame_idx += 1
                    should_process = (frame_idx % self.frame_skip == 0)
                    
                    # Perform MediaPipe detection only on selected frames
                    if should_process:
                        try:
                            image, results = mediapipe_detection(frame, self.holistic)
                            draw(image, results)
                        except Exception as e:
                            print(f"[WARN] Detection error: {e}")
                            image = frame
                            results = None
                    else:
                        image = frame
                        results = None
                    
                    # Extract landmarks only when processing
                    if should_process:
                        try:
                            if results:
                                landmarks = extract_coordinates(results)
                            else:
                                landmarks = np.zeros((468 + 21 + 33 + 21, 3))
                        except Exception as e:
                            landmarks = np.zeros((468 + 21 + 33 + 21, 3))
                        
                        self.sequence_data.append(landmarks)
                    
                    sign = ""
                    
                    # Generate prediction every SEQ_LEN frames (or skip some for better FPS)
                    if len(self.sequence_data) >= SEQ_LEN and self.prediction_count % PREDICTION_SKIP == 0:
                        try:
                            seq_to_predict = np.array(self.sequence_data[-SEQ_LEN:], dtype=np.float32)
                            prediction = tflite_keras_model(seq_to_predict)["outputs"]
                            
                            pred_max = np.max(prediction.numpy(), axis=-1)
                            if pred_max > THRESH_HOLD:
                                sign_idx = int(np.argmax(prediction.numpy(), axis=-1))
                                sign = decoder(sign_idx)
                                print(f"[DETECT] {sign} (confidence: {pred_max:.2f})")
                            
                            # Slide window
                            self.sequence_data = self.sequence_data[SEQ_LEN//2:]
                        except Exception as e:
                            print(f"[WARN] Prediction error: {e}")
                            self.sequence_data = self.sequence_data[1:]
                    
                    self.prediction_count += 1
                    
                    # Add to detected signs
                    # Only prevent duplicate if it's the most recent sign (not if it's anywhere in history)
                    last_sign = self.detected_signs[0] if len(self.detected_signs) > 0 else None
                    if sign != "" and sign != last_sign:
                        with self.lock:
                            self.detected_signs.appendleft(sign)
                    
                    # Flip image for selfie view
                    image = cv2.flip(image, 1)
                    
                    # Add sequence counter (lightweight)
                    cv2.putText(image, f"Seq: {len(self.sequence_data)}/{SEQ_LEN}", (5, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
                    
                    # Calculate FPS
                    self.frame_count += 1
                    current_time = time.time()
                    if current_time - self.last_time > 1.0:
                        self.fps = self.frame_count
                        print(f"  FPS: {self.fps} | Seq: {len(self.sequence_data)}")
                        self.frame_count = 0
                        self.last_time = current_time
                    
                    # Add FPS counter (lightweight)
                    cv2.putText(image, f"FPS: {self.fps}", (5, 60),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1, cv2.LINE_AA)
                    
                    # Encode and queue frame
                    try:
                        ret, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, JPEG_QUALITY])
                        if ret:
                            frame_bytes = buffer.tobytes()
                            # Non-blocking put
                            try:
                                self.frame_queue.put_nowait(frame_bytes)
                            except:
                                # Queue full, skip this frame
                                pass
                    except Exception as e:
                        print(f"[WARN] Encode error: {e}")
                    
                    # Minimal sleep for CPU relief
                    time.sleep(0.0001)
                    
                except Exception as e:
                    print(f"[WARN] Frame processing error: {e}")
                    traceback.print_exc()
                    time.sleep(0.01)
        
        except Exception as e:
            print(f"[FATAL] Camera thread error: {e}")
            traceback.print_exc()
        finally:
            print("[CLEANUP] Cleaning up camera thread...")
            if self.cap:
                self.cap.release()
            if self.holistic:
                self.holistic.close()
            self.is_running = False
            print("[OK] Camera thread cleaned up")
    
    def generate_frames(self):
        """Generate MJPEG frames from queue"""
        print("[STREAM] Starting frame streaming...")
        frame_timeout_count = 0
        
        while self.is_running:
            try:
                # Wait for frame from queue (timeout 2 seconds)
                try:
                    frame_bytes = self.frame_queue.get(timeout=2)
                    frame_timeout_count = 0
                except:
                    # No frame available
                    frame_timeout_count += 1
                    if frame_timeout_count > 3:
                        print("[WARN] No frames from camera for 6+ seconds")
                    continue
                
                # Yield frame in MJPEG format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n'
                       b'Content-Length: ' + f'{len(frame_bytes)}'.encode() + b'\r\n\r\n' +
                       frame_bytes + b'\r\n')
                
            except GeneratorExit:
                print("[OK] Client disconnected from stream")
                break
            except Exception as e:
                print(f"[WARN] Stream error: {e}")
                time.sleep(0.01)
        
        print("[OK] Frame streaming ended")
    
    def start(self):
        """Start camera capture thread"""
        if not self.is_running:
            self.is_running = True
            self.sequence_data = []
            self.detected_signs.clear()
            self.camera_thread = threading.Thread(
                target=self.camera_capture_thread,
                daemon=True,
                name="CameraThread"
            )
            self.camera_thread.start()
            print("✓ Camera thread started")
            # Give thread time to initialize
            time.sleep(1)
    
    def stop(self):
        """Stop camera capture thread"""
        self.is_running = False
        if self.camera_thread and self.camera_thread.is_alive():
            self.camera_thread.join(timeout=3)
        print("✓ Camera stopped")
    
    def get_detected_signs(self):
        """Get current detected signs"""
        with self.lock:
            return list(self.detected_signs)
    
    def clear_signs(self):
        """Clear detected signs"""
        with self.lock:
            self.detected_signs.clear()

# Initialize video stream handler
video_handler = VideoStreamHandler()

# ================== ROUTES ==================

@app.route('/')
def index():
    """Home page route"""
    return render_template('index.html')

@app.route('/translator')
def translator():
    """Translator page route"""
    return render_template('translator.html')

@app.route('/learn')
def learn():
    """Learning hub page route"""
    return render_template('learn.html', signs=signs_list)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'running': video_handler.is_running,
        'fps': video_handler.fps,
        'detected_signs': len(video_handler.get_detected_signs())
    })

@app.route('/video_feed')
def video_feed():
    """Video streaming route with proper MJPEG headers"""
    try:
        response = Response(video_handler.generate_frames(),
                           mimetype='multipart/x-mixed-replace; boundary=frame')
        response.headers.add('Connection', 'keep-alive')
        response.headers.add('Cache-Control', 'no-cache')
        response.headers.add('Pragma', 'no-cache')
        response.headers.add('Expires', '0')
        return response
    except Exception as e:
        print(f"✗ Streaming error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/start_detection', methods=['POST'])
def start_detection():
    """Start sign detection"""
    try:
        if not video_handler.is_running:
            print("Starting detection...")
            video_handler.start()
            # Give it a moment to start
            time.sleep(0.5)
            return jsonify({'status': 'started', 'message': 'Detection started'})
        return jsonify({'status': 'already_running', 'message': 'Detection already running'})
    except Exception as e:
        print(f"✗ Error starting detection: {e}")
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/stop_detection', methods=['POST'])
def stop_detection():
    """Stop sign detection"""
    try:
        print("Stopping detection...")
        video_handler.stop()
        return jsonify({'status': 'stopped', 'message': 'Detection stopped'})
    except Exception as e:
        print(f"✗ Error stopping detection: {e}")
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/clear_signs', methods=['POST'])
def clear_signs():
    """Clear detected signs"""
    try:
        video_handler.clear_signs()
        return jsonify({'status': 'cleared', 'message': 'Detected signs cleared'})
    except Exception as e:
        print(f"✗ Error clearing signs: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 400

@app.route('/api/detected_signs', methods=['GET'])
def get_detected_signs():
    """Get current detected signs"""
    try:
        signs = video_handler.get_detected_signs()
        return jsonify({
            'signs': signs,
            'fps': video_handler.fps,
            'running': video_handler.is_running
        })
    except Exception as e:
        print(f"✗ Error fetching detected signs: {e}")
        traceback.print_exc()
        return jsonify({'status': 'error', 'message': str(e), 'signs': [], 'fps': 0}), 400

@app.route('/api/signs', methods=['GET'])
def get_signs():
    """API endpoint to get all signs"""
    try:
        return jsonify(signs_list)
    except Exception as e:
        print(f"✗ Error fetching signs: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/search', methods=['POST'])
def search_signs():
    """API endpoint to search signs"""
    try:
        query = request.json.get('query', '').lower()
        
        if not query:
            return jsonify(signs_list)
        
        results = [sign for sign in signs_list if query in sign.lower()]
        return jsonify(results)
    except Exception as e:
        print(f"✗ Error searching signs: {e}")
        return jsonify({'error': str(e)}), 500

@app.before_request
def before_request():
    """Pre-request processing"""
    pass

@app.after_request
def after_request(response):
    """Post-request processing"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    print("=" * 60)
    print("🤟 Sign Language Translator - Flask Server")
    print("=" * 60)
    print(f"✓ Loaded {len(signs_list)} signs")
    print("✓ ML Model: FINAL_ASL_250.h5")
    print("✓ Starting server on http://0.0.0.0:5000")
    print("=" * 60)
    print()
    print("Routes:")
    print("  http://localhost:5000/               - Home page")
    print("  http://localhost:5000/translator     - Live translator")
    print("  http://localhost:5000/learn          - Learning hub")
    print("  http://localhost:5000/health         - Health check")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    try:
        # Use threaded=True for concurrent requests
        # use_reloader=False to prevent double threading
        # debug=False to prevent debug mode issues
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000,
            threaded=True,
            use_reloader=False
        )
    except KeyboardInterrupt:
        print("\n✓ Shutting down...")
        video_handler.stop()
        print("✓ Server shutdown complete")
    except Exception as e:
        print(f"\n✗ Server error: {e}")
        traceback.print_exc()
        video_handler.stop()

