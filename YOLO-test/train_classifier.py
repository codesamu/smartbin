import os
import random
import shutil
from pathlib import Path

from ultralytics import YOLO


IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_image(p: Path) -> bool:
    return p.is_file() and p.suffix.lower() in IMG_EXTS


def prepare_split(dataset_dir: Path, out_dir: Path, val_ratio: float = 0.2, seed: int = 42) -> None:
    """
    Converts:
      dataset/<class>/*.jpg
    Into:
      out_dir/train/<class>/*.jpg
      out_dir/val/<class>/*.jpg
    """
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")

    class_dirs = [p for p in dataset_dir.iterdir() if p.is_dir()]
    if not class_dirs:
        raise RuntimeError(f"No class subfolders found in {dataset_dir} (expected dataset/<class>/...)")

    random.seed(seed)

    if out_dir.exists():
        shutil.rmtree(out_dir)
    (out_dir / "train").mkdir(parents=True, exist_ok=True)
    (out_dir / "val").mkdir(parents=True, exist_ok=True)

    for class_dir in sorted(class_dirs):
        images = [p for p in class_dir.rglob("*") if is_image(p)]
        if not images:
            continue

        random.shuffle(images)
        n_val = max(1, int(len(images) * val_ratio)) if len(images) >= 5 else max(0, int(len(images) * val_ratio))
        val_set = set(images[:n_val])

        (out_dir / "train" / class_dir.name).mkdir(parents=True, exist_ok=True)
        (out_dir / "val" / class_dir.name).mkdir(parents=True, exist_ok=True)

        for img in images:
            split = "val" if img in val_set else "train"
            dst = out_dir / split / class_dir.name / img.name
            shutil.copy2(img, dst)


def main() -> None:
    dataset_dir = Path(os.environ.get("DATASET_DIR", "dataset"))
    split_dir = Path(os.environ.get("SPLIT_DIR", "dataset_split"))
    output_model = Path(os.environ.get("OUTPUT_MODEL", "models/my_model.pt"))

    val_ratio = float(os.environ.get("VAL_RATIO", "0.2"))
    epochs = int(os.environ.get("EPOCHS", "20"))
    imgsz = int(os.environ.get("IMGSZ", "224"))
    batch = int(os.environ.get("BATCH", "32"))

    print(f"Preparing split from {dataset_dir} -> {split_dir} (val_ratio={val_ratio})")
    prepare_split(dataset_dir, split_dir, val_ratio=val_ratio)

    # Start from a pretrained backbone, then finetune on your classes.
    model = YOLO("yolov8n-cls.pt")
    print("Training classifier...")
    model.train(
        data=str(split_dir),
        epochs=epochs,
        imgsz=imgsz,
        batch=batch,
    )

    train_dir = Path(model.trainer.save_dir)
    best_weights = train_dir / "weights" / "best.pt"
    if not best_weights.exists():
        raise FileNotFoundError(f"Could not find trained weights at {best_weights}")

    output_model.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(best_weights, output_model)

    print("Done.")
    print(f"Latest run weights: {best_weights}")
    print(f"Copied model to: {output_model}")
    print("test.py will load this model path by default.")


if __name__ == "__main__":
    main()

