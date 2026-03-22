from pathlib import Path

import cv2
import pandas as pd

from src.config import (
    CSV_FILTERED_DIR,
    CSV_RAW_DIR,
    FILTERED_DIR,
    RAW_DIR,
)


def filter_narrow_bboxes(df, min_width):
    filtered = df[df["width"] >= min_width].copy()
    print(f"Удалено узких bbox: {len(df) - len(filtered)}")
    return filtered


def remove_nested_bboxes(df, overlap_threshold=0.7):
    keep_indices = []
    df = df.reset_index(drop=True)

    df["area"] = df["width"] * df["height"]
    df = df.sort_values(by="area", ascending=False).reset_index(drop=True)

    for i, row_i in df.iterrows():
        x1_i, y1_i, w_i, h_i = row_i["left"], row_i["top"], row_i["width"], row_i["height"]
        x2_i, y2_i = x1_i + w_i, y1_i + h_i
        area_i = w_i * h_i

        nested = False

        for j, row_j in df.iterrows():
            if i == j:
                continue

            x1_j, y1_j, w_j, h_j = row_j["left"], row_j["top"], row_j["width"], row_j["height"]
            x2_j, y2_j = x1_j + w_j, y1_j + h_j

            xi1 = max(x1_i, x1_j)
            yi1 = max(y1_i, y1_j)
            xi2 = min(x2_i, x2_j)
            yi2 = min(y2_i, y2_j)

            inter_area = max(0, xi2 - xi1) * max(0, yi2 - yi1)

            if inter_area / area_i >= overlap_threshold:
                nested = True
                break

        if not nested:
            keep_indices.append(i)

    return df.loc[keep_indices].drop(columns=["area"]).reset_index(drop=True)


def filter_bboxes(image_name: str):
    image_path = RAW_DIR / image_name
    csv_input = CSV_RAW_DIR / f"{Path(image_name).stem}.csv"

    if not image_path.exists():
        raise FileNotFoundError(image_path)
    if not csv_input.exists():
        raise FileNotFoundError(csv_input)

    df = pd.read_csv(csv_input)

    print(f"Всего bbox: {len(df)}")

    # --- height filtering ---
    Q1 = df["height"].quantile(0.25)
    Q3 = df["height"].quantile(0.75)
    IQR = Q3 - Q1

    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    filtered = df[(df["height"] >= lower) & (df["height"] <= upper)]

    # --- additional filters ---
    filtered = filter_narrow_bboxes(filtered, min_width=15)
    filtered = remove_nested_bboxes(filtered)

    # --- save CSV ---
    CSV_FILTERED_DIR.mkdir(parents=True, exist_ok=True)
    csv_output = CSV_FILTERED_DIR / f"{Path(image_name).stem}.csv"
    filtered.to_csv(csv_output, index=False)

    # --- draw image ---
    image = cv2.imread(str(image_path))

    FILTERED_DIR.mkdir(parents=True, exist_ok=True)
    output_image = FILTERED_DIR / f"{Path(image_name).stem}.jpg"

    for _, row in filtered.iterrows():
        x, y, w, h = int(row.left), int(row.top), int(row.width), int(row.height)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imwrite(str(output_image), image)

    print(f"[FILTER] CSV: {csv_output}")
    print(f"[FILTER] Image: {output_image}")
