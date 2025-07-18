import streamlit as st
from PIL import Image

st.title("📸 Webcam Camera Test")

camera_image = st.camera_input("Take a selfie")

if camera_image:
    img = Image.open(camera_image)
    st.image(img, caption="This is your captured photo!")
else:
    st.warning("📷 No image captured. Make sure your camera is working.")
