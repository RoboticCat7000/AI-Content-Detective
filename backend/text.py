from transformers import pipeline 
import os
os.environ["TF_USE_LEGACY_KERAS"] = "1"
    
detector = pipeline("text-classification", model="roberta-base-openai-detector")

def analyze_text(text):
    # 1. Run the AI Detection Model
    # The model returns a label (e.g., "Fake" or "Real") and a score
    results = detector(text)
    
    # 2. Interpret Results for the Student
    # Example output: [{'label': 'Fake', 'score': 0.98}]
    label = results[0]['label']
    score = results[0]['score']
    
    # Convert label to "AI-Generated" or "Human-Written"
    # Note: Model labels vary. For OpenAI detector: 'Fake' = AI, 'Real' = Human
    if label == 'Fake':
        verdict = "Likely AI-Generated"
        confidence = score * 100
        rec = "Stay careful of AI-generated content."
        explanation = "The text structure is highly predictable and lacks the variability often seen in human writing."
    else:
        verdict = "Likely Human-Written"
        confidence = score * 100
        rec = "This was human made, but always verify the source."
        explanation = "The text shows high sentence variation and unpredictability typical of human authors."
    return verdict,confidence,explanation,rec

def ai_text(text):
    return analyze_text(text)    
