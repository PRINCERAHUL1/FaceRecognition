import cv2
import numpy as np
import os
import pickle
from sklearn.neighbors import KNeighborsClassifier

# Create data directory if not exists
os.makedirs('data', exist_ok=True)

# Load face detector
facedetect = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

if facedetect.empty():
    print("Error loading cascade file")
else:
    print("Cascade file loaded successfully")


# Start webcam
video = cv2.VideoCapture(0)

# Input name once
name = input("Enter Your Name: ")

face_data = []
count = 0
max_samples = 100

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = frame[y:y+h, x:x+w]
        resized_face = cv2.resize(face, (50, 50)).flatten()
        face_data.append(resized_face)

        # Display rectangle and count
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, str(count), (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

    cv2.imshow("Capturing Faces", frame)
    if cv2.waitKey(1) == ord('q') or count >= max_samples:
        break

video.release()
cv2.destroyAllWindows()

# Save data only if at least 100 faces collected
if len(face_data) >= max_samples:
    # Load previous data if exists
    if os.path.exists('data/faces_data.pkl'):
        with open('data/faces_data.pkl', 'rb') as f:
            faces = pickle.load(f)
        with open('data/names.pkl', 'rb') as f:
            labels = pickle.load(f)
    else:
        faces = []
        labels = []

    # Append new data
    for face in face_data:
        faces.append(face)
        labels.append(name)

    # Save updated data
    with open('data/faces_data.pkl', 'wb') as f:
        pickle.dump(faces, f)
    with open('data/names.pkl', 'wb') as f:
        pickle.dump(labels, f)

    # Train and save KNN model
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    with open('data/knn_model.pkl', 'wb') as f:
        pickle.dump(knn, f)

    print(f"Successfully collected {count} samples and trained the KNN model.")
else:
    print("Error: Collected fewer than 100 faces. Try again.")
