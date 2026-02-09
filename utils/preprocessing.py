import cv2
import numpy as np

def improve_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    denoise = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    contrast = clahe.apply(denoise)
    kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    sharp = cv2.filter2D(contrast, -1, kernel)
    return sharp


def correct_rotation(img):
    if img is None:
        return img
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if img.ndim == 3 else img
    _, bw = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    coords = np.column_stack(np.where(bw > 0))
    if coords.shape[0] < 5:
        return img
    angle = cv2.minAreaRect(coords.astype(np.float32))[-1]
    angle = -(90 + angle) if angle < -45 else -angle
    (h, w) = img.shape[:2]
    M = cv2.getRotationMatrix2D((w//2, h//2), angle, 1.0)
    return cv2.warpAffine(img, M, (w, h))



