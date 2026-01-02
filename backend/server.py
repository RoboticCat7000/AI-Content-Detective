
from flask import Flask, request, jsonify
from flask_cors import CORS
from text import ai_text
from image import ai_image
from video import ai_video

app = Flask(__name__)
CORS(app)

def make_response(verdict, confidence_score, explanation, recommendation):
    print(confidence_score)
    return {
        "verdict": verdict,
        "confidence": confidence_score,
        "mentor_response": explanation,
        "recommendation": recommendation
    }

@app.route('/image', methods=['POST'])
def detect_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    if file.content_type not in ['image/jpeg', 'image/png']:    
        return jsonify({"error": "Unsupported file type"}), 400
    
    if file:
        v,c,r,rec = ai_image(file)
        output = make_response(v,c.astype(float),r,rec)
        return jsonify({"message": f"Image {file.filename} scanned successfully", "output": output}), 200
        

    return jsonify({"error": "Something went wrong"}), 500


@app.route('/video', methods=['POST'])
def detect_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400
    
    if file.content_type not in ['video/mp4']:
        return jsonify({"error": "Unsupported file type"}), 400
    
    if file:
        print(file)
        v,c,r,rec = ai_video(file)
        output = make_response(v,c,r,rec)
        return jsonify({"message": f"Video {file.filename} scanned successfully", "output": output}), 200
        

    return jsonify({"error": "Something went wrong"}), 500

@app.route("/text",methods=["POST"])
def detect_text():
    if 'text' not in request.form:
        return jsonify({"error": "No text part in the request"}), 400

    text = request.form['text']
    v,c,r,rec = ai_text(text)
    output = make_response(v,c,r,rec)
    return jsonify({"message": f"{text} uploaded successfully", "output": output}), 200

if __name__ == "__main__":
    app.run()
