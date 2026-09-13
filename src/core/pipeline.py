from __future__ import annotations

from datetime import datetime

import cv2
import numpy as np

from src.alerts.notifier import Notifier
from src.config import Settings, get_settings
from src.database.db import DatabaseManager
from src.database.repository import AttendanceRepository
from src.detectors.yolo_face_detector import YOLOFaceDetector
from src.recognition.facenet_recognizer import FaceNetRecognizer
from src.services.attendance_service import AttendanceService
from src.tracking.deep_sort_tracker import DeepSortFaceTracker
from src.utils.helpers import compute_iou, crop_with_margin, save_frame
from src.utils.logging import get_logger


logger = get_logger(__name__)


class AttendancePipeline:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.database = DatabaseManager(self.settings)
        self.database.bootstrap()
        self.repository = AttendanceRepository(self.database)
        self.detector = YOLOFaceDetector(self.settings)
        self.tracker = DeepSortFaceTracker()
        self.recognizer = FaceNetRecognizer(self.repository, self.settings)
        self.notifier = Notifier(self.settings)
        self.attendance_service = AttendanceService(self.repository, self.notifier, self.settings)

    def _match_detection(self, track_bbox: list[int], detections: list[dict]) -> dict | None:
        best_iou = 0.0
        best_detection = None
        for detection in detections:
            iou = compute_iou(track_bbox, detection["bbox_xyxy"])
            if iou > best_iou:
                best_iou = iou
                best_detection = detection
        return best_detection

    def process_frame(self, frame):
        annotated = frame.copy()
        detections = self.detector.detect(frame)
        face_embeddings: list[np.ndarray] = []
        for detection in detections:
            face_crop = crop_with_margin(frame, detection["bbox_xyxy"])
            embedding = self.recognizer.compute_embedding(face_crop)
            detection["face_crop"] = face_crop
            detection["embedding"] = embedding
            face_embeddings.append(
                embedding if embedding is not None else np.zeros(self.recognizer.embedding_dim, dtype=np.float32)
            )

        tracks = self.tracker.update(detections, face_embeddings)
        processed_rows: list[dict] = []

        for track in tracks:
            bbox = track["bbox_xyxy"]
            matched_detection = self._match_detection(bbox, detections)
            if matched_detection and matched_detection.get("embedding") is not None:
                recognition = self.recognizer.recognize_from_embedding(matched_detection["embedding"])
            else:
                face_crop = crop_with_margin(frame, bbox)
                recognition = self.recognizer.recognize(face_crop)
            frame_path = str(self.settings.live_frame_path) if self.settings.save_live_frame else None
            self.attendance_service.handle_recognition(
                recognition=recognition,
                track_id=track["track_id"],
                camera_source=f"camera:{self.settings.camera_index}",
                frame_path=frame_path,
            )

            color = (21, 195, 154) if recognition["matched"] else (255, 93, 115)
            label = (
                f'{recognition["label"]} | {recognition["confidence"]:.2f}'
                if recognition["matched"]
                else f'Unknown | {recognition["confidence"]:.2f}'
            )
            cv2.rectangle(annotated, (bbox[0], bbox[1]), (bbox[2], bbox[3]), color, 2)
            cv2.rectangle(annotated, (bbox[0], max(0, bbox[1] - 32)), (bbox[2], bbox[1]), color, -1)
            cv2.putText(
                annotated,
                label,
                (bbox[0] + 8, max(18, bbox[1] - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
            )
            processed_rows.append(
                {
                    "track_id": track["track_id"],
                    "label": recognition["label"],
                    "confidence": recognition["confidence"],
                }
            )

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(
            annotated,
            f"{self.settings.app_name} | {timestamp}",
            (18, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )
        if self.settings.save_live_frame:
            save_frame(self.settings.live_frame_full_path, annotated)
        return annotated, processed_rows

    def run(self, show_window: bool = True) -> None:
        capture = cv2.VideoCapture(self.settings.camera_index)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.settings.camera_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.settings.camera_height)
        if not capture.isOpened():
            raise RuntimeError(f"Unable to open camera index {self.settings.camera_index}")

        logger.info("Camera pipeline started.")
        frame_number = 0
        try:
            while True:
                grabbed, frame = capture.read()
                if not grabbed:
                    logger.warning("Failed to read frame from camera.")
                    continue

                frame_number += 1
                if frame_number % self.settings.frame_skip != 0:
                    if show_window:
                        cv2.imshow(self.settings.app_name, frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                    continue

                annotated, _ = self.process_frame(frame)
                if show_window:
                    cv2.imshow(self.settings.app_name, annotated)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
        finally:
            capture.release()
            cv2.destroyAllWindows()
            logger.info("Camera pipeline stopped.")
