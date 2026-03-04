# Usage - python bbox_ocr.py original/test.jpg

import cv2
import pytesseract
import pandas as pd
import sys
from pathlib import Path
import shutil
import os


def ensure_dirs():
    folders = ["original", "bboxes", "csvs_original"]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)


def process_image(image_path):
    ensure_dirs()

    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Файл не найден: {image_path}")

    image = cv2.imread(str(image_path))

    if image is None:
        raise ValueError("Не удалось загрузить изображение")

    original_path = Path("original") / image_path.name

    if image_path.resolve() != original_path.resolve():
        shutil.copy(image_path, original_path)
        print(f"Оригинал сохранён: {original_path}")
    else:
        print("Файл уже находится в папке original, копирование пропущено")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(
        gray,
        output_type=pytesseract.Output.DATAFRAME
    )

    data = data[data.text.notnull()]
    data = data[data.text.str.strip() != ""]
    words = data[data.level == 5].copy()

    csv_path = Path("csvs_original") / f"{image_path.stem}.csv"
    words[['left', 'top', 'width', 'height']].to_csv(csv_path, index=False)
    print(f"Original CSV сохранён: {csv_path}")

    for _, row in words.iterrows():
        x, y, w, h = int(row.left), int(row.top), int(row.width), int(row.height)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    bbox_image_path = Path("bboxes") / f"{image_path.stem}_bbox.jpg"
    cv2.imwrite(str(bbox_image_path), image)
    print(f"BBox изображение сохранено: {bbox_image_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python bbox_ocr.py image.jpg")
        sys.exit(1)

    process_image(sys.argv[1])