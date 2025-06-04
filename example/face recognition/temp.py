import os
import sys
import cv2
import ctypes

import numpy as np
#from deepface import DeepFace

sys.path.append(os.path.abspath("."))
from lib import detector, utils
import threading

def main():
    
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
    
    video = cv2.VideoCapture(1)

    user32 = ctypes.windll.user32
    win_x, win_y = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]

    cv2.namedWindow("Statues Game", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Statues Game", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (win_x, win_y))















        cv2.imshow("Statues Game", frame)
        key = cv2.waitKey(1)
        if key == 27: #ESC
            # Close program
            break

main()