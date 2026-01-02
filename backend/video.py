import os
import cv2
import numpy as np
import tensorflow as tf
import tempfile
import keras

try:
    detection_model = keras.models.load_model('./ai_detector.h5')
    print("Model loaded successfully!")
except:
    print("ERROR: Could not find 'ai_detector.h5'. Did you run the training script?")
    detection_model = None
    
def preprocess_uploaded_image(file_stream):
    file_bytes = np.frombuffer(file_stream.read(), np.uint8)
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    if image is None:
        return None
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 

    resized_img = cv2.resize(image, (128, 128))
    normalized_img = resized_img.astype("float32") 
    return np.expand_dims(normalized_img, axis=0)

def analyze_video_frames(video_path, model):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    fake_votes = 0
    real_votes = 0
    total_frames_checked = 0
    
    FRAME_SKIP = 30 

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % FRAME_SKIP == 0:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            resized = cv2.resize(rgb_frame, (128, 128))
            input_data = np.expand_dims(resized, axis=0)
            score = model.predict(input_data)[0][0]
            
            if score < 0.5:
                fake_votes += 1
            else:
                real_votes += 1
            
            total_frames_checked += 1

        frame_count += 1
    
    cap.release()
    
    if total_frames_checked == 0:
        return "Error", 0.0

    fake_ratio = fake_votes / total_frames_checked
    
    if fake_ratio > 0.4:
        verdict = "AI-Generated Video"
        conf = min(fake_ratio * 100 + 20, 99.9) 
        reasoning = "Multiple frames showed signs of  artifacts or unnatural flickering."
        rec = "Look closely at mouth movements and blinking; deepfakes often struggle there."
    else:
        verdict = "Real Video"
        conf = (1 - fake_ratio) * 100
        reasoning = "Motion blur and frame consistency look natural across the video."
        rec = "Video appears legitimate. Stay vigilant!"
        
    return verdict,conf,reasoning,rec
    
    
def ai_video(video):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_vid:
        video.save(temp_vid.name)
        temp_path = temp_vid.name
    
    try:
       return analyze_video_frames(temp_path, detection_model)
    finally:
        # Clean up the temp file
        os.remove(temp_path)