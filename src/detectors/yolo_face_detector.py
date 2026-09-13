from __future__ import annotations

import cv2

from src.config import Settings, get_settings
from src.utils.logging import get_logger


logger = get_logger(__name__)


class YOLOFaceDetector:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.mode = "haar-cascade"
        self.model = None

        try:
            if self.settings.yolo_face_model_full_path.exists():
                from ultralytics import YOLO

                self.model = YOLO(str(self.settings.yolo_face_model_full_path))
                self.mode = "yolo-face"
                logger.info("Using YOLO face model from %s", self.settings.yolo_face_model_full_path)
        except Exception as exc:
            logger.warning("YOLO face model failed to load: %s", exc)

        self.cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect(self, frame) -> list[dict]:
        if self.model is not None:
            results = self.model.predict(frame, verbose=False, conf=0.35)
            detections: list[dict] = []
            for result in results:
                for box in result.boxes:
                    x1, y1, x2, y2 = [int(value) for value in box.xyxy[0].tolist()]
                    width = max(0, x2 - x1)
                    height = max(0, y2 - y1)
                    detections.append(
                        {
                            "bbox_xyxy": [x1, y1, x2, y2],
                            "bbox_ltwh": [x1, y1, width, height],
                            "confidence": float(box.conf[0]),
                        }
                    )
            return detections

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(64, 64))
        return [
            {
                "bbox_xyxy": [int(x), int(y), int(x + w), int(y + h)],
                "bbox_ltwh": [int(x), int(y), int(w), int(h)],
                "confidence": 0.55,
            }
            for x, y, w, h in faces
        ]

