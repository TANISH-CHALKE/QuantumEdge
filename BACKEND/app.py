
from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = {"wav", "mp3", "m4a"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def init_db():
    conn = sqlite3.connect("voiceshield.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        upload_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "VoiceShield AI Backend is Running!"


@app.route("/upload", methods=["POST"])
def upload_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio = request.files["audio"]

    if audio.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(audio.filename):
        return jsonify({
            "error": "Invalid file type. Only .wav, .mp3 and .m4a files are allowed."
        }), 400

    audio.save(f"uploads/{audio.filename}")

    conn = sqlite3.connect("voiceshield.db")
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO uploads (filename) VALUES (?)",
        (audio.filename,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Audio uploaded successfully!",
        "filename": audio.filename
    })

if __name__ == "__main__":
    init_db()   # Create the database and table if they don't exist
    app.run(debug=True)
