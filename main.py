import cv2
import cv2.dnn_superres
import numpy as np
from lib.detector import PersonDetector
import time
import ctypes
import random
import math
#Function that detect movement based on keypoints
def detect_keypoint_movement(kpts1, kpts2):
    for pid in range(len(kpts1)):
        for kp in range(17):
            if kp not in [2,3]:
                x1, y1, isvis1 = kpts1[pid][kp]
                x2, y2, isvis2 = kpts2[pid][kp]
                if int(isvis1 * 100) > 80 or int(isvis2 * 100) > 75:
                    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                    if distance > 90:
                        print(f"Keypoint who has moved: {kp} \n Edit distance = {distance} \n Freezing point: {x1, y1} \n Actual point: {x2, y2}")
                        return True
    

    return False

def detect_movement(prev, curr, box):
        x1, y1, x2, y2 = map(int, box)
        region1 = prev[y1:y2, x1:x2]
        region2 = curr[y1:y2, x1:x2]
        if region1.shape != region2.shape or region1.size == 0:
            return 0
        diff = cv2.absdiff(region1, region2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        score = np.sum(thresh) / 255
        return score

def main():

    rng = np.random.RandomState(42)
    detector = PersonDetector()
    
    # Initialize Variable
    video = cv2.VideoCapture(1)

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    # Window options
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    #cv2.namedWindow("TMPR", cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty("TMPR", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Pre-game variable
    eliminated = set()
    freeze_frame = None
    freeze_keypoints = None
    game_state = "idle" # moving, frozen, idle, ended
    round_finished = False
    score = 0
    starting_state = 0 #0: Start button not pressed | 1: Start button pressed | 2: Start button pressed and waiting time finished
    state_text = "Idle - Press S to start"
    moving_time = random.randint(10,15)    
    freezing_time = random.randint(5,8)
    INTERVAL_TIME = 0.8

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
        face_boxes = faceDetector.detect_face(frame)

        # Timing
        x1, y1, x2, y2 = map(int, face_boxes[0])
        cv2.rectangle(frame, (x1, y1), (x2, y2), (50, 200, 129), 2)

        if game_state != "idle":

            if game_state == "moving":

                # Moving phase lasts 3 seconds
                if time.time() - last_state_change > moving_time:
                    game_state = "frozen"
                    freeze_frame = frame.copy()
                    freeze_keypoints = people_keypoints
                    last_state_change = time.time()

            elif game_state == "frozen":

                # Frozen phase lasts 10 seconds
                if time.time() - last_state_change > freezing_time + INTERVAL_TIME:    
                    game_state = "moving"
                    moving_time = random.randint(10,15)    
                    freezing_time = random.randint(5,8)
                    last_state_change = time.time()
            


            # Players Management
            if len(people_boxes) > 0 and len(people_keypoints) > 0:

                for i, keypoint in enumerate(people_keypoints):
                    player_id = f"P{i+1}"
                    if len(people_boxes) > 0:
                        x1, y1, x2, y2 = map(int, people_boxes[i])
                        keybox = tuple(map(int, people_boxes[i]))
                    
                    # Eliminate players if frozen and not already eliminated

                        if game_state == "frozen" and keybox not in eliminated and time.time() - last_state_change > INTERVAL_TIME:
                        #is_moving = detect_keypoint_movement(freeze_keypoints, people_keypoints)
                            score = detect_movement(freeze_frame, frame, people_boxes[i])
                            if score > 16500 or detect_keypoint_movement(freeze_keypoints, people_keypoints):
                                eliminated.add(keybox)
                            

                    eliminated_flag = keybox in eliminated
                    color = (0, 0, 255) if eliminated_flag else (0, 255, 0)
                    status = "OUT" if eliminated_flag else "SAFE"
                    label = f"{player_id} - {status}"

                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    for k in keypoint:
                        x,y,iv = k
                        cv2.circle(frame, (int(x),int(y)), 3, color, -1)
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # Display current state

             
            if game_state == "moving":
                state_text = f"{moving_time - int(abs(time.time() - last_state_change))}s MOVE"
            elif game_state == "frozen":
                state_text = f"{freezing_time - int(abs(time.time() - last_state_change))}s FREEZE"
            else:
                state_text = "ROUND ENDED" 

        # Waiting time before going to "moving" phase
        if game_state == "idle" and starting_state == 1:
            waiting_time_to_start = time.time() - last_state_change
            
            if  waiting_time_to_start > 3:
                game_state = "moving"

            state_text = f"{3 - int(abs(waiting_time_to_start))}..."

        # Fixed screen values
        cv2.putText(frame, state_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, "Press R to restart - Esc to exit", (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.putText(frame, f'''Score: {score}''', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # 3 seconds of preparation before game starts
        
            

        cv2.imshow("Statues Game", frame)

        key = cv2.waitKey(1)
        if key == 27: # ESC
            # Close program
            break
        elif (key == ord('r') or key == ord('R')) and game_state != "idle":
            # Reset game variables
            eliminated.clear()
            game_state = "moving"
            round_finished = False
            last_state_change = time.time()
            score = 0
        elif key == ord('s') or key == ord('S') and game_state == "idle":
            starting_state = 1
            # Start game after 3 seconds:
            last_state_change = time.time()
    
    video.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()