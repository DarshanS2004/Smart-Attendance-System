from __future__ import annotations

import json
import pickle
from pathlib import Path

import cv2
import numpy as np
import torch
from facenet_pytorch import InceptionResnetV1, fixed_image_standardization
from PIL import Image
from torchvision import transforms

from src.config import Settings, get_settings
from src.database.repository import AttendanceRepository
from src.utils.logging import get_logger


logger = get_logger(__name__)


class FaceNetRecognizer:
    def __init__(self, repository: AttendanceRepository, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.repository = repository
        self.device = torch.device("cpu")
        self.model = InceptionResnetV1(pretrained="vggface2").eval().to(self.device)
        self.transform = transforms.Compose(
            [
                transforms.Resize((160, 160)),
                transforms.ToTensor(),
                fixed_image_standardization,
            ]
        )
        self.embedding_dim = 512
        self.embeddings = self._load_embeddings()

    def _load_embeddings(self) -> list[dict]:
        if not self.settings.embeddings_full_path.exists():
            return []
        with self.settings.embeddings_full_path.open("rb") as file:
            data = pickle.load(file)
        return data if isinstance(data, list) else []

    def _save_embeddings(self) -> None:
        self.settings.embeddings_full_path.parent.mkdir(parents=True, exist_ok=True)
        with self.settings.embeddings_full_path.open("wb") as file:
            pickle.dump(self.embeddings, file)

    def compute_embedding(self, face_bgr: np.ndarray) -> np.ndarray | None:
        if face_bgr.size == 0:
            return None
        image = cv2.cvtColor(face_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image)
        tensor = self.transform(pil_image).unsqueeze(0).to(self.device)
        with torch.no_grad():
            embedding = self.model(tensor).cpu().numpy()[0]
        norm = np.linalg.norm(embedding)
        return embedding / norm if norm else None

    def recognize_from_embedding(self, embedding: np.ndarray | None) -> dict:
        if embedding is None or not self.embeddings:
            return {
                "matched": False,
                "label": "Unknown",
                "confidence": 0.0,
                "person_id": None,
                "employee_code": None,
            }

        best_match = None
        best_score = -1.0
        for entry in self.embeddings:
            score = float(np.dot(embedding, entry["embedding"]))
            if score > best_score:
                best_score = score
                best_match = entry

        if not best_match or best_score < self.settings.face_match_threshold:
            return {
                "matched": False,
                "label": "Unknown",
                "confidence": max(best_score, 0.0),
                "person_id": None,
                "employee_code": None,
            }

        return {
            "matched": True,
            "label": best_match["full_name"],
            "confidence": round(best_score, 3),
            "person_id": best_match["person_id"],
            "employee_code": best_match["employee_code"],
        }

    def recognize(self, face_bgr: np.ndarray) -> dict:
        embedding = self.compute_embedding(face_bgr)
        return self.recognize_from_embedding(embedding)

    def enroll_from_directory(self) -> list[dict]:
        enrolled: list[dict] = []
        embeddings: list[dict] = []
        for person_dir in sorted(self.settings.known_faces_full_path.glob("*")):
            if not person_dir.is_dir():
                continue

            profile_path = person_dir / "profile.json"
            if profile_path.exists():
                profile = json.loads(profile_path.read_text(encoding="utf-8"))
            else:
                parts = person_dir.name.split("_", maxsplit=1)
                employee_code = parts[0]
                full_name = parts[1].replace("_", " ") if len(parts) > 1 else parts[0]
                profile = {
                    "employee_code": employee_code,
                    "full_name": full_name,
                    "department": "General",
                    "email": "",
                    "phone": "",
                }

            person = self.repository.upsert_person(profile, image_dir=str(person_dir))
            vectors: list[np.ndarray] = []
            for image_path in person_dir.iterdir():
                if image_path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
                    continue
                image = cv2.imread(str(image_path))
                if image is None:
                    continue
                embedding = self.compute_embedding(image)
                if embedding is not None:
                    vectors.append(embedding)

            if not vectors:
                logger.warning("No valid face images found for %s", person_dir.name)
                continue

            mean_embedding = np.mean(vectors, axis=0)
            mean_embedding = mean_embedding / np.linalg.norm(mean_embedding)
            embeddings.append(
                {
                    "person_id": person.id,
                    "employee_code": person.employee_code,
                    "full_name": person.full_name,
                    "embedding": mean_embedding,
                }
            )
            enrolled.append(
                {
                    "employee_code": person.employee_code,
                    "full_name": person.full_name,
                    "image_count": len(vectors),
                }
            )

        self.embeddings = embeddings
        self._save_embeddings()
        logger.info("Enrollment completed for %s people", len(enrolled))
        return enrolled
