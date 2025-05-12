from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_name="yolo11n-pose.pt", modelface_name="yolo11n-face.pt"):
        self.model = YOLO(model_name)
        self.modelFace = YOLO(modelface_name)

    def detect_people(self, frame):
        results = self.model(frame)  # class 0 = person
        detections = results[0].boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
        keypoints = results[0].keypoints.data.cpu().numpy()
        return detections, keypoints
    
    def detect_face(self, img):
        results = self.model(img)

        if results[0].boxes != None:
            boxes = results[0].boxes.xyxy.cpu().numpy().astype(int)
            return boxes