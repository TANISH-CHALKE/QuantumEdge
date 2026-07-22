
import torch
import librosa
from transformers import AutoModelForAudioClassification, AutoFeatureExtractor

# Hugging Face model
MODEL_NAME = "garystafford/wav2vec2-deepfake-voice-detector"

print("Loading AI model...")

# Load AI model
model = AutoModelForAudioClassification.from_pretrained(MODEL_NAME)
feature_extractor = AutoFeatureExtractor.from_pretrained(MODEL_NAME)

#print("Model loaded successfully!")


def predict(audio_path):
    try:
        # Load the test audio
        audio, sample_rate = librosa.load(
            audio_path,
            sr=16000,
            mono=True
        )

        #print("\nAudio loaded successfully!")
        #print(f"File: {audio_path}")
        #print(f"Sample Rate: {sample_rate} Hz")     

        # Convert audio into the format expected by the AI model
        inputs = feature_extractor(
            audio,
            sampling_rate=sample_rate,
            return_tensors="pt"
        )

        #print("\nAudio converted into AI input successfully!")

        # Let the AI analyze the audio
        with torch.no_grad():
            outputs = model(**inputs)

        #print("AI has analyzed the audio!")

        # Convert AI output into probabilities
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

        # Find the predicted class
        predicted_class = torch.argmax(probabilities, dim=-1).item()

        # Confidence score
        confidence = probabilities[0][predicted_class].item()

        print("\nPrediction complete!")
        prediction = model.config.id2label[predicted_class]

        print("\n========== RESULT ==========")
        print(f"Prediction : {prediction.upper()}")
        print(f"Confidence : {confidence:.2%}")
        print("============================")

        #print("\nModel Labels:")
        #print(model.config.id2label)

        return {
    "prediction": prediction,
    "confidence": round(confidence * 100, 2)
}

    except Exception as e:
        return {
            "error": str(e)
        }
    
#if __name__ == "__main__":
 #   result = predict("samples/ai1.wav")
  #  print("\nReturned Result:")
   # print(result)


