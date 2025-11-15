import cv2
import os
import numpy as np
from sklearn.model_selection import train_test_split

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

def preprocess_data(data_dir, output_dir):
    # Assuming Celeb-DF structure: data/Celeb-real and data/Celeb-synthesis
    real_dir = os.path.join(data_dir, 'Celeb-real')
    fake_dir = os.path.join(data_dir, 'Celeb-synthesis')
    
    X = []
    y = []
    
    # Process real videos
    if os.path.exists(real_dir):
        for video in os.listdir(real_dir)[:5]:  # Limit for demo
            if video.endswith('.mp4'):
                frames = extract_frames(os.path.join(real_dir, video))
                X.extend(frames)
                y.extend([0] * len(frames))  # 0 for real
    
    # Process fake videos
    if os.path.exists(fake_dir):
        for video in os.listdir(fake_dir)[:5]:  # Limit for demo
            if video.endswith('.mp4'):
                frames = extract_frames(os.path.join(fake_dir, video))
                X.extend(frames)
                y.extend([1] * len(frames))  # 1 for fake
    
    if not X:
        print("No videos found. Please check data directory.")
        return
    
    X = np.array(X) / 255.0  # Normalize
    y = np.array(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Save preprocessed data
    np.save(os.path.join(output_dir, 'X_train.npy'), X_train)
    np.save(os.path.join(output_dir, 'X_test.npy'), X_test)
    np.save(os.path.join(output_dir, 'y_train.npy'), y_train)
    np.save(os.path.join(output_dir, 'y_test.npy'), y_test)

if __name__ == "__main__":
    preprocess_data('./data', './data')