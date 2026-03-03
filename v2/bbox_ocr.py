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

    original_image_path = Path(image_path).stem + "_original.jpg"
    shutil.copy(image_path, original_image_path)
    print(f"Сохранили оригинал: {original_image_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)

    data = data[data.text.notnull()]
    data = data[data.text.str.strip() != ""]

    words = data[data.level == 5]

    for _, row in words.iterrows():
        x, y, w, h = row.left, row.top, row.width, row.height
        text = row.text
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # cv2.putText(image, text, (x, y - 5),
                    # cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    bbox_image_path = Path(image_path).stem + "_bbox.jpg"
    cv2.imwrite(bbox_image_path, image)

    words[['text', 'left', 'top', 'width', 'height']].to_csv("bboxes.csv", index=False)

    print(f"Сохранили размеченное изображение: {bbox_image_path}")
    print("CSV с координатами: bboxes.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python bbox_ocr.py image.jpg")
        sys.exit(1)

    process_image(sys.argv[1])