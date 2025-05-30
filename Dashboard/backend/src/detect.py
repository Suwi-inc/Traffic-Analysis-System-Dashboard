from ultralytics import YOLO


class YoloDetector:
    def __init__(self, model_path, confidence, device="cuda"):
        self.model = YOLO(model_path).to(device)  # Move model to GPU
        self.confidence = confidence

    def detect(self, image, use="cuda"):
        results = self.model.predict(image, conf=self.confidence, device=use)
        result = results[0]
        detections = self.make_detections(result)
        return detections

    def make_detections(self, result):
        boxes = result.boxes
        detections = []
        labels = []
        allowed_classes = {
            "car",
            "motorcycle",
            "truck",
            "bus",
        }

        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1
            class_number = int(box.cls[0])
            label = result.names[class_number]
            labels.append(label)
            if label not in allowed_classes:
                continue
            conf = box.conf[0]
            detections.append((([x1, y1, w, h]), class_number, conf))

        return detections, labels
