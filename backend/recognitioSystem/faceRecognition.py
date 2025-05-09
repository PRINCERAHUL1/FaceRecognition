import sys
import cv2
import pickle
import numpy as np
from sklearn.neighbors import KNeighborsClassifier

# Get image path from command-line
image_path = sys.argv[1]

# Load data
with open('recognitionSystem/data/faces_data.pkl', 'rb') as f:
    faces = pickle.load(f)
with open('recognitionSystem/data/names.pkl', 'rb') as f:
    names = pickle.load(f)

# Train model
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(faces, names)

# Load and detect face
image = cv2.imread(image_path)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
facedetect = cv2.CascadeClassifier('recognitionSystem/data/haarcascade_frontalface_default.xml')
faces_rect = facedetect.detectMultiScale(gray, 1.3, 5)

for (x, y, w, h) in faces_rect:
    face = image[y:y+h, x:x+w]
    resized = cv2.resize(face, (50, 50)).flatten().reshape(1, -1)
    prediction = knn.predict(resized)
    print(prediction[0])  # Node.js reads this output
    break
