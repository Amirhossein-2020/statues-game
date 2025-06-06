import math
import cv2
import numpy as np
from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_name="yolo11n-pose.pt", modelface_name="yolo11n-face.pt"):
        self.model = YOLO(model_name)   # Yolo person model
        self.modelFace = YOLO(modelface_name) # Yolo face model
        self.offset = 32    # offset (usato solo su detect_face)

    def detect_people(self, frame):
        results = self.model(frame)  # class 0 = person
        detections = results[0].boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
        keypoints = results[0].keypoints.data.cpu().numpy()
        return detections, keypoints
    
    def detect_face(self, img):
        results = self.modelFace(img)

        if results[0].boxes is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int) # [x1, y1, x2, y2]

            # Applico offset (ritaglio della faccia più ampio)
            for array in boxes:
                array[0] -= self.offset
                array[1] -= self.offset
                array[2] += self.offset
                array[3] += self.offset

            return boxes
        return []
    
class MovementDetector:
    @staticmethod
    def detect_keypoint_movement(kpts1, kpts2, win, box):

        diff = box /  win
        print(f"Differenza = {diff}")
    

        
        for kp in range(17):
            if kp != 2 and kp != 3:
                x1, y1, isvis1 = kpts1[kp]
                x2, y2, isvis2 = kpts2[kp]
                
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                if (isvis1 > 0.8 and isvis2 > 0.8) and distance > 100:
                    print(f"Keypoint who has moved: {kp} \n Edit distance = {distance} \n Freezing point: {x1, y1} \n Actual point: {x2, y2}")
                    return True
        return False

    @staticmethod
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