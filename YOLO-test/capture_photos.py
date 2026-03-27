import os
import time

import cv2


RAW_DIR = "raw_photos"


def next_index(folder: str) -> int:
    max_i = -1
    for name in os.listdir(folder):
        if not name.startswith("img_"):
            continue
        stem, ext = os.path.splitext(name)
        if ext.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        try:
            i = int(stem.split("_", 1)[1])
            max_i = max(max_i, i)
        except (IndexError, ValueError):
            continue
    return max_i + 1


def main() -> None:
    os.makedirs(RAW_DIR, exist_ok=True)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not open webcam.")
        return

    img_count = next_index(RAW_DIR)
    print("Preview opened.")
    print("Controls:")
    print("  c -> capture photo")
    print("  q -> quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            break

        cv2.imshow("Capture Photos", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break
        if key == ord("c"):
            filename = f"img_{img_count}.jpg"
            path = os.path.join(RAW_DIR, filename)
            cv2.imwrite(path, frame)
            print(f"Saved: {path}")
            img_count += 1
            time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

