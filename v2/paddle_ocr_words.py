# Usage - python paddle_ocr_words.py cropped_boxes/test markup/test

import sys
from pathlib import Path
from paddleocr import PaddleOCR
from tqdm import tqdm

TOP_K = 3


def get_images(folder):
    exts = {".png", ".jpg", ".jpeg", ".bmp"}
    return [p for p in sorted(folder.iterdir()) if p.suffix.lower() in exts]


def save_results(file_path, results):
    with open(file_path, "w", encoding="utf-8") as f:
        for i, (text, score) in enumerate(results[:TOP_K], 1):
            f.write(f"{i}. {text} {score:.4f}\n")


def process_batch(ocr, images, output_dir):
    try:
        results = ocr.ocr([str(img) for img in images], cls=True)

        for img_path, res in zip(images, results):
            out_file = output_dir / f"{img_path.stem}.txt"

            if not res:
                with open(out_file, "w") as f:
                    f.write("No text detected\n")
                continue

            parsed = [(line[1][0], line[1][1]) for line in res]

            parsed = sorted(parsed, key=lambda x: x[1], reverse=True)

            save_results(out_file, parsed)

    except Exception as e:
        print(f"Batch error: {e}")


def main(input_dir, output_dir, batch_size=16):

    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.exists():
        raise ValueError(f"Input folder not found: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    images = get_images(input_dir)

    print(f"Images found: {len(images)}")

    ocr = PaddleOCR(
        use_angle_cls=True,
        lang="ar",
        use_textline_orientation=True
    )

    for i in tqdm(range(0, len(images), batch_size)):

        batch = images[i:i + batch_size]

        process_batch(ocr, batch, output_dir)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        print("Usage: python paddle_ocr_words.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    main(input_folder, output_folder)