from pathlib import Path

import cv2
import pandas as pd

from src.config import CROPS_DIR, CSV_FILTERED_DIR, RAW_DIR


def group_into_lines(df):
    df = df.sort_values(by="top").reset_index(drop=True)

    lines = []
    avg_height = df["height"].mean()
    threshold = avg_height * 0.6

    current_line = []
    current_top = None

    for _, row in df.iterrows():
        if current_top is None:
            current_line.append(row)
            current_top = row["top"]
            continue

        if abs(row["top"] - current_top) <= threshold:
            current_line.append(row)
        else:
            lines.append(current_line)
            current_line = [row]
            current_top = row["top"]

    if current_line:
        lines.append(current_line)

    return lines


def crop_bboxes(image_name: str, padding=8):
    image_path = RAW_DIR / image_name
    csv_path = CSV_FILTERED_DIR / f"{Path(image_name).stem}.csv"

    if not image_path.exists():
        raise FileNotFoundError(image_path)
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    image = cv2.imread(str(image_path))
    df = pd.read_csv(csv_path)

    if image is None:
        raise ValueError("Ошибка загрузки изображения")

    h, w = image.shape[:2]

    lines = group_into_lines(df)

    output_dir = CROPS_DIR / Path(image_name).stem
    output_dir.mkdir(parents=True, exist_ok=True)

    counter = 0

    for line_idx, line in enumerate(lines):
        line_sorted = sorted(line, key=lambda x: x["left"])

        for word_idx, row in enumerate(line_sorted):
            x, y, bw, bh = int(row.left), int(row.top), int(row.width), int(row.height)

            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(w, x + bw + padding)
            y2 = min(h, y + bh + padding)

            crop = image[y1:y2, x1:x2]

            out_path = output_dir / f"{Path(image_name).stem}_l{line_idx}_w{word_idx}.jpg"
            cv2.imwrite(str(out_path), crop)

            counter += 1

    print(f"[CROP] Сохранено: {counter}")
