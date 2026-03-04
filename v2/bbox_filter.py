# Usage - python bbox_filter.py original/test.jpg

import pandas as pd
import cv2
import sys
from pathlib import Path
import os


def ensure_dirs():
    os.makedirs("filtered", exist_ok=True)
    os.makedirs("csvs_filtered", exist_ok=True)


def filter_narrow_bboxes(df, min_width):
    filtered = df[df['width'] >= min_width].copy()
    print(f"Удалено узких bbox (<{min_width}): {len(df) - len(filtered)}")
    return filtered


def remove_nested_bboxes(df, overlap_threshold=0.7):
    keep_indices = []
    df = df.reset_index(drop=True)

    df['area'] = df['width'] * df['height']
    df = df.sort_values(by='area', ascending=False).reset_index(drop=True)

    for i, row_i in df.iterrows():
        x1_i, y1_i, w_i, h_i = row_i['left'], row_i['top'], row_i['width'], row_i['height']
        x2_i, y2_i = x1_i + w_i, y1_i + h_i
        area_i = w_i * h_i

        nested = False

        for j, row_j in df.iterrows():
            if i == j:
                continue

            x1_j, y1_j, w_j, h_j = row_j['left'], row_j['top'], row_j['width'], row_j['height']
            x2_j, y2_j = x1_j + w_j, y1_j + h_j

            xi1 = max(x1_i, x1_j)
            yi1 = max(y1_i, y1_j)
            xi2 = min(x2_i, x2_j)
            yi2 = min(y2_i, y2_j)

            inter_w = max(0, xi2 - xi1)
            inter_h = max(0, yi2 - yi1)
            inter_area = inter_w * inter_h

            if inter_area / area_i >= overlap_threshold:
                nested = True
                break

        if not nested:
            keep_indices.append(i)

    filtered = df.loc[keep_indices].drop(columns=["area"]).reset_index(drop=True)
    print(f"Удалено вложенных bbox: {len(df) - len(filtered)}")
    return filtered


def filter_bboxes(image_name, min_width=15):
    ensure_dirs()

    image_name = Path(image_name)

    original_image_path = Path("original") / image_name.name
    csv_input_path = Path("csvs_original") / f"{image_name.stem}.csv"

    if not original_image_path.exists():
        raise FileNotFoundError(f"Не найдено изображение: {original_image_path}")

    if not csv_input_path.exists():
        raise FileNotFoundError(f"Не найден CSV: {csv_input_path}")

    df = pd.read_csv(csv_input_path)

    print(f"Всего боксов: {len(df)}")

    Q1 = df['height'].quantile(0.25)
    Q3 = df['height'].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    filtered = df[(df['height'] >= lower) & (df['height'] <= upper)]
    print(f"После фильтрации по height: {len(filtered)}")

    filtered = filter_narrow_bboxes(filtered, min_width)
    filtered = remove_nested_bboxes(filtered)

    csv_output = Path("csvs_filtered") / f"{image_name.stem}_filtered.csv"
    filtered.to_csv(csv_output, index=False)
    print(f"Filtered CSV сохранён: {csv_output}")

    image = cv2.imread(str(original_image_path))

    for _, row in filtered.iterrows():
        x, y, w, h = int(row.left), int(row.top), int(row.width), int(row.height)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    output_image = Path("filtered") / f"{image_name.stem}_filtered.jpg"
    cv2.imwrite(str(output_image), image)

    print(f"Filtered изображение сохранено: {output_image}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python bbox_filter.py test.jpg")
        sys.exit(1)

    filter_bboxes(sys.argv[1])