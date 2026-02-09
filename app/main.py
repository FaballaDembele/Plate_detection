from fastapi import FastAPI, UploadFile, File
import numpy as np
import cv2

from utils.preprocessing import improve_image,correct_rotation
from utils.detection import detect_plate
from utils.ocr import ocr_multi,clean_and_validate
from fastapi import FastAPI, UploadFile, File
from   utils.detection import detect_plate
# from utils.detection import detect_plate_fallback
app = FastAPI(title="API Reconnaissance Plaques")

@app.get("/",
         summary="Point de départ de l'API",
         description="Bienvenue à l'API de detection de plaque. Utilisez le point de terminaison /scan pour scanner la plaque.",
            response_description="Message de bienvenue",
            operation_id="health_check",
            tags=["Général"]
         )

async def root():
    return {"message": "Bienvenue à l'API de "}


@app.post("/scan")
async def scan_plate(file: UploadFile = File(...)):
    image_bytes = await file.read()
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    improved = improve_image(img)
    plate = detect_plate(img)
    if plate is None:
       plate = improved


    texts = ocr_multi(plate)
    final_text = clean_and_validate(texts)

    return {
        
        "texts_detectes": texts,
        "plaque": final_text,
    }
