import cv2
import cv2.dnn_superres
import numpy as np
import time
import ctypes
import random
import math

from detector import PersonDetector
import db


counter = 1

def crop_image(image, coordinates):
    global counter

    crop = image[coordinates[1]:coordinates[3], coordinates[0]:coordinates[2]]
    cropped_path = f"prova{counter}.jpg"
    cv2.imwrite(cropped_path, crop)
    counter += 1

def main():
    # Initialize Variable
    video = cv2.VideoCapture(1)

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    observer = PersonDetector()
    database = db.DB()
    database.LoadDB()
    print(database)

    # Window options
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Game Variable
    screenshot = None
    screenshotBool = False

    while True:

        ret, frame = video.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))

        boxes = observer.detect_face(frame)

        for face in boxes:
            x1, y1, x2, y2 = map(int, face)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 200, 129), 2)

        if screenshotBool:
            for face in boxes:
                crop_image(frame, face)
            screenshotBool = False


        cv2.imshow("Statues Game", frame)

        key = cv2.waitKey(1)
        if key == 27:
            # Close program
            break
        if (key == ord('s') or key == ord('s')):
            screenshotBool = True


if __name__ == "__main__":
    main()