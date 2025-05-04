import cv2
import numpy as np
from detector import PersonDetector
import time
def main():
    
    detector = PersonDetector()
    cap = cv2.VideoCapture(0)
    # Make the window fullscreen
    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    eliminated = set()
    freeze_frame = None
    game_state = "moving"  # Start in "moving"
    STATE_DURATION = 10
    last_state_change = time.time()
    round_finished = False

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

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        people = detector.detect_people(frame)
        people = sorted(people, key=lambda b: b[0])

        # Game state management: move -> freeze -> end
        if not round_finished and time.time() - last_state_change > STATE_DURATION:
            if game_state == "moving":
                game_state = "frozen"
                freeze_frame = frame.copy()
                last_state_change = time.time()
            elif game_state == "frozen":
                game_state = "ended"
                round_finished = True

        # Eliminate players if frozen and not already eliminated
        for i, box in enumerate(people):
            x1, y1, x2, y2 = map(int, box)
            key = tuple(map(int, box))
            player_id = f"P{i+1}"

            if game_state == "frozen" and key not in eliminated:
                score = detect_movement(freeze_frame, frame, box)
                if score > 1500:
                    eliminated.add(key)

            eliminated_flag = key in eliminated
            color = (0, 0, 255) if eliminated_flag else (0, 255, 0)
            status = "OUT" if eliminated_flag else "SAFE"
            label = f"{player_id} - {status}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # Display current state
        if game_state == "moving":
            state_text = f"{STATE_DURATION - int(abs(time.time() - last_state_change))}s MOVE"
        elif game_state == "frozen":
            state_text = f"{STATE_DURATION - int(abs(time.time() - last_state_change))}s FREEZE"
        else:
            state_text = "ROUND ENDED"

        cv2.putText(frame, state_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, "Press R to restart - Esc to exit", (20, 470), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

        cv2.imshow("Statues Game", frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC
            break
        elif key == ord('r') or key == ord('R'):
            eliminated.clear()
            game_state = "moving"
            round_finished = False
            last_state_change = time.time()

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()