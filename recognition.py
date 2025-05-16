from deepface import DeepFace
import cv2

def checkFace(imgToCompare, imageListPath, faceMatch, i):

    try:
        for key in imageListPath.keys():
            for path in imageListPath[key]:
                result = DeepFace.verify(imgToCompare, path)

                print(f"distance: {result["distance"]}, thresold: {result["threshold"]}, Person: {i}, db_img: {path}")

                if result["verified"]:
                    faceMatch[i] = key
                    break

                # Se la % che non sia la persona della cartella è alta, cambia cartella
                if result["distance"] > 0.80: 
                    break


            if result["verified"]:
                break
        else:
            faceMatch[i] = False

    except ValueError:
        pass

# USELESS
def extractFace(frame, Faces):
    try:
        ## LIST[DICT[STR, value]]
        Faces = DeepFace.extract_faces(frame)
    except:
        Faces.append(False) ## Faces[0] == FALSE only if extractFace doesn't work