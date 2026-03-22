import sys
from pathlib import Path

from src.pipelines import bbox, crop, filter, ocr

if len(sys.argv) != 2:
    print("Использование: python run_pipeline.py <image_file>")
    sys.exit(1)

image_path = Path(sys.argv[1])

print("[BBOX] Старт OCR bbox...")
bbox.process_image(image_path)

print("[FILTER] Старт фильтрации bbox...")
filter.filter_bboxes(image_path)

print("[CROP] Старт кропа bbox...")
crop.crop_bboxes(image_path)

print("[OCR] Старт PaddleOCR...")
ocr.run_ocr(image_path)
