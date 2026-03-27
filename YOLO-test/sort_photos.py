import os
import shutil
from pathlib import Path

import cv2


RAW_DIR = Path("raw_photos")
DATASET_DIR = Path("dataset")
VALID_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def list_images(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXTS])


def print_help(classes: list[str]) -> None:
    print("\nSorting controls:")
    print("  [1..9] -> move image to corresponding class")
    print("  s      -> skip image")
    print("  d      -> delete image")
    print("  q      -> quit")
    print("\nClass mapping:")
    for i, cls in enumerate(classes, start=1):
        print(f"  {i}: {cls}")
    print("")


def ensure_classes() -> list[str]:
    DATASET_DIR.mkdir(exist_ok=True)
    classes = sorted([p.name for p in DATASET_DIR.iterdir() if p.is_dir()])
    if classes:
        return classes

    raw = input("No classes found in dataset/. Enter class names separated by commas: ").strip()
    classes = [c.strip() for c in raw.split(",") if c.strip()]
    for c in classes:
        (DATASET_DIR / c).mkdir(parents=True, exist_ok=True)
    return classes


def main() -> None:
    RAW_DIR.mkdir(exist_ok=True)
    classes = ensure_classes()
    if not classes:
        print("No classes available. Exiting.")
        return

    print_help(classes)
    images = list_images(RAW_DIR)
    if not images:
        print("No images found in raw_photos/.")
        return

    for img_path in images:
        image = cv2.imread(str(img_path))
        if image is None:
            print(f"Skipping unreadable file: {img_path}")
            continue

        cv2.imshow("Sort Photos", image)
        key = cv2.waitKey(0) & 0xFF

        if key == ord("q"):
            break
        if key == ord("s"):
            continue
        if key == ord("d"):
            img_path.unlink(missing_ok=True)
            print(f"Deleted: {img_path}")
            continue

        idx = key - ord("1")
        if 0 <= idx < len(classes):
            target_class = classes[idx]
            target_dir = DATASET_DIR / target_class
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / img_path.name
            shutil.move(str(img_path), str(target_path))
            print(f"Moved: {img_path.name} -> dataset/{target_class}/")
        else:
            print("Unknown key, skipped.")

    cv2.destroyAllWindows()
    print("Sorting finished.")


if __name__ == "__main__":
    main()

