import os
import librosa
import soundfile as sf

def process_audio(audio_path, category):

    print("\n----------------------------------------")
    print(f"Processing : {audio_path}")

    # Load audio (16 kHz)
    y, sr = librosa.load(audio_path, sr=16000)

    # Normalize Audio
    y = librosa.util.normalize(y)

    print("Audio normalized.")

    # -------------------------------
    # TEMPORARY TEST
    # Skip noise reduction completely
    # -------------------------------
    clean_audio = y

    print("Noise reduction skipped (TEST MODE).")

    # Audio Information
    print(f"Sample Rate      : {sr} Hz")
    print(f"Samples          : {len(clean_audio)}")
    print(f"Duration         : {len(clean_audio)/sr:.2f} seconds")
    print(f"Data Type        : {clean_audio.dtype}")

    # Create output folder if needed
    os.makedirs(f"output/cleaned_audio/{category}", exist_ok=True)

    # File name
    filename = os.path.splitext(os.path.basename(audio_path))[0]
    clean_path = f"output/cleaned_audio/{category}/{filename}_clean.wav"

    # Save audio
    sf.write(
        clean_path,
        clean_audio,
        sr
    )

    print(f"Saved: {clean_path}")

    return clean_path


