import os
import sys
import cv2
import ctypes

import numpy as np
#from deepface import DeepFace

sys.path.append(os.path.abspath("."))
from lib import db, detector, recognition
import threading

def main():
    
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    DB = db.DB()
    DB.LoadDB()
    '''
    video = cv2.VideoCapture(1)

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    observer = detector.PersonDetector()

    Thread = threading.Thread()
    Return = [False]

    counter = 0

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))

        boxes = observer.detect_face(frame)
        boxes = sorted(boxes, key=lambda b: b[0])

        x1, y1, x2, y2 = map(int, boxes[0])
        
        if not Thread.is_alive():
            Thread = threading.Thread(target=recognition.checkFace, 
                                    args=(frame[y1:y2, x1:x2].copy(), DB.imageList, DB.playerList, Return, 0),
                                    daemon=True)
            Thread.start()

        if Return[0]:
            cv2.putText(frame, Return[0], (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)
        else:
            cv2.putText(frame, "Not recognized", (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 3)

        cv2.imshow("Statues Game", frame)
        counter += 1
        key = cv2.waitKey(1)
        if key == 27: #ESC
            # Close program
            breakx
        '''
    
    DB.printAllDatabase()
    print(DB.audioListPath)

main()