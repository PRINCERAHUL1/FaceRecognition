import cv2
import pickle
import numpy as np
import os
from datetime import datetime
import csv
import time
from win32com.client import Dispatch
from sklearn.neighbors import KNeighborsClassifier

# --- Text-to-Speech Function ---
def speak(text):
    speaker = Dispatch("SAPI.SpVoice")
    speaker.Speak(text)

# --- Load Data ---
# data_path = "data"
# model_path = os.path.join(data_path, "knn_model.pkl")
# faces_path = os.path.join(data_path, "faces_data.pkl")
# labels_path = os.path.join(data_path, "names.pkl")
# cascade_path = os.path.join(data_path, "haarcascade_frontalface_default.xml")
data_path = os.path.join(os.path.dirname(__file__), 'data')
model_path = os.path.join(data_path, 'knn_model.pkl')
faces_path = os.path.join(data_path, 'faces_data.pkl')
labels_path = os.path.join(data_path, 'names.pkl')
cascade_path = os.path.join(data_path, 'haarcascade_frontalface_default.xml')


if not (os.path.exists(faces_path) and os.path.exists(labels_path) and os.path.exists(model_path)):
    print("Required data files not found. Run add_faces.py first.")
    exit()

with open(faces_path, 'rb') as f:
    FACES = pickle.load(f)
with open(labels_path, 'rb') as f:
    LABELS = pickle.load(f)
with open(model_path, 'rb') as f:
    knn = pickle.load(f)

LABELS = np.array(LABELS)
FACES = np.array(FACES)

# --- Face Detector ---
facedetect = cv2.CascadeClassifier(cascade_path)
if facedetect.empty():
    print("Error loading Haar Cascade XML. Check the file path.")
    exit()

# --- Start Webcam ---
video = cv2.VideoCapture(0)
attendance_taken = set()
COL_NAMES = ['NAME', 'TIME']

print("Starting face recognition. Press 'o' to mark attendance, 'q' to quit.")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = facedetect.detectMultiScale(gray, 1.3, 5)

    k = cv2.waitKey(1)

    for (x, y, w, h) in faces:
        crop_img = frame[y:y+h, x:x+w]
        resized_img = cv2.resize(crop_img, (50, 50)).flatten().reshape(1, -1)

        prediction = knn.predict(resized_img)[0]

        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, str(prediction), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        if k == ord('o') and prediction not in attendance_taken:
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            attendance = [str(prediction), str(timestamp)]

            os.makedirs("Attendance", exist_ok=True)
            attendance_file = f"Attendance/Attendance_{date}.csv"

            if not os.path.exists(attendance_file):
                with open(attendance_file, "w", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
            else:
                with open(attendance_file, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(attendance)

            attendance_taken.add(prediction)
            speak(f"Attendance recorded for {prediction}")
            print(f"Attendance recorded for {prediction}")

    cv2.imshow("Face Recognition", frame)

    if k == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
