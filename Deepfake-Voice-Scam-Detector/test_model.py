import os
from predictor import predict

folder = "samples"

print("\n===== TESTING ALL AUDIO FILES =====\n")

for file in sorted(os.listdir(folder)):
    if file.endswith(".wav"):
        print(f"Testing: {file}")

        result = predict(os.path.join(folder, file))

        print(result)
        print("-" * 40)


        