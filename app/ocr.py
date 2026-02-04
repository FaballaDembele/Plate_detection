import easyocr
import pytesseract
import re

reader = easyocr.Reader(['en', 'fr'])

def ocr_multi(img):
    texts = []
    for r in reader.readtext(img):
        texts.append(r[1])
    tess = pytesseract.image_to_string(
        img,
        config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    )
    texts.append(tess)
    return texts


def clean_and_validate(texts):
    candidates = []
    for t in texts:
        t = t.upper()
        t = re.sub(r'[^A-Z0-9-]', '', t)
        if len(t) >= 6:
            candidates.append(t)
    return max(set(candidates), key=candidates.count) if candidates else "NON_DETECTE"