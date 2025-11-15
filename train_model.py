import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam

def build_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    # Load preprocessed data
    X_train = np.load('./data/X_train.npy')
    y_train = np.load('./data/y_train.npy')
    
    model = build_model()
    model.fit(X_train, y_train, epochs=5, batch_size=16, validation_split=0.2)  # Reduced epochs for demo
    
    # Save model
    model.save('./models/deepfake_detector.h5')
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()