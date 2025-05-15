from deepface import DeepFace
import cv2

def checkFace(imgToCompare, imageListPath, faceMatch, i):

    try:
        for path in imageListPath:
            result = DeepFace.verify(imgToCompare, path)

            print(f"distance: {result["distance"]}, thresold: {result["threshold"]}, Person: {i}")

            if result["verified"]:
                faceMatch[i] = True
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