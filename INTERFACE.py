##JAI SHREE RAM
from src.backbone import TFLiteModel, get_model
from src.landmarks_extraction import mediapipe_detection, draw, extract_coordinates, load_json_file 
from src.config import SEQ_LEN, THRESH_HOLD, USE_GPU, USE_MIXED_PRECISION, CAMERA_WIDTH, CAMERA_HEIGHT
import numpy as np
import cv2
import time
import mediapipe as mp

# =========== GPU SETUP ===========
try:
    import tensorflow as tf
    import os
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    gpus = tf.config.list_physical_devices('GPU')
    if gpus and USE_GPU:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"[GPU] {len(gpus)} GPU(s) detected - Memory growth enabled")
    else:
        print("[CPU] No GPU detected, using CPU")
    
    if USE_MIXED_PRECISION and gpus:
        try:
            policy = tf.keras.mixed_precision.Policy('mixed_float16')
            tf.keras.mixed_precision.set_global_policy(policy)
            print("[GPU] Mixed precision (float16) enabled")
        except Exception as e:
            print(f"[GPU] Mixed precision info: {e}")
except Exception as e:
    print(f"[GPU] Config error: {e}")

mp_holistic = mp.solutions.holistic 
mp_drawing = mp.solutions.drawing_utils

s2p_map = {k.lower():v for k,v in load_json_file("src/sign_to_prediction_index_map.json").items()}
p2s_map = {v:k for k,v in load_json_file("src/sign_to_prediction_index_map.json").items()}
encoder = lambda x: s2p_map.get(x.lower())
decoder = lambda x: p2s_map.get(x)

models_path = [
                './models/FINAL_ASL_250.h5',
]
models = [get_model() for _ in models_path]

# Load weights from the weights file.
for model,path in zip(models,models_path):
    model.load_weights(path)

def real_time_asl():
    res = []
    tflite_keras_model = TFLiteModel(islr_models=models)
    sequence_data = []
    cap = cv2.VideoCapture(0)
    
    start = time.time()
    
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5, model_complexity=0) as holistic:
        # The main loop for the mediapipe detection.
        while cap.isOpened():
            ret, frame = cap.read()
            
            start = time.time()
            
            image, results = mediapipe_detection(frame, holistic)
            draw(image, results)
            
            try:
                landmarks = extract_coordinates(results)
            except:
                landmarks = np.zeros((468 + 21 + 33 + 21, 3))
            sequence_data.append(landmarks)
            
            sign = ""
            
            # Generate the prediction for the given sequence data.
            if len(sequence_data) % SEQ_LEN == 0:
                prediction = tflite_keras_model(np.array(sequence_data, dtype = np.float32))["outputs"]

                if np.max(prediction.numpy(), axis=-1) > THRESH_HOLD:
                    sign = np.argmax(prediction.numpy(), axis=-1)
                
                sequence_data = []
            
            image = cv2.flip(image, 1)
            
            cv2.putText(image, f"{len(sequence_data)}", (3, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            
            # Insert the sign in the result set if sign is not empty.
            if sign != "" and decoder(sign) not in res:
                res.insert(0, decoder(sign))
            
            # Display detected signs directly on image (lightweight)
            cv2.putText(image, f"Signs: {', '.join(str(x) for x in res[:5])}", (5, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2, cv2.LINE_AA)
                            
            cv2.imshow('Webcam Feed', image)
            
            # Wait for a key to be pressed.
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

real_time_asl()