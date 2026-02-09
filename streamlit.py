import streamlit as st
import requests
from PIL import Image

st.title("Test reconnaissance plaques 🇲🇱")

uploaded = st.file_uploader("Téléverser une image", type=["jpg","png","webp","jpeg"])

if uploaded:
    st.image(uploaded, caption="Image envoyée", width=700)
    if st.button("Scanner la plaque"):
        response = requests.post(
            "http://127.0.0.1:8000/scan",
            files={"file": uploaded.getvalue()}
        )
        if response.status_code == 200:
            data = response.json()
            st.success(f"Plaque détectée : {data['plaque']}")
            st.write(data)
        else:
            st.error("Erreur API")

# import streamlit as st
# import requests

# st.title("ANPR - Reconnaissance de plaque")

# img = st.file_uploader("Uploader une image", type=["jpg","png","jpeg"])

# if img:
#     st.image(img)
#     if st.button("Reconnaître"):
#         response = requests.post(
#             "http://localhost:8000/scan",
#             files={"file": img.getvalue()}
#         )
#         st.success(f"Plaque détectée : {response.json()['plate']}")
