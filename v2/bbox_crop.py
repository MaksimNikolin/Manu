# python bbox_crop.py original/test.jpg

import pandas as pd
import cv2
import sys
from pathlib import Path
import os


def ensure_dirs(image_stem):
    os.makedirs("cropped_boxes", exist_ok=True)
    os.makedirs(Path("cropped_boxes") / image_stem, exist_ok=True)


def group_into_lines(df):
    df = df.sort_values(by="top").reset_index(drop=True)
    lines = []

    avg_height = df["height"].mean()
    line_threshold = avg_height * 0.6

    current_line = []
    current_top = None

    for _, row in df.iterrows():
        if current_top is None:
            current_line.append(row)
            current_top = row["top"]
            continue

        if abs(row["top"] - current_top) <= line_threshold:
            current_line.append(row)
        else:
            lines.append(current_line)
            current_line = [row]
            current_top = row["top"]

    if current_line:
        lines.append(current_line)

    return lines


def crop_bboxes(image_name, padding=8):
    image_name = Path(image_name)

    original_image_path = Path("original") / image_name.name
    csv_filtered_path = Path("csvs_filtered") / f"{image_name.stem}_filtered.csv"

    if not original_image_path.exists():
        raise FileNotFoundError(f"Не найдено изображение: {original_image_path}")

    if not csv_filtered_path.exists():
        raise FileNotFoundError(f"Не найден CSV: {csv_filtered_path}")

    ensure_dirs(image_name.stem)

    df = pd.read_csv(csv_filtered_path)
    image = cv2.imread(str(original_image_path))

    if image is None:
        raise ValueError("Не удалось загрузить изображение")

    img_h, img_w = image.shape[:2]

    lines = group_into_lines(df)

    print(f"Найдено строк: {len(lines)}")

    counter = 0

    for line_idx, line in enumerate(lines):
        line_sorted = sorted(line, key=lambda x: x["left"])

        for word_idx, row in enumerate(line_sorted):
            x = int(row["left"])
            y = int(row["top"])
            w = int(row["width"])
            h = int(row["height"])

            # --- применяем padding ---
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(img_w, x + w + padding)
            y2 = min(img_h, y + h + padding)

            cropped = image[y1:y2, x1:x2]

            output_path = (
                Path("cropped_boxes")
                / image_name.stem
                / f"{image_name.stem}_line{line_idx}_word{word_idx}.jpg"
            )

            cv2.imwrite(str(output_path), cropped)
            counter += 1

    print(f"Готово. Сохранено {counter} изображений в cropped_boxes/{image_name.stem}/")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python bbox_crop.py test.jpg [padding]")
        sys.exit(1)

    image_name = sys.argv[1]
    padding = int(sys.argv[2]) if len(sys.argv) == 3 else 8

    crop_bboxes(image_name, padding)