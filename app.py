from pathlib import Path

import streamlit as st
from PIL import Image

from model import Model

st.set_page_config(page_title="Mbaza Streamlit Interface")


@st.cache_resource
def get_model():
    return Model("gabon.onnx")


model = get_model()

"# Mbaza Streamlit Interface"
"By [Appsilon](https://appsilon.com/) with ❤️"
"---"
"This app is a simple showcase of how to run [Mbaza](https://appsilon.com/data-for-good/mbaza-ai/) ONNX model in `streamlit`."
"To use the uploaded image, select `Upload your own` option."

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

options = ["Upload your own"] + sorted(Path("images").glob("*.jpg"))
selected_predefined_image = st.selectbox("Or select a predefined image", options)

img = None
if uploaded_file and selected_predefined_image == "Upload your own":
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)
if selected_predefined_image is not None and selected_predefined_image != "Upload your own":
    img = Image.open(selected_predefined_image)
    st.image(img, caption=f"Predefined {selected_predefined_image}", use_column_width=True)

if img:
    label, confidence = model.predict(img)
    f"Classification: {label}"
    f"Confidence: {confidence:.2f}"
