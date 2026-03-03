import cv2
import pytesseract
import pandas as pd
import sys
from pathlib import Path
import shutil

def process_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Не удалось загрузить изображение")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)

    data = data[data.text.notnull()]
    data = data[data.text.str.strip() != ""]

    words = data[data.level == 5]

    for _, row in words.iterrows():
        x, y, w, h = row.left, row.top, row.width, row.height
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    bbox_image_path = Path(image_path).stem + "_bbox.jpg"
    cv2.imwrite(bbox_image_path, image)

    words[['left', 'top', 'width', 'height']].to_csv("bboxes.csv", index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python bbox_ocr.py image.jpg")
        sys.exit(1)

    process_image(sys.argv[1])