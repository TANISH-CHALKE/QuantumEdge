from flask import Flask, request, jsonify
from predictor import predict
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return {
        "message": "Deepfake Voice Scam Detector Backend is Running!"
    }

@app.route("/test")
def test():
    result = predict("samples/human1_clean.wav")
    return result

@app.route("/predict", methods=["POST"])
def predict_audio():

    if "audio" not in request.files:
        return jsonify({
            "error": "No audio file uploaded."
        }), 400

    audio_file = request.files["audio"]

    file_path = os.path.join(UPLOAD_FOLDER, audio_file.filename)

    audio_file.save(file_path)

    result = predict(file_path)

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5001)




