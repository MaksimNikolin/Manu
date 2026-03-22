import json
import time
from pathlib import Path

import easyocr

from src.config import CROPS_DIR, OCR_DIR

reader = easyocr.Reader(["ar"], gpu=False)


def run_ocr(image_name: str, batch_size: int = 20, pause: float = 0.05):
    """
    Обрабатывает все crop-изображения для данного изображения с помощью EasyOCR.

    :param image_name: имя исходного изображения
    :param batch_size: количество файлов, обрабатываемых за один цикл
    :param pause: пауза между обработкой файлов (секунды)
    """
    image_id = Path(image_name).stem
    input_dir = CROPS_DIR / image_id
    output_dir = OCR_DIR / image_id

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory не найден: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    all_files = list(input_dir.iterdir())
    total_files = len(all_files)
    print(f"[OCR] Найдено {total_files} crop-изображений для {image_id}")

    for i in range(0, total_files, batch_size):
        batch = all_files[i : i + batch_size]

        for img_path in batch:
            if not img_path.is_file() or img_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                continue

            out_file = output_dir / f"{img_path.stem}.json"
            if out_file.exists():
                continue

            try:
                results = reader.readtext(str(img_path), detail=1)

                if not results:
                    print(f"[WARN] Текст не найден: {img_path.name}")
                    continue

                processed = [(text, float(conf)) for (_, text, conf) in results]
                top3 = sorted(processed, key=lambda x: x[1], reverse=True)[:3]

                with open(out_file, "w", encoding="utf-8") as f:
                    json.dump(top3, f, ensure_ascii=False, indent=2)

                print(f"[OK] {img_path.name}: {top3}")

            except Exception as e:
                print(f"[ERROR] OCR не сработал для {img_path.name}: {e}")

            time.sleep(pause)

    print(f"[OCR] Готово: {image_id}")


if __name__ == "__main__":
    for folder in CROPS_DIR.iterdir():
        if folder.is_dir():
            run_ocr(folder.name)
