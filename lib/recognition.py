from deepface import DeepFace
import threading
import numpy as np

from lib.detector import PersonDetector

# Game Variable
Threads = []

observer = PersonDetector()

# DOESN'T WORK
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

# Uguale alla funzione checkFace, ma fatta con un solo thread
def OneThreadCheckFace(frame, imageListPath, keys, faceMatch, boxes):
    for i, box in enumerate(boxes):
        x1, y1, x2, y2 = map(int, box)

        try:
            for key in keys:
                for path in imageListPath[key]:
                    result = DeepFace.verify(frame[y1:y2, x1:x2], path)

                    print(f"distance: {result['distance']}, threshold: {result['threshold']}, Person: {i}, db_img: {path}")

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

# Ogni singola persona su schermo ha un proprio thread che controlla la sua faccia
def checkFace(imgToCompare, DB, keys, faceMatch, i):

    # Fast check, se la persona ha gia un nome (era stata trovata in precedenza), controlla subito se la persona è la stessa
    '''
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
        
    '''

    result = {"verified": False}

    for key in keys:
        for path in DB.imageList[key]:

            # Path = immagine caricata, controllo se non è stringa, 
            # ovvero il percorso, se non è la trasformo in numpy array, 
            # se fallisce gli passo il percorso dell'immagine (Con il percorso deve ricaricare l'immagine)
            img = path

            try:
                if type(path) != str:
                    img = np.array(path)
                else:
                    img = path
            except:
                img = DB.imageListPath[key][0]

            # Purtroppo se l'immagine è troppo mossa e 
            # DeepFace non riesce a trovare la faccia fa errore            
            try:
                result = DeepFace.verify(imgToCompare, img)
            
            except Exception as e:         
                print("ERRORE, Immagine brutta")
                print(e)
                continue

            # Usato per debuggin
            #print(f"distance: {result['distance']}, threshold: {result['threshold']}, Person: {i}, db_img: {DB.imageListPath[key][i]}")

            # Se la % che non sia la persona della cartella è alta, cambia cartella
            # Se è match, esci dalla funzione.
            # Usata in fase di sviluppo, ma alla fine non viene eseguita poiché 
            # viene creata solo un'immagine per persona
            if result["verified"] or result["distance"] > 0.70:
                if result["verified"]:
                    faceMatch[i] = key
                
                break

        if result["verified"]:
            break
    else:
        # Se giro tutto il database e non trovo la faccia, il giocatore ancora non esiste
        faceMatch[i] = "Not in database"