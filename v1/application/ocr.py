import easyocr

def get_text_from_image(path: str,
                        reader: easyocr.Reader) -> str:
    result = reader.readtext(path)

    result = " ".join([chunk[1] for chunk in result])

    return result