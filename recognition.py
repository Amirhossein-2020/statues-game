from deepface import DeepFace

def checkFace(imgToCompare, imageListPath, faceMatch, i):

    try:
        for path in imageListPath:
            if DeepFace.verify(imgToCompare, path)["verified"]:
                faceMatch[i] = True
                break
            else:
                faceMatch[i] = False
    except:
        faceMatch[i] = False

# USELESS
def extractFace(frame, Faces):
    try:
        ## LIST[DICT[STR, value]]
        Faces = DeepFace.extract_faces(frame)
    except:
        Faces.append(False) ## Faces[0] == FALSE only if extractFace doesn't work