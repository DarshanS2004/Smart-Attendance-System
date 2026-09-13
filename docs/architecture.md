# Smart Attendance System Architecture

## Runtime Split

- `run_camera.py` runs the real-time OpenCV pipeline.
- `app.py` runs the Streamlit command center and analytics dashboard.
- `scripts/enroll_faces.py` generates FaceNet embeddings from employee images.
- `scripts/bootstrap_db.py` creates the SQL Server database and seeds login users.

## Core Flow

1. Camera frames come from the local webcam.
2. YOLO face detection runs first.
3. DeepSORT assigns stable track IDs across frames.
4. FaceNet converts cropped faces into embeddings.
5. Embeddings are matched against the enrolled employee gallery.
6. Duplicate logic prevents noisy repeat attendance events.
7. SQL Server stores attendance, event, and alert history.
8. Streamlit reads live analytics and the latest annotated frame.

## Duplicate Control

- A person can only have one `attendance` row per day.
- Each frame can still generate `attendance_events`.
- When the same person is seen again inside the configured cooldown window, the event is tagged as duplicate.

## Alerting

- Unknown face detections trigger email and optional SMS alerts.
- Alert cooldown protects the system from spamming for the same unknown visitor.

