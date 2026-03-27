
from ultralytics import YOLO
import cv2
import os

CUSTOM_WEIGHTS = os.environ.get("YOLO_CLS_WEIGHTS", "models/my_model.pt")
if not os.path.exists(CUSTOM_WEIGHTS):
    raise FileNotFoundError(
        f"Custom weights not found: {CUSTOM_WEIGHTS}\n"
        "Train first with: python train_classifier.py"
    )
print(f"Loading model weights: {CUSTOM_WEIGHTS}")
model = YOLO(CUSTOM_WEIGHTS)

cap = cv2.VideoCapture(0)

DATASET_DIR = "dataset"
os.makedirs(DATASET_DIR, exist_ok=True)

img_count = 0

while True:
    cmd = input("Press Enter to capture, or type 'q' to quit: ").strip().lower()
    if cmd == "q":
        break

    ret, frame = cap.read()
    if not ret:
        print("Failed to read from camera.")
        continue

    results = model(frame)
    probs = results[0].probs

    predicted_class = probs.top1
    confidence = probs.top1conf
    predicted_name = results[0].names.get(int(predicted_class), str(predicted_class))

    print(f"Prediction: {predicted_name} ({confidence:.2f})")

    cv2.imshow("Frame", frame)

    resp = input("Correct? [y]=save as predicted, [n]=type label, [s]=skip, [q]=quit: ").strip().lower()
    if resp == "q":
        break
    if resp == "y":
        label = str(predicted_name)
    elif resp == "n":
        label = input("Enter correct label (e.g. with/without): ").strip()
        if not label:
            continue
    elif resp == "s":
        continue
    else:
        continue

    # Save image
    folder = os.path.join(DATASET_DIR, label)
    os.makedirs(folder, exist_ok=True)

    img_path = os.path.join(folder, f"img_{img_count}.jpg")
    cv2.imwrite(img_path, frame)

    img_count += 1
cap.release()
cv2.destroyAllWindows()
