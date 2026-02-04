import streamlit as st
import requests
from PIL import Image

st.title("Test reconnaissance plaques 🇲🇱")

uploaded = st.file_uploader("Téléverser une image", type=["jpg","png"])

if uploaded:
    st.image(uploaded, caption="Image envoyée", use_column_width=True)
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