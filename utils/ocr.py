import easyocr
import pytesseract
import re
import numpy as np
reader = easyocr.Reader(['en', 'fr'])

def ocr_multi(img):
    texts = []
    results = reader.readtext(img)
    if results:
          #merged_text = merge_easyocr_blocks(results)
#         merged_text = clean_text(merged_text)
          fixed = enforce_plate_rules(results)
          if fixed:
               texts.append(fixed)
    tess = pytesseract.image_to_string(
        img,
        config="--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"
    )
    texts.append(tess)
    return texts


def clean_and_validate(texts):
    candidates = []
    for t in texts:
        t = t.upper()
        t = re.sub(r'[^A-Z0-9-]', '', t)
        if len(t) >= 4:
            candidates.append(t)
    return max(set(candidates), key=candidates.count) if candidates else "NON_DETECTE"


# Corrections OCR courantes
LETTER_FIX = {
    '0': 'O',
    '1': 'I',
    '5': 'S',
    '8': 'B',
    'U': 'M',
    'D': 'O' # cas fréquent sur plaques
}

DIGIT_FIX = {
    'O': '0',
    'D': '0',
    'I': '1',
    'S': '5',
    'B': '8'
}


# def clean_text(text):
#     text = text.upper()
#     text = re.sub(r'[^A-Z0-9-]', '', text)
#     return text


def enforce_plate_rules(text):

    if len(text) < 4:
        return None

    chars = list(text)

    # 2 premières lettres
    for i in [0, 1]:
        if chars[i].isdigit():
            chars[i] = LETTER_FIX.get(chars[i], chars[i])

    # Dernière lettre
    if chars[-1].isdigit():
        chars[-1] = LETTER_FIX.get(chars[-1], chars[-1])

    return ''.join(chars)


def merge_easyocr_blocks(results, x_threshold=50):
    """
    Fusionne les blocs OCR éloignés horizontalement
    """
    blocks = []

    for bbox, text, conf in results:
        x_coords = [p[0] for p in bbox]
        x_center = int(np.mean(x_coords))
        blocks.append((x_center, text))

    # Trier de gauche à droite
    blocks = sorted(blocks, key=lambda x: x[0])

    merged = blocks[0][1]
    last_x = blocks[0][0]

    for x, text in blocks[1:]:
        if abs(x - last_x) < x_threshold:
            merged += text
        else:
            merged += "-" + text  # séparation logique
        last_x = x

    return merged