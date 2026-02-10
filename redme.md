# 🚗 API de Reconnaissance de Plaques d’Immatriculation (ANPR)

Cette API permet d’extraire automatiquement le **numéro de plaque** à partir d’une image de véhicule.
Elle est optimisée pour les **plaques africaines (ex : Mali)**, y compris :

* plaques **1 ligne**

  erreurs OCR courantes (`0/O`, `U/M`, `D/O`, etc.)

---

## 🧠 Fonctionnalités

* 📸 Upload d’image via **requête POST**

* 🤖 OCR combiné **EasyOCR + Tesseract**

* 🔎 Validation intelligente du format de plaque

* 🚀 API rapide avec **FastAPI**

* 🐳 Déploiement avec **Docker + Uvicorn**

---

## 📁 Structure du projet

```
plate_api/
│
├── app/
│   ├── main.py                # Point d’entrée FastAPI           # 
│   ├──  model
│    ── Dockerfile
│             
│├── utils/
│   │   ├── ocr.py              # OCR EasyOCR + Tesseract
│   │   ├── detection.py      # Règles & validation plaques
│   │   └── preprocessing.py
├── requirements.txt
├── 
└── README.md
```

---

## ⚙️ Prérequis (sans Docker)

* Python **3.9+**
* Tesseract OCR installé

### 📌 Installation Tesseract

**Windows**

```
https://github.com/UB-Mannheim/tesseract/wiki
```

Ajouter le chemin dans le code ou dans les variables d’environnement.

**Linux**

```
sudo apt install tesseract-ocr
```

---

## 📦 Installation locale

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---

## ▶️ Lancer l’API (local)

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Accès API :

```
http://localhost:8000
```

Swagger UI :

```
http://localhost:8000/docs
```

---

## 🐳 Lancer avec Docker (recommandé)

### 1️⃣ Build de l’image

```bash
docker build -t plate-api .
```

### 2️⃣ Lancer le conteneur

```bash
docker run -p 8000:8000 plate-api
```

---

## 🔌 Endpoint principal

### POST `/scan`

**Description** :

> Reçoit une image et retourne le numéro de plaque détecté sous forme de texte

### 📤 Réponse JSON

```json
{
  "plate_number": "BM7749MD"
}
```

Si non détecté :

```json
{
  "plate_number": "NON_DETECTE"
}
```

---

## 🧪 Exemple avec cURL

```bash
curl -X POST "http://localhost:8000/api/v1/recognize" \
     -F "file=@plaque.jpg"
```

---

## 📱 Intégration Mobile

* Android : Retrofit / OkHttp
* Flutter : http / dio
* React Native : fetch / axios

➡️ L’API retourne **uniquement le texte de la plaque** (léger & rapide).

---

## 🛠️ Formats de plaques supportés

* `BM7749MD`
* `AB123CD`
* plaques **2 lignes** :

  ```
  BM
  7749 MD
  ```

---

## 🚀 Améliorations possibles

* Ajout score de confiance
* Sauvegarde image annotée
* Support multi-pays
* Authentification API

---

## 👨‍💻 Auteur

Projet conçu pour un **système ANPR professionnel** (YOLO + OCR + API)

👉 Prêt pour production, mobile & cloud.

---

💡 *Besoin d’une version avec YOLOv8 intégré ou d’un déploiement VPS ?*
