import cv2
import numpy as np
import time
import ctypes
import random
import threading
import os

from lib.detector import PersonDetector, MovementDetector
from lib import db
from lib.utils import wait, waiting_thread_function, launch_face_threads, get_state_text
from lib.sound import SoundManager

def main():
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    rng = np.random.RandomState(42)
    detector = PersonDetector()


    # Window options
    video = cv2.VideoCapture(0)
    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #Initializing database
    DB = db.DB()
    DB.LoadDB()

    # Sound Manager
    sound_manager = SoundManager(DB)
    sound_manager.play("idle", loop=True)

    # Pre-game variables
    freeze_frame = None
    freeze_keypoints = None
    game_state = "idle" # idle, moving, frozen, ended
    score = 0
    starting_state = 0 #0: Start button not pressed | 1: Start button pressed | 2: Start button pressed and waiting time finished
    state_text = "Idle - Press S to start"
    moving_time = 10   
    freezing_time = random.randint(5,8)
    INTERVAL_TIME = 0.8
    eliminated = []
    initialPlayerRemain = 0
    playerRemain = 0
    playerRemainList = []
    playerPlaying = []
    DBPlayerToCheck = DB.playerList
    notRecognized = "Unknown"
    last_state_change = time.time()
    
    # Face recognition variables
    face_match = []
    startRecognition = False
    Threads = []
    event_obj = threading.Event()

    waitingThread = threading.Thread(target= waiting_thread_function,
                                     args=(event_obj, ),
                                     daemon=True)
    
    ControlThreadReturn = [False]
    ControlThread = threading.Thread(target=wait,
                                     args=(Threads, ControlThreadReturn, ),
                                     daemon= True)
    counter = 1

    oneTimeRecognition = True
    oneTimeThreadControl = True

    ### MAIN PROGRAM ###
    while True:
        # Get frame of the webcam
        ret, frame = video.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))

        people_boxes, people_keypoints = detector.detect_people(frame)
        people_boxes = sorted(people_boxes, key=lambda b: b[0])
        face_boxes = detector.detect_face(frame)
        face_boxes = sorted(face_boxes, key=lambda b: b[0])
        
        # If there are more people in webcam comparing to face_match, increase until they are equal
        requiredSlot = len(face_boxes) - len(face_match)
        if requiredSlot > 0:
            face_match.extend([notRecognized] * requiredSlot)
            Threads.extend([threading.Thread()] * requiredSlot)


        if starting_state != 1:
            
            #face_match = face_match[0:len(boxes)]
            if len(face_boxes) < len(face_match):
                for index in range(len(face_boxes), len(face_match)):
                    face_match[index] = notRecognized

            if game_state == "idle":
                initialPlayerRemain = len(face_boxes)
 
                if (counter % 20 == 0):
                    launch_face_threads(face_boxes, frame, DB, DBPlayerToCheck, face_match, Threads)
        

        # Timing
        if game_state != "idle":

            if game_state == "moving":
                # Moving phase lasts 10 to 13 seconds
                if time.time() - last_state_change > moving_time:
                    game_state = "frozen"
                    sound_manager.play(game_state)
                    freeze_frame = frame.copy()
                    freeze_keypoints = people_keypoints
                    last_state_change = time.time()

            elif game_state == "frozen":
                # Frozen phase lasts between 5 to 8 seconds
                if time.time() - last_state_change > freezing_time + INTERVAL_TIME:    
                    game_state = "moving"
                    sound_manager.play(game_state)
                    moving_time = random.randint(10,15)    
                    freezing_time = random.randint(5,8)
                    last_state_change = time.time()
            
            # Face Recognition Management
            if ControlThreadReturn[0]:
                if len(face_boxes) != playerRemain:
                    startRecognition = True
                
                if startRecognition & (len(face_boxes) == playerRemain):
                    launch_face_threads(face_boxes, frame, DB, DBPlayerToCheck, face_match, Threads)
                    startRecognition = False
                
            # Players Management
            if len(people_boxes) > 0 and len(people_keypoints) > 0:
                for i, keypoint in enumerate(people_keypoints):
                    if i < len(face_boxes):
                        player_id = face_match[i]
                        x1, y1, x2, y2 = map(int, people_boxes[i])
                        # Eliminate players if frozen and not already eliminated
                        if game_state == "frozen" and player_id not in eliminated and time.time() - last_state_change > INTERVAL_TIME:
                            is_moving = MovementDetector.detect_keypoint_movement(freeze_keypoints, people_keypoints)
                            score = MovementDetector.detect_movement(freeze_frame, frame, people_boxes[i])
                            if score > 16500 or is_moving:
                                eliminated.append(face_match[i])
                                playerRemain -= 1
                                sound_manager.play("eliminated")
                                
                        
                        eliminated_flag = player_id in eliminated
                        color = (0, 0, 255) if eliminated_flag else (0, 255, 0)
                        status = "OUT" if eliminated_flag else "SAFE"
                        label = f"{player_id} - {status}"
                        
                        if player_id in playerPlaying or "Not in database":
                            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                            for k in keypoint:
                                x,y,iv = k
                                cv2.circle(frame, (int(x),int(y)), 3, color, -1)
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        # Waiting time before going to "moving" phase
        if game_state == "idle" and starting_state == 1:

            if oneTimeThreadControl:
                ControlThread.start()
                oneTimeThreadControl = False
                
            if ControlThreadReturn[0]:
                if oneTimeRecognition:
                    oneTimeRecognition = False
                
                    for i, box in enumerate(face_boxes):
                        if face_match[i] == "Not in database":
                            x1, y1, x2, y2 = map(int, box)
                            DB.saveFace(frame[y1:y2, x1:x2].copy())
                            face_match[i] = f"id{DB.lastUnknownPlayerId}"
                
                    playerPlaying = face_match.copy()
                    DB.UpdateDB()
                    last_state_change = time.time()
                
                waiting_time_to_start = time.time() - last_state_change
                if waiting_time_to_start == 0:
                    sound_manager.play("countdown")

                if  (waiting_time_to_start > 3):
                    game_state = "moving"
                    sound_manager.play(game_state)
                    playerRemain = len(face_boxes)
                    initialPlayerRemain = playerRemain
                    playerRemainList = face_match[0:playerRemain].copy()
                    DBPlayerToCheck = DB.playerList
                

        # Fixed screen values drawing on frame
        state_text = get_state_text(
            game_state,
            last_state_change,
            moving_time,
            freezing_time,
            starting_state,
            ControlThread.is_alive() if ControlThread else False,
            ControlThreadReturn[0]
        )
        cv2.putText(frame, state_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, f'''Score: {score}''', (win_x-300, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        if starting_state == 0:
            cv2.putText(frame, "Press S to start", (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            cv2.putText(frame, "Press R to restart", (20, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
            cv2.putText(frame, "Esc to exit", (20, 510), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        # 3 seconds of preparation before game starts

        for i, box in enumerate(face_boxes):
            if i < initialPlayerRemain:
                x1, y1, x2, y2 = map(int, box)
                cv2.putText(frame, face_match[i], (x1,y1-20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

        cv2.imshow("Statues Game", frame)
        counter += 1
        print(counter)

        key = cv2.waitKey(1)
        if key == 27: # ESC
            # Close program
            break
        elif (key == ord('r') or key == ord('R')) and game_state != "idle":
            # Reset game variables
            if ControlThread.is_alive():
                ControlThread.join(timeout=1)
            game_state = "idle"
            sound_manager.play("idle", loop=True)
            score = 0
            starting_state = 0
            last_state_change = time.time()
            playerRemain = 0
            face_match = []
            eliminated = []
            oneTimeRecognition = True
            oneTimeThreadControl = True
            ControlThreadReturn[0] = False
            ControlThread = threading.Thread(target=wait, args=(Threads, ControlThreadReturn,), daemon=True)
        elif key == ord('s') or key == ord('S') and game_state == "idle":
            starting_state = 1
            # Start game after 3 seconds:
    
    video.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()