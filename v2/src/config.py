from pathlib import Path

# Корень данных
DATA_DIR = Path("data")

# Уровни данных
RAW_DIR = DATA_DIR / "raw"
INTERIM_DIR = DATA_DIR / "interim"
PROCESSED_DIR = DATA_DIR / "processed"
ANNOTATIONS_DIR = DATA_DIR / "annotations"

# bbox этап
BBOX_DIR = INTERIM_DIR / "bboxes"
FILTERED_DIR = INTERIM_DIR / "filtered"

# csv (аннотации)
CSV_RAW_DIR = ANNOTATIONS_DIR / "raw"
CSV_FILTERED_DIR = ANNOTATIONS_DIR / "filtered"

# crops + OCR
CROPS_DIR = PROCESSED_DIR / "crops"
OCR_DIR = PROCESSED_DIR / "ocr"
