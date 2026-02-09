from ultralytics import YOLO
import cv2
model = YOLO("model/yolov8n.pt")

def detect_plate(img):
    results = model(img, conf=0.4)
    for r in results:
        for box in r.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            return img[y1:y2, x1:x2]
    return None




