import cv2
import numpy as np
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
import tensorflow as tf
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

def get_ai_mentor_report(file_stream):
    
    processed_image = preprocess_uploaded_image(file_stream)
    
    raw_score = detection_model.predict(processed_image)[0][0]
    ai_percentage = (1- raw_score) * 100 
    
    if ai_percentage >= 50:
        verdict = "AI-Generated Image"
        reasoning = "I detected digital artifacts and pixel inconsistencies that are common in AI synthesis."
        recommendation = "Check the background details and shadows; AI often gets them wrong."
    else:
        verdict = "Real Photograph"
        reasoning = "The lighting physics and fine textures appear consistent with a natural camera capture."
        recommendation = "This looks authentic, but always verify the source."
        
    return verdict,ai_percentage, reasoning, recommendation

#used in server.py
def ai_image(image):
    return get_ai_mentor_report(image)
