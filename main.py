import cv2
import cv2.dnn_superres
import numpy as np
import time
import ctypes
import random
import math
import json
import os
import threading

from deepface import DeepFace

from detector import PersonDetector
import db


def save_image(image):
    cropped_path = f"TEMP.jpg"
    cv2.imwrite(cropped_path, image)

def crop_image(image, coordinates, save=False):
    crop = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]

    cropped_path = f"TEMP.jpg"
    cv2.imwrite(cropped_path, image)

    if save:    
        save_image(crop)
    else:
        return image

def checkFace(frame, databaseListPath, face_match, i):

    for path in databaseListPath:
        try:
            if DeepFace.verify(frame, path, model_name="Facenet512")["verified"]:
                face_match[i] = True
                break
            else:
                face_match[i] = False
        except:
            face_match[i] = False

def main():
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    # Initialize Variable
    video = cv2.VideoCapture("http://192.168.53.162:4747/video")

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    observer = PersonDetector()
    database = db.DB()
    database.LoadDB()
    #print(database)

    # Window options
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Game Variable
    screenshot = None
    screenshotBool = False
    state = "Unknown" 
    face_match = []
    counter = 0 # "pseudo time"

    while True:

        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))

        boxes = observer.detect_face(frame)

        # Se in webcam ci sono più persone che in face_match aumenta fino al numero di persone
        if len(boxes) > len(face_match):
            for i in range(len(face_match), len(boxes)):
                face_match.append(False)

        for i, face in enumerate(boxes):

            x1, y1, x2, y2 = map(int, face)
            
            if counter % 15 == 0:
                try:
                    threading.Thread(target=checkFace, args=(frame, database.imageListPath, face_match, i)).start()
                except ValueError:
                    pass

            if face_match[i]:
                cv2.putText(frame, "Giovanni", (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            else:
                cv2.putText(frame, state, (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        if screenshotBool:
            for face in boxes:
                crop_image(frame, face, True)
            screenshotBool = False


        cv2.imshow("Statues Game", frame)
        counter += 1

        key = cv2.waitKey(1)
        if key == 27: #ESC
            # Close program
            break
        if (key == ord('s') or key == ord('s')):
            screenshotBool = True


if __name__ == "__main__":
    main()