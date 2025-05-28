from deepface import DeepFace
import threading

from lib.detector import PersonDetector
from lib import utils

# Game Variable
Threads = []

observer = PersonDetector()

# The return of this fuction is in face_match, sarà false di base, se trova faccia cambia il false con il nome della persona identificata
def FaceDetection_AllInOne(Database, frame, face_match): 

    global Threads
    DBChanged = False


    boxes = observer.detect_face(frame)
    boxes = sorted(boxes, key=lambda b: b[0])

    # Se in webcam ci sono più persone che in face_match aumenta fino al numero di persone
    requiredSlot = len(boxes) - len(face_match)
    if requiredSlot > 0:
        face_match.extend([False] * requiredSlot)
        Threads.extend([threading.Thread()] * requiredSlot)

    #face_match = face_match[0:len(boxes)]

    # Se ho meno persone in webcam rispetto a face_match, metti false le persone da non controllare
    if len(boxes) < len(face_match):
        for index in range(len(boxes), len(face_match)):
            face_match[index] = False

    ### MAIN PROGRAM ###
    for i, box in enumerate(boxes):
            x1, y1, x2, y2 = map(int, box)

            try:
                if not Threads[i].is_alive():
                    Threads[i] = (threading.Thread(target=checkFace, 
                                                    args=(frame[y1:y2, x1:x2].copy(), Database.imageListPath, face_match, i)))
                    Threads[i].start()

            except ValueError:
                pass
    
    for t in Threads:
        if t.is_alive():
            t.join()
    
    face_match.extend("done")

def OneThreadCheckFace(frame, imageListPath, keys, faceMatch, boxes):
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)

        try:
            for key in keys:
                for path in imageListPath[key]:
                    result = DeepFace.verify(frame[y1:y2, x1:x2], path)

                    print(f"distance: {result["distance"]}, thresold: {result["threshold"]}, Person: {i}, db_img: {path}")

                    # Exit from path for
                    if result["verified"]:
                        faceMatch[i] = key
                        break

                    # Se la % che non sia la persona della cartella è alta, cambia cartella (change key)
                    if result["distance"] > 0.68: 
                        break
                
                # Exit from key for
                if result["verified"]:
                    break
            else:
                faceMatch[i] = False

        except:
            pass


def checkFace(imgToCompare, imageListPath, keys, faceMatch, i):

    try:
        if faceMatch[i] is not False:
            key = faceMatch[i]

            for path in imageListPath[key]:
                    result = DeepFace.verify(imgToCompare, path, model_name="Facenet")

                    print(f"distance: {result["distance"]}, thresold: {result["threshold"]}, Person: {i}, db_img: {path}, fast way.")

                    if result["verified"]:
                        faceMatch[i] = key
                        break

                    # Se la % che non sia la persona della cartella è alta, cambia cartella
                    if result["distance"] > 0.70: 
                        break
    except:
        pass

    try:
        for key in keys:
            for path in imageListPath[key]:
                result = DeepFace.verify(imgToCompare, path)

                print(f"distance: {result["distance"]}, thresold: {result["threshold"]}, Person: {i}, db_img: {path}")

                if result["verified"]:
                    faceMatch[i] = key
                    break

                # Se la % che non sia la persona della cartella è alta, cambia cartella
                if result["distance"] > 0.70: 
                    break


            if result["verified"]:
                break
        else:
            faceMatch[i] = False

    except:
        pass
     

# USELESS
def extractFace(frame, Faces):
    try:
        ## LIST[DICT[STR, value]]
        Faces = DeepFace.extract_faces(frame)
    except:
        Faces.append(False) ## Faces[0] == FALSE only if extractFace doesn't work