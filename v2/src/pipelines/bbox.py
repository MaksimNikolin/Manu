
import cv2
import pytesseract

from src.config import BBOX_DIR, CSV_RAW_DIR, RAW_DIR


def process_image(image_name: str):
    image_path = RAW_DIR / image_name

    if not image_path.exists():
        raise FileNotFoundError(f"Нет файла: {image_path}")

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError("Не удалось загрузить изображение")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    data = pytesseract.image_to_data(gray, output_type=pytesseract.Output.DATAFRAME)

    data = data[data.text.notnull()]
    data = data[data.text.str.strip() != ""]
    words = data[data.level == 5].copy()

    # --- CSV ---
    CSV_RAW_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = CSV_RAW_DIR / f"{image_path.stem}.csv"

    words[["left", "top", "width", "height"]].to_csv(csv_path, index=False)

    # --- BBOX IMAGE ---
    BBOX_DIR.mkdir(parents=True, exist_ok=True)
    bbox_image_path = BBOX_DIR / f"{image_path.stem}.jpg"

    for _, row in words.iterrows():
        x, y, w, h = int(row.left), int(row.top), int(row.width), int(row.height)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(str(bbox_image_path), image)

    print(f"[BBOX] CSV: {csv_path}")
    print(f"[BBOX] Image: {bbox_image_path}")
