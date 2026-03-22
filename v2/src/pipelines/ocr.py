import json
from pathlib import Path

from paddleocr import PaddleOCR

from src.config import CROPS_DIR, OCR_DIR

ocr = PaddleOCR(lang="ar", use_angle_cls=True, use_gpu=False)


def run_ocr(image_name: str):
    image_id = Path(image_name).stem

    input_dir = CROPS_DIR / image_id
    output_dir = OCR_DIR / image_id

    if not input_dir.exists():
        raise FileNotFoundError(input_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    for img_path in input_dir.iterdir():
        if not img_path.is_file():
            continue

        result = ocr.ocr(str(img_path))

        processed = []
        for line in result:
            text = line[1][0]
            score = float(line[1][1])
            processed.append((text, score))

        top3 = sorted(processed, key=lambda x: x[1], reverse=True)[:3]

        out_file = output_dir / f"{img_path.stem}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(top3, f, ensure_ascii=False, indent=2)

    print(f"[OCR] Готово: {image_id}")
