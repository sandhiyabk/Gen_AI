# -*- coding: utf-8 -*-
"""voice_reg(language).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1s__Xa4LNo7aFPCU1in9A12heXhHPEWv4
"""

import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ✅ Path to dataset
data_dir = "/content/drive/MyDrive/task1"  # Change this to your path

# ✅ Feature extraction function
def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, duration=3, offset=0.5)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        return np.mean(mfccs.T, axis=0)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# ✅ Load data
features = []
labels = []

for folder in os.listdir(data_dir):
    folder_path = os.path.join(data_dir, folder)
    if os.path.isdir(folder_path):
        language = folder.lower()
        for file in os.listdir(folder_path):
            if file.endswith(".mp3"):
                file_path = os.path.join(folder_path, file)
                feat = extract_features(file_path)
                if feat is not None:
                    features.append(feat)
                    labels.append(language)

# ✅ Convert to NumPy arrays
X = np.array(features)
y = np.array(labels)

# ✅ Train model
if len(X) > 0:
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
else:
    print("No valid features found.")

from google.colab import files
import numpy as np
import librosa

uploaded = files.upload()

# Feature extraction function (copied from the previous cell)
def extract_features(file_path):
    try:
        audio, sr = librosa.load(file_path, duration=3, offset=0.5)
        mfccs = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
        return np.mean(mfccs.T, axis=0)
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def predict_lan(audio_file):
    feature = extract_features(audio_file)
    if feature is not None:
        feature = feature.reshape(1,-1)
        # The 'model' variable is defined in the previous cell,
        # ensure that cell is run before this one.
        prediction = model.predict(feature)
        return prediction[0]
    else:
      return "could not process audio"

# Check if any files were uploaded
if uploaded:
    for fname in uploaded.keys():
        print(f"{fname}: {predict_lan(fname)}")
else:
    print("No files were uploaded.")