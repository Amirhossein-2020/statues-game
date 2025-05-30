import cv2
import ctypes
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import threading

from deepface import DeepFace

import sys
sys.path.append(os.path.abspath("."))
from lib.detector import PersonDetector
from lib import db, recognition

def main():
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    # Initialize Variable
    #video = cv2.VideoCapture("http://192.168.53.162:4747/video")
    video = cv2.VideoCapture(1)

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    global imgSaveCount

    observer = PersonDetector()

    # Initialize database
    DB = db.DB()
    DB.LoadDB()

    # Window options
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Game Variable

    # * MUST HAVE VARIABLES FOR FACE RECOGNITION * #
    
    face_match = []
    Threads = []
    Thread = threading.Thread()
    # database (initialized above)
    DBChanged = False

    # - - - - - - - - - - - - - - - - - - - - - - - #

    counter = 0 # "pseudo time"
    create = False # Create ids
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

        # Se in webcam ci sono più persone che in face_match aumenta fino al numero di persone
        requiredSlot = len(boxes) - len(face_match)
        if requiredSlot > 0:
            face_match.extend([False] * requiredSlot)
            Threads.extend([threading.Thread()] * requiredSlot)

        #face_match = face_match[0:len(boxes)]
        if len(boxes) < len(face_match):
            for index in range(len(boxes), len(face_match)):
                face_match[index] = False
        
        '''
        # Un solo thread per tutte le facce funziona, ma lentino
        if counter % 30 == 0:
            try:
                if not Thread.is_alive():
                    Thread = threading.Thread(target=recognition.OneThreadCheckFace,
                                              args=(frame, DB.imageListPath, DB.playerList, face_match, boxes))
                    Thread.start()
            except ValueError:
                pass
        '''

        for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)

            
            if counter % 30 == 0:
                try:
                    if not Threads[i].is_alive():
                        Threads[i] = (threading.Thread(target=recognition.checkFace, 
                                                        args=(frame[y1:y2, x1:x2].copy(), DB.imageList, DB.playerList, face_match, i)))
                        Threads[i].start()

                except ValueError:
                    pass       
            

            # Rettangolo e nome sulla faccia face_match(if = true, else = false)
            if face_match[i] != False:
                if DBChanged:
                    DBChanged = False
                    DB.UpdateDB()

                cv2.putText(frame, face_match[i], (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
            else:
                if create:
                    DB.saveFace(frame[y1:y2, x1:x2].copy())
                    DBChanged = True
                    face_match[i] = f"id{DB.lastUnkownPlayerId}"

                cv2.putText(frame, notRecognized, (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        else:
            create = False

        cv2.imshow("Statues Game", frame)
        counter += 1

        key = cv2.waitKey(1)
        if key == 27: #ESC
            # Close program
            break
        elif (key == ord('c') or key == ord('C')):
            create = True # Create ids for unknown people


main()