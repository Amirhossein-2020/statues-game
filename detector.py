from ultralytics import YOLO

class PersonDetector:
    def __init__(self, model_name="yolov8n.pt"):
        self.model = YOLO(model_name)

    def detect_people(self, frame):
        results = self.model(frame, classes=[0])  # class 0 = person
        detections = results[0].boxes.xyxy.cpu().numpy()  # [x1, y1, x2, y2]
        return detections