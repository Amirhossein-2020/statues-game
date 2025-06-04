import threading
import time
from lib.recognition import checkFace

# Funzione usata dal control Thread per gestire tutti i threads di checkface
def wait(Threads, Return):
    for t in Threads:
        if t.is_alive():
            t.join()
    Return[0] = True

# Non viene usata, inutile
def waiting_thread_function(event_obj):
    event_obj.wait()

# Funzione principale per la face recognition
def launch_face_threads(face_boxes, frame, DB, DBPlayerToCheck, face_match, Threads):
    for i, box in enumerate(face_boxes):
        x1, y1, x2, y2 = map(int, box)
        try:
            if not Threads[i].is_alive():
                Threads[i] = threading.Thread(
                    target=checkFace,
                    args=(frame[y1:y2, x1:x2].copy(), DB, DBPlayerToCheck, face_match, i),
                    daemon=True
                )
                Threads[i].start()
        except ValueError:
            pass

# Screen feedback per il giocatore
# In base alla fase del gioco, visualizza una scritta diversa su schermo
def get_state_text(game_state, last_state_change, moving_time, freezing_time, starting_state, control_thread_alive, control_thread_return):
    now = time.time()
    delta = int(abs(now - last_state_change))

    match game_state:
        case "moving":
            seconds_left = max(0, moving_time - delta)
            return f"{seconds_left}s MOVE"

        case "frozen":
            seconds_left = max(0, freezing_time - delta)
            return f"{seconds_left}s FREEZE"

        case "idle":
            if starting_state == 1:
                if control_thread_alive and not control_thread_return:
                    return "Creating players..."
                else:
                    seconds_left = max(0, 3 - delta)
                    return f"{seconds_left}..."
            else:
                return "Idle - Press S to start"

        case _:
            return "ROUND ENDED"