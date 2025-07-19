



# Install dependencies (run only once)
!pip install librosa

import os
import numpy as np
import librosa
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical

# Set your audio dataset path
data_dir = "/content/drive/MyDrive/kav"

# Function to extract MFCC features
def extract_features(file_path):
    try:
        audio, sample_rate = librosa.load(file_path, duration=3, offset=0.5)
        mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=13)
        return np.mean(mfccs.T, axis=0)
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

# Extract features and labels
features = []
labels = []

print(f"Checking directory: {data_dir}")
for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path):
        emotion = folder.split('_')[-1].lower()
        for filename in os.listdir(folder_path):
            if filename.endswith('.mp3'):
                file_path = os.path.join(folder_path, filename)
                print(f"Extracting from: {file_path}")
                feature = extract_features(file_path)
                if feature is not None:
                    features.append(feature)
                    labels.append(emotion)

# Convert to numpy arrays
x = np.array(features)
y = np.array(labels)

# Encode labels to integers
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

# Train/test split
x_train, x_test, y_train, y_test = train_test_split(x, y_categorical, test_size=0.2, random_state=42)

# Define Neural Network model
model = Sequential([
    Dense(128, activation='relu', input_shape=(x.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(y_categorical.shape[1], activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=30, batch_size=16, validation_data=(x_test, y_test))

# Save the model in .keras format
model.save("voice_emotion_model.keras")
print("Model saved as voice_emotion_model.keras")

from google.colab import files
uploaded = files.upload()

def predict_emotion(audio_file):
    feature = extract_features(audio_file)
    if feature is not None:
        feature = feature.reshape(1, -1)
        prediction = model.predict(feature)
        predicted_label = encoder.inverse_transform([np.argmax(prediction)])
        return predicted_label[0]
    else:
        return "Could not process audio"

# Run prediction on uploaded files
if uploaded:
    for fname in uploaded.keys():
        print(f"{fname}: {predict_emotion(fname)}")
else:
    print("No files were uploaded.")

from google.colab import files
uploaded = files.upload()

def predict_emotion(audio_file):
    feature = extract_features(audio_file)
    if feature is not None:
        feature = feature.reshape(1,-1)
        prediction = model.predict(feature)
        return prediction[0]
    else:
      return "could not process audio"

# Check if any files were uploaded
if uploaded:
    for fname in uploaded.keys():
        print(f"{fname}: {predict_emotion(fname)}")
else:
    print("No files were uploaded.")
