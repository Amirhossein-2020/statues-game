import cv2
import ctypes
import threading

from deepface import DeepFace

import os
import sys
sys.path.append(os.path.abspath("."))
from lib import db, detector, recognition

### DOESN'T WORK ###

def main():
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    # Initialize Variable
    #video = cv2.VideoCapture("http://192.168.53.162:4747/video")
    video = cv2.VideoCapture(1)

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    global imgSaveCount

    observer = detector.PersonDetector()

    # Initialize database
    DB = db.DB()
    DB.LoadDB()

    # Window options
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Game Variable

    # * MUST HAVE VARIABLES FOR FACE RECOGNITION * #
    
    face_match = []
    faceRecognitionThread = threading.Thread()
    # database (initialized above)
    DBChanged = False

    # - - - - - - - - - - - - - - - - - - - - - - - #


    counter = 0 # "pseudo time"
    check = False # Invece di usare il counter, premo c e fa riconoscimento
    notRecognized = "Unknown"
    #DB.printAllDatabase()

    while True:

        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))

        boxes = observer.detect_face(frame)
        boxes = sorted(boxes, key=lambda b: b[0])

        ### MAIN PROGRAM ###
        if counter % 30:
            if not faceRecognitionThread.is_alive():
                faceRecognitionThread = threading.Thread(target=recognition.FaceDetection_AllInOne,
                                                         args=(DB, frame, face_match))
                faceRecognitionThread.start()
            
        for i in range(len(face_match)):
            if i < len(boxes):
                x1, y1, x2, y2 = map(int, boxes[i])

                # Rettangolo e nome sulla faccia face_match(if = true, else = false)
                if face_match[i] != False:
                    if face_match[-1] == "done" and DBChanged:
                        DBChanged = False
                        DB.UpdateDB()

                    cv2.putText(frame, face_match[i], (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                else:
                    if face_match[-1] == "done":
                        DB.saveFace(frame[y1:y2, x1:x2].copy())
                        DBChanged = True
                        face_match[i] = f"id{DB.lastUnkownPlayerId}"

                    cv2.putText(frame, notRecognized, (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.imshow("Statues Game", frame)
        counter += 1

        key = cv2.waitKey(1)
        if key == 27: #ESC
            break   # Close program

        elif (key == ord('c') or key == ord('C')):
            check = True    # Start recognition, N.B. not used

main()