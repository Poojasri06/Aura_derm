import streamlit as st
import cv2
import numpy as np
from tensorflow.keras.models import load_model
import tempfile
import os

def extract_frames(video_path, num_frames=10):
    cap = cv2.VideoCapture(video_path)
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    step = max(1, total_frames // num_frames)
    for i in range(0, total_frames, step):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (224, 224))
            frames.append(frame)
        if len(frames) >= num_frames:
            break
    cap.release()
    return frames

def predict_video(video_path):
    model = load_model('./models/deepfake_detector.h5')
    frames = extract_frames(video_path)
    if not frames:
        return "Unable to process video", 0.0
    
    frames = np.array(frames) / 255.0
    predictions = model.predict(frames)
    avg_prediction = np.mean(predictions)
    label = "Fake" if avg_prediction > 0.5 else "Real"
    confidence = avg_prediction if avg_prediction > 0.5 else 1 - avg_prediction
    return label, confidence

st.title("Deepfake Video Detector")

uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name
    
    st.video(uploaded_file)
    
    if st.button("Detect Deepfake"):
        with st.spinner("Analyzing video..."):
            label, confidence = predict_video(tmp_path)
        
        st.success(f"Prediction: {label}")
        st.info(f"Confidence: {confidence:.2f}")
    
    # Clean up temp file
    os.unlink(tmp_path)