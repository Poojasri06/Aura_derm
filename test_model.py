import numpy as np
from tensorflow.keras.models import load_model
from sklearn.metrics import accuracy_score, precision_score, recall_score

def test_model():
    # Load model and test data
    model = load_model('./models/deepfake_detector.h5')
    X_test = np.load('./data/X_test.npy')
    y_test = np.load('./data/y_test.npy')
    
    # Predict
    y_pred = (model.predict(X_test) > 0.5).astype(int).flatten()
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")

if __name__ == "__main__":
    test_model()