import cv2
import cv2.dnn_superres
import numpy as np
from detector import PersonDetector
import time
import ctypes

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
    detector = PersonDetector()
    
    # Initialize Variable
    video = cv2.VideoCapture(0)

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
    game_state = "idle" # moving, frozen, idle, ended
    round_finished = False
    score = 0
    state_text = "Idle - Press S to start"

    ### MAIN PROGRAM ###
    while True:
        # Get frame of the webcam
        ret, frame = video.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))

        people = detector.detect_people(frame)
        #people = sorted(people, key=lambda b: b[0])

        if game_state != "idle":

            if game_state == "moving":
                # Moving phase lasts 3 seconds
                if time.time() - last_state_change > 3:
                    game_state = "frozen"
                    freeze_frame = frame.copy()
                    last_state_change = time.time()

            elif game_state == "frozen":
                # Frozen phase lasts 10 seconds
                if time.time() - last_state_change > 10:
                    game_state = "moving"
                    last_state_change = time.time()
            


            # Eliminate players if frozen and not already eliminated
            for i, box in enumerate(people):
                x1, y1, x2, y2 = map(int, box)
                key = tuple(map(int, box))
                player_id = f"P{i+1}"

                if game_state == "frozen" and key not in eliminated:
                    temp_score = detect_movement(freeze_frame, frame, box)
                    
                    if score < temp_score:
                        score = temp_score

                    if score > 4000:
                        eliminated.add(key)

                eliminated_flag = key in eliminated
                color = (0, 0, 255) if eliminated_flag else (0, 255, 0)
                status = "OUT" if eliminated_flag else "SAFE"
                label = f"{player_id} - {status}"

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

                # Display current state
                if game_state == "moving":
                    state_text = f"{3 - int(abs(time.time() - last_state_change))}s MOVE"
                elif game_state == "frozen":
                    state_text = f"{10 - int(abs(time.time() - last_state_change))}s FREEZE"
                else:
                    state_text = "ROUND ENDED" # THE GAME ENDS ONLY WHEN REMAINS 1 PERSON/Something else we come up with

        cv2.putText(frame, state_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, "Press R to restart - Esc to exit", (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)
        cv2.putText(frame, f'''Score: {score}''', (20, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow("Statues Game", frame)

        key = cv2.waitKey(1)
        if key == 27:
            # Close program
            break
        elif key == ord('r') or key == ord('R'):
            # Reset game variables
            eliminated.clear()
            game_state = "moving"
            round_finished = False
            last_state_change = time.time()
            score = 0
        elif key == ord('s') or key == ord('S'):
            # Start game
            game_state = "moving"
            last_state_change = time.time()
    
    video.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()