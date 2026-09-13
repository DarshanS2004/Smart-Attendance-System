from __future__ import annotations

import numpy as np
from deep_sort_realtime.deepsort_tracker import DeepSort


class DeepSortFaceTracker:
    def __init__(self, embedding_dim: int = 512) -> None:
        self.embedding_dim = embedding_dim
        self.tracker = DeepSort(max_age=25, n_init=2, max_cosine_distance=0.3, embedder=None)

    def update(self, detections: list[dict], embeddings: list[np.ndarray] | None = None) -> list[dict]:
        ds_detections = [
            (detection["bbox_ltwh"], detection["confidence"], "face")
            for detection in detections
        ]
        if not ds_detections:
            return []

        prepared_embeddings = embeddings or [
            np.zeros(self.embedding_dim, dtype=np.float32) for _ in ds_detections
        ]
        tracks = self.tracker.update_tracks(ds_detections, embeds=prepared_embeddings)
        stable_tracks: list[dict] = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            left, top, right, bottom = track.to_ltrb()
            stable_tracks.append(
                {
                    "track_id": str(track.track_id),
                    "bbox_xyxy": [int(left), int(top), int(right), int(bottom)],
                }
            )
        return stable_tracks
