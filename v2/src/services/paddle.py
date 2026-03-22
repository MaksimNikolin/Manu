# Usage - python paddle_ocr_words.py cropped_boxes/test markup/test

import json
import logging
import os
from pathlib import Path

from paddleocr import PaddleOCR

# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

input_folder = Path("cropped_boxes/test")
output_folder = Path("markup/test")
output_folder.mkdir(parents=True, exist_ok=True)

# Проверяем словарь
rec_dict_path = (
    Path(os.environ["VIRTUAL_ENV"])
    / "lib/python3.11/site-packages/paddleocr/ppocr/utils/dict/arabic_dict.txt"
)
if not os.path.isfile(rec_dict_path):
    logging.error(f"Файл словаря не найден: {rec_dict_path}")
else:
    logging.info(f"Файл словаря найден ✅ {rec_dict_path}")

# Пути к моделям
det_model_path = "/Users/ggang/.paddleocr/whl/det/ml/Multilingual_PP-OCRv3_det_infer"
rec_model_path = "/Users/ggang/.paddleocr/whl/rec/arabic/arabic_PP-OCRv4_rec_infer"
cls_model_path = "/Users/ggang/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer"

# Инициализация OCR
logging.info("Инициализация PaddleOCR...")
ocr = PaddleOCR(
    lang="ar",
    use_angle_cls=True,
    det_model_dir=det_model_path,
    rec_model_dir=rec_model_path,
    cls_model_dir=cls_model_path,
    use_gpu=False,
    rec_char_dict_path=str(rec_dict_path),
)
logging.info("PaddleOCR готов ✅")

for img_path in input_folder.iterdir():
    if not img_path.is_file():
        continue

    try:
        logging.info(f"Обрабатываем {img_path.name}...")
        result = ocr.ocr(str(img_path))
        processed = []

        for line in result:
            text = line[1][0]
            score = float(line[1][1])
            processed.append((text, score))

        top3 = sorted(processed, key=lambda x: x[1], reverse=True)[:3]

        out_file = output_folder / f"{img_path.stem}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(top3, f, ensure_ascii=False, indent=2)

        logging.info(f"Готово: {img_path.name} -> {out_file.name}")

    except Exception as e:
        logging.error(f"OCR ошибка для {img_path.name}: {e}")
