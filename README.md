# Smart Attendance System

An AI-powered attendance management system that combines real-time face detection, FaceNet-based face recognition, DeepSORT multi-object tracking, duplicate attendance protection, SQL Server persistence, authentication, Streamlit analytics, and automated email/SMS alerts into a unified application.

---

## Overview

The Smart Attendance System is designed to automate attendance capture using real-time computer vision and facial recognition.

The system captures frames from a webcam, detects faces, tracks individuals across video frames, recognizes enrolled employees using FaceNet embeddings, applies duplicate-attendance protection, and stores attendance information in SQL Server.

A premium dark-themed Streamlit dashboard provides centralized access to attendance analytics, live monitoring, employee information, alert history, and system configuration.

### Core Workflow

```text
Webcam
   ↓
Face Detection
   ↓
Face Tracking
   ↓
Face Recognition
   ↓
Identity Matching
   ↓
Duplicate Protection
   ↓
Attendance Recording
   ↓
SQL Server
   ↓
Streamlit Dashboard
   ↓
Analytics & Alerts
```

---

## Project Objectives

The main objectives of this project are:

- Automate employee attendance using face recognition.
- Capture attendance through a webcam.
- Detect faces in real time.
- Recognize enrolled employees using FaceNet embeddings.
- Track detected individuals using DeepSORT.
- Prevent repeated attendance records.
- Store attendance information persistently in SQL Server.
- Provide an interactive attendance analytics dashboard.
- Maintain an enrolled employee directory.
- Maintain recognition and attendance events.
- Provide automated email alerts.
- Provide optional Twilio SMS alerts.
- Provide system health monitoring.
- Provide application authentication.
- Maintain a modular and maintainable software architecture.

---

## Key Features

| Feature | Description |
|---|---|
| Webcam-Based Attendance | Captures live attendance through a webcam |
| Face Detection | YOLO-ready face detector with OpenCV fallback |
| Face Recognition | FaceNet-based facial embeddings |
| Multi-Object Tracking | DeepSORT-based tracking |
| Duplicate Protection | Prevents repeated attendance marking |
| SQL Server Persistence | Stores attendance and application data |
| Authentication | Seeded admin, HR, and viewer accounts |
| Streamlit Dashboard | Premium dark analytics interface |
| Daily Analytics | Daily attendance visualization |
| Monthly Analytics | Monthly attendance analysis |
| Person-Wise Analytics | Attendance counts by person |
| Live Monitor | Latest processed camera frame |
| Employee Directory | Displays enrolled employees |
| Alert History | Email and SMS notification history |
| Email Alerts | SMTP-based notifications |
| SMS Alerts | Optional Twilio integration |
| Health Check | Validates critical system components |
| Testing | Pytest-based automated tests |
| Modular Architecture | Separated application responsibilities |

---

# System Architecture

The system is divided into multiple layers responsible for camera processing, AI inference, attendance management, persistence, analytics, authentication, and notifications.

```text
                              SMART ATTENDANCE SYSTEM
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │       WEBCAM        │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   VIDEO CAPTURE     │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   FACE DETECTION    │
                              │                     │
                              │ YOLO / OpenCV       │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  DEEPSORT TRACKING  │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   FACE EXTRACTION   │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │      FACENET        │
                              │ FACE EMBEDDING      │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ IDENTITY MATCHING   │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ DUPLICATE CHECK     │
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                              ▼                     ▼
                    ┌──────────────────┐   ┌──────────────────┐
                    │ NEW ATTENDANCE   │   │ EXISTING EVENT   │
                    │     RECORD       │   │ / DUPLICATE      │
                    └────────┬─────────┘   └────────┬─────────┘
                             │                      │
                             └──────────┬───────────┘
                                        │
                                        ▼
                              ┌─────────────────────┐
                              │     SQL SERVER      │
                              │  SmartAttendanceDB  │
                              └──────────┬──────────┘
                                         │
                     ┌───────────────────┼───────────────────┐
                     │                   │                   │
                     ▼                   ▼                   ▼
              ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
              │  DASHBOARD   │   │    ALERTS    │   │  ANALYTICS   │
              │  STREAMLIT   │   │ EMAIL / SMS  │   │   & REPORTS  │
              └──────────────┘   └──────────────┘   └──────────────┘
```

---

# End-to-End Attendance Flow

```text
START
  │
  ▼
Start Camera Pipeline
  │
  ▼
Capture Webcam Frame
  │
  ▼
Detect Faces
  │
  ▼
Track Detected Faces
  │
  ▼
Extract Face Region
  │
  ▼
Generate FaceNet Embedding
  │
  ▼
Compare With Enrolled Embeddings
  │
  ▼
Recognize Employee
  │
  ▼
Check Duplicate Attendance
  │
  ├──────────────────────┐
  │                      │
  ▼                      ▼
New Attendance       Already Marked
  │                      │
  ▼                      ▼
Create Record        Track Event
  │                      │
  └───────────┬──────────┘
              │
              ▼
          SQL Server
              │
       ┌──────┼──────┐
       │      │      │
       ▼      ▼      ▼
  Dashboard Alerts Analytics
       │      │      │
       └──────┼──────┘
              │
              ▼
             END
```

---

# AI Computer Vision Pipeline

The real-time camera pipeline combines face detection, tracking, and face recognition.

```text
┌──────────────────────────────────────────────┐
│                 VIDEO FRAME                  │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              FACE DETECTION                 │
│                                              │
│       YOLO Detector / OpenCV Fallback       │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│             DEEPSORT TRACKING               │
│                                              │
│      Maintain Tracks Across Frames          │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│           FACE REGION EXTRACTION            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│                  FACENET                     │
│                                              │
│         FACE EMBEDDING GENERATION            │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│              IDENTITY MATCHING              │
└──────────────────────┬───────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────┐
│            ATTENDANCE DECISION              │
└──────────────────────────────────────────────┘
```

---

# Face Detection

The project supports a YOLO-ready face detector.

The expected YOLO face model path is:

```text
models/yolo/yolov8n-face.pt
```

When the YOLO face model is available, it can be used for face detection.

During initial setup, the system can fall back to an OpenCV Haar Cascade detector.

### Detection Flow

```text
Camera Frame
     │
     ▼
Check YOLO Model
     │
     ├─────────────────────┐
     │                     │
  Available            Not Available
     │                     │
     ▼                     ▼
YOLO Detector         OpenCV Detector
     │                     │
     └──────────┬──────────┘
                │
                ▼
          Detected Faces
```

---

# DeepSORT Multi-Object Tracking

The system uses DeepSORT for multi-object tracking.

Tracking helps maintain a track for a detected individual across consecutive frames.

```text
Frame 1
   │
   ▼
Face Detection
   │
   ▼
Track ID Assigned
   │
   ▼
Frame 2
   │
   ▼
Face Detection
   │
   ▼
DeepSORT Association
   │
   ▼
Existing Track Updated
   │
   ▼
Frame 3
   │
   ▼
Continue Tracking
```

This tracking layer works together with the recognition pipeline to provide more consistent real-time processing.

---

# Face Recognition with FaceNet

The recognition component uses FaceNet embeddings.

The enrollment process converts employee face images into embedding representations that can be used during live recognition.

```text
Employee Face Image
        │
        ▼
Face Processing
        │
        ▼
FaceNet Model
        │
        ▼
Face Embedding
        │
        ▼
Known Face Embedding Store
        │
        ▼
Identity Comparison
        │
        ▼
Recognized Employee
```

The generated embedding file is:

```text
models/embeddings/facenet_embeddings.pkl
```

---

# Employee Enrollment

Employees are enrolled by creating an individual folder under the known-faces directory.

Example:

```text
data/
└── known_faces/
    │
    ├── Employee_1/
    │   ├── profile.json
    │   ├── face_1.jpg
    │   ├── face_2.jpg
    │   └── face_3.jpg
    │
    ├── Employee_2/
    │   ├── profile.json
    │   ├── face_1.jpg
    │   ├── face_2.jpg
    │   └── face_3.jpg
    │
    └── ...
```

The project is configured around using approximately 2–5 clear face images per employee.

### Enrollment Flow

```text
Add Employee
      │
      ▼
Create Employee Folder
      │
      ▼
Add profile.json
      │
      ▼
Add Clear Face Images
      │
      ▼
Run Enrollment Script
      │
      ▼
Process Face Images
      │
      ▼
Generate FaceNet Embeddings
      │
      ▼
Save Embeddings
      │
      ▼
facenet_embeddings.pkl
```

Run:

```powershell
python scripts\enroll_faces.py
```

---

# Duplicate Attendance Protection

The application includes duplicate attendance suppression logic.

The current design provides:

- One attendance record per person per day.
- Additional detections can remain represented as attendance events.
- A duplicate cooldown prevents noisy repeated marking within the configured window.

### Duplicate Handling Flow

```text
Recognized Employee
        │
        ▼
Check Today's Attendance
        │
        ▼
Already Marked?
        │
   ┌────┴──────────────┐
   │                   │
  NO                  YES
   │                   │
   ▼                   ▼
Create Attendance   Track Event
Record
   │                   │
   └────────┬──────────┘
            │
            ▼
      Continue Camera
```

---

# Database Architecture

The system uses Microsoft SQL Server for persistent storage.

Default database configuration:

```text
Server       : localhost\SQLEXPRESS
Database     : SmartAttendanceDB
Authentication: Windows Authentication
```

SQLAlchemy is used as part of the database layer.

### Database Flow

```text
Camera Recognition
        │
        ▼
Attendance Service
        │
        ▼
Repository Layer
        │
        ▼
SQLAlchemy
        │
        ▼
SQL Server
        │
        ▼
SmartAttendanceDB
        │
        ├────────────────────┐
        │                    │
        ▼                    ▼
Attendance Records     Recognition Events
        │                    │
        └──────────┬─────────┘
                   │
                   ▼
          Dashboard Services
                   │
                   ▼
           Streamlit Dashboard
```

---

# Authentication

The application contains seeded users for different access levels.

| Username | Role |
|---|---|
| `admin` | Administrator |
| `hr` | HR |
| `viewer` | Viewer |

These accounts are intended for initial local setup.

> Security Recommendation: Change the default passwords before using the application in a real deployment.

---

# Streamlit Dashboard

The application provides a premium dark-themed Streamlit dashboard.

```text
┌────────────────────────────────────────────────────────────┐
│                SMART ATTENDANCE SYSTEM                    │
├───────────────────┬────────────────────────────────────────┤
│                   │                                        │
│   NAVIGATION      │          DASHBOARD CONTENT             │
│                   │                                        │
│   Overview        │   KPIs / Charts / Analytics            │
│                   │                                        │
│   Live Monitor    │   Latest Camera Snapshot               │
│                   │                                        │
│   People          │   Employee Directory                   │
│                   │                                        │
│   Alerts          │   Email / SMS History                  │
│                   │                                        │
│   System          │   Runtime Configuration                │
│                   │                                        │
└───────────────────┴────────────────────────────────────────┘
```

---

# Dashboard Modules

## Overview

The Overview section provides:

- KPI cards
- Daily attendance chart
- Monthly attendance chart
- Person-wise attendance count

---

## Live Monitor

The Live Monitor provides:

- Latest processed camera frame
- Recent recognition information
- Recent recognition table

The latest annotated frame is saved to:

```text
data/exports/live_frame.jpg
```

---

## People

The People section provides an enrolled employee directory.

It provides a centralized view of people registered in the attendance system.

---

## Alerts

The Alerts section provides notification history.

Supported mechanisms include:

```text
Email
  +
Optional Twilio SMS
```

---

## System

The System section provides:

- Runtime configuration
- System status
- Configuration summary
- Run commands

---

# Attendance Analytics Flow

```text
SQL Server
    │
    ▼
Attendance Records
    │
    ▼
Dashboard Service
    │
    ├──────────────┬───────────────┬────────────────┐
    │              │               │                │
    ▼              ▼               ▼                ▼
 Daily         Monthly        Person-Wise       Recent
Attendance     Analytics       Attendance       Activity
    │              │               │                │
    └──────────────┴───────────────┴────────────────┘
                           │
                           ▼
                   Streamlit Dashboard
```

---

# Alert System

The project supports automated notification workflows through email and optional Twilio SMS.

### Alert Flow

```text
Attendance / System Event
          │
          ▼
      Alert Service
          │
      ┌───┴──────────────┐
      │                  │
      ▼                  ▼
    Email              Twilio
 Notification            SMS
      │                  │
      └────────┬─────────┘
               │
               ▼
         Alert History
               │
               ▼
       Streamlit Dashboard
```

---

# Health Check

The project includes a health-check utility.

Run:

```powershell
python scripts\healthcheck.py
```

The health check validates:

- Database connection
- Camera availability
- Known faces directory
- FaceNet embeddings path
- YOLO model presence

### Health Check Flow

```text
Run Health Check
       │
       ├──► Database Connection
       │
       ├──► Camera Availability
       │
       ├──► Known Faces Directory
       │
       ├──► FaceNet Embeddings
       │
       └──► YOLO Model
                │
                ▼
          System Readiness
```

---

# Testing

The project includes automated tests.

Run:

```powershell
.\.venv\Scripts\python -m pytest
```

Current test modules include:

```text
tests/
├── test_security.py
└── test_settings.py
```

---

# Project Structure

```text
Smart-Attendance-System/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── app.py
├── run_camera.py
├── requirements.txt
│
├── .vscode/
│   ├── extensions.json
│   ├── launch.json
│   ├── settings.json
│   └── tasks.json
│
├── assets/
│   ├── branding/
│   └── styles/
│       └── dashboard.css
│
├── config/
│
├── data/
│   ├── exports/
│   │   └── .gitkeep
│   ├── known_faces/
│   │   └── README.md
│   └── logs/
│       └── .gitkeep
│
├── docs/
│   └── architecture.md
│
├── models/
│   ├── embeddings/
│   ├── facenet/
│   ├── yolo/
│   └── README.md
│
├── scripts/
│   ├── bootstrap_db.py
│   ├── enroll_faces.py
│   ├── healthcheck.py
│   └── setup_env.ps1
│
├── sql/
│   └── bootstrap.sql
│
├── src/
│   ├── alerts/
│   │   └── notifier.py
│   │
│   ├── auth/
│   │   └── security.py
│   │
│   ├── core/
│   │   └── pipeline.py
│   │
│   ├── dashboard/
│   │   └── ui.py
│   │
│   ├── database/
│   │   ├── db.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── detectors/
│   │   └── yolo_face_detector.py
│   │
│   ├── recognition/
│   │   └── facenet_recognizer.py
│   │
│   ├── services/
│   │   ├── attendance_service.py
│   │   └── dashboard_service.py
│   │
│   ├── tracking/
│   │   └── deep_sort_tracker.py
│   │
│   ├── utils/
│   │   ├── helpers.py
│   │   └── logging.py
│   │
│   └── config.py
│
└── tests/
    ├── test_security.py
    └── test_settings.py
```

---

# Technology Stack

| Category | Technology |
|---|---|
| Programming Language | Python |
| Computer Vision | OpenCV |
| Face Detection | YOLO / OpenCV Haar Cascade |
| Face Recognition | FaceNet |
| Face Tracking | DeepSORT |
| Web Application | Streamlit |
| Database | Microsoft SQL Server |
| Database Layer | SQLAlchemy |
| Authentication | Custom Security Module |
| Email | SMTP |
| SMS | Twilio |
| Testing | Pytest |
| Development | VS Code |
| Environment | Python Virtual Environment / PowerShell |

---

# Installation & Setup

## Prerequisites

Before running the project, make sure the system has:

- Windows
- Python
- VS Code
- SQL Server / SQL Server Express
- A working webcam
- Required Python dependencies
- Required model files where applicable

---

## 1. Clone the Repository

```bash
git clone https://github.com/DarshanS2004/Smart-Attendance-System.git
```

Navigate into the project:

```bash
cd Smart-Attendance-System
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

---

## 3. Activate the Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

---

## 4. Upgrade pip

```powershell
python -m pip install --upgrade pip
```

---

## 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 6. Configure Environment Variables

The project contains:

```text
.env
.env.example
```

Use `.env.example` as a template for your local environment configuration.

Sensitive credentials should remain in `.env`.

Never commit `.env` to GitHub.

---

## 7. Bootstrap the Database

Run:

```powershell
python scripts\bootstrap_db.py
```

This initializes the SQL Server database required by the application.

---

## 8. Run the Health Check

Run:

```powershell
python scripts\healthcheck.py
```

Verify that the required components are available.

---

## 9. Add Employees

Create one folder per employee inside:

```text
data/known_faces/
```

Each employee folder should contain:

```text
profile.json
```

and approximately:

```text
2–5 clear face images
```

---

## 10. Generate Face Embeddings

Run:

```powershell
python scripts\enroll_faces.py
```

This generates:

```text
models/embeddings/facenet_embeddings.pkl
```

---

## 11. Add YOLO Model

For YOLO-based face detection, place the face-trained weights file at:

```text
models/yolo/yolov8n-face.pt
```

If the YOLO model is unavailable, the system can use the OpenCV face detector fallback.

---

## 12. Start the Camera Pipeline

Open one terminal:

```powershell
.\.venv\Scripts\python run_camera.py
```

The camera pipeline will begin processing webcam frames.

---

## 13. Start the Streamlit Dashboard

Open a second terminal:

```powershell
.\.venv\Scripts\python -m streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

Default:

```text
http://localhost:8501
```

---

# Complete Setup Flow

```text
Clone Repository
       │
       ▼
Create Virtual Environment
       │
       ▼
Activate Environment
       │
       ▼
Install Dependencies
       │
       ▼
Configure .env
       │
       ▼
Configure SQL Server
       │
       ▼
Bootstrap Database
       │
       ▼
Run Health Check
       │
       ▼
Add Employee Images
       │
       ▼
Run Face Enrollment
       │
       ▼
Generate FaceNet Embeddings
       │
       ▼
Add YOLO Model
       │
       ▼
Start Camera Pipeline
       │
       ▼
Start Streamlit Dashboard
       │
       ▼
Monitor Attendance
```

---

# VS Code Setup

Open the project folder in VS Code.

Open the integrated terminal in the project root.

Run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\scripts\setup_env.ps1
```

For manual setup:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python scripts\bootstrap_db.py
python scripts\healthcheck.py
```

Select the following interpreter in VS Code:

```text
.venv\Scripts\python.exe
```

---

# SQL Server Configuration

Default configuration:

```text
SQL Server Instance : localhost\SQLEXPRESS
Database            : SmartAttendanceDB
Authentication      : Windows Authentication
```

If another SQL Server instance is being used, update the appropriate environment configuration.

The database driver can be adjusted through:

```text
DB_DRIVER
```

when necessary.

---

# SQL Server Troubleshooting

SQL Server Express installations may use dynamic TCP ports.

If the application encounters database connection issues, possible solutions include:

```text
1. Start SQLBrowser.

2. Configure a fixed TCP port for SQLEXPRESS.

3. Update DB_SERVER and DB_PORT in .env
   with the active SQL Server endpoint.
```

The exact configuration depends on the SQL Server installation.

---

# Camera Configuration

The default camera source is:

```text
Camera Index: 0
```

This normally refers to the primary/default webcam.

If multiple cameras are available, the camera configuration can be adjusted according to the local environment.

---

# YOLO Model Configuration

Expected model location:

```text
models/yolo/yolov8n-face.pt
```

The YOLO face model is optional during initial setup because the project provides an OpenCV fallback detector.

---

# Security

The application uses environment-based configuration for sensitive values.

The `.env` file should never be committed to GitHub.

Recommended `.gitignore` entries:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

Never commit:

- Email passwords
- SMTP credentials
- Twilio credentials
- API keys
- Private database credentials
- Employee face images
- Private employee information
- Sensitive application logs

Before publishing the repository, verify that no secrets or private biometric information are included.

---

# Biometric Data & Privacy

This application processes facial images and facial embeddings.

A real-world deployment should therefore consider:

- Employee consent
- Data protection requirements
- Biometric-data handling policies
- Secure storage
- Access control
- Encryption
- Data retention
- Data deletion
- Audit logging
- Organizational policies
- Applicable laws and regulations

This project demonstrates the technical implementation and should not be considered a complete legal or compliance implementation.

---

# Current Limitations

## Face Recognition Accuracy

Recognition performance can be affected by:

- Lighting conditions
- Camera quality
- Face angle
- Image quality
- Enrollment image quality
- Recognition configuration

## YOLO Model Dependency

The YOLO detection path requires the appropriate face-trained model weights.

Without the YOLO weights, the system uses the OpenCV fallback detector.

## Hardware Requirements

Real-time face detection, tracking, and recognition can require significant CPU/GPU resources.

## Camera Dependency

The real-time attendance pipeline requires a working webcam.

## Database Dependency

Persistent attendance storage requires a compatible SQL Server configuration.

## Privacy

Facial recognition involves sensitive biometric information and requires appropriate privacy and security controls in real deployments.

---

# Business Use Cases

## Corporate Offices

Automated employee attendance tracking.

## Educational Institutions

Automated student or staff attendance workflows.

## Industrial Facilities

Workforce attendance monitoring.

## Organizations

Attendance automation in controlled environments where biometric identification is appropriate and permitted.

## Enterprise Operations

Centralized attendance monitoring and analytics.

---

# Future Enhancements

## Mobile Dashboard

Develop a mobile-friendly interface for attendance monitoring.

## Cloud Database

Support cloud-hosted databases for distributed deployments.

## Advanced Reporting

Potential reporting capabilities include:

- CSV exports
- Excel reports
- Attendance summaries
- Department-level analytics
- Absence reports
- Late-arrival analysis

## Improved Face Recognition

Explore additional recognition models and recognition calibration techniques.

## Multi-Camera Support

Support multiple cameras across different locations.

```text
Camera 1 ──┐
Camera 2 ──┤
Camera 3 ──┼──► Central Recognition Service
Camera 4 ──┤
Camera N ──┘
                  │
                  ▼
             SQL Server
                  │
                  ▼
          Central Dashboard
```

## Advanced Analytics

Potential additions include:

- Attendance percentages
- Department comparisons
- Employee attendance trends
- Late-arrival patterns
- Absence analytics
- Attendance forecasting

## Notification Enhancements

Future notification features could include:

- Attendance summaries
- Configurable alerts
- Administrative notifications
- Scheduled reports

---

# Modular Architecture

The project separates major responsibilities into dedicated modules.

```text
src/
│
├── alerts/
│   └── notifier.py
│
├── auth/
│   └── security.py
│
├── core/
│   └── pipeline.py
│
├── dashboard/
│   └── ui.py
│
├── database/
│   ├── db.py
│   ├── models.py
│   └── repository.py
│
├── detectors/
│   └── yolo_face_detector.py
│
├── recognition/
│   └── facenet_recognizer.py
│
├── services/
│   ├── attendance_service.py
│   └── dashboard_service.py
│
├── tracking/
│   └── deep_sort_tracker.py
│
├── utils/
│   ├── helpers.py
│   └── logging.py
│
└── config.py
```

---

# Module Interaction Flow

```text
                  ┌──────────────────┐
                  │      CORE        │
                  │     PIPELINE     │
                  └────────┬─────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     DETECTION         TRACKING        RECOGNITION
          │                │                │
          └────────────────┼────────────────┘
                           │
                           ▼
                  ATTENDANCE SERVICE
                           │
                           ▼
                    DATABASE LAYER
                           │
                           ▼
                      SQL SERVER
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             DASHBOARD             ALERTS
                 │                   │
                 ▼                   ▼
             STREAMLIT            EMAIL/SMS
```

---

# Development & Validation Workflow

```text
Code Changes
     │
     ▼
Run Tests
     │
     ▼
Run Health Check
     │
     ▼
Verify Database
     │
     ▼
Verify Camera
     │
     ▼
Verify Employee Enrollment
     │
     ▼
Verify FaceNet Embeddings
     │
     ▼
Run Camera Pipeline
     │
     ▼
Verify Face Detection
     │
     ▼
Verify Recognition
     │
     ▼
Verify Attendance
     │
     ▼
Verify Dashboard
     │
     ▼
Verify Alerts
```

---

# Skills Demonstrated

```text
Python
│
├── Computer Vision
│   ├── OpenCV
│   ├── Face Detection
│   └── Webcam Processing
│
├── Face Recognition
│   ├── FaceNet
│   ├── Face Embeddings
│   └── Identity Matching
│
├── Object Tracking
│   └── DeepSORT
│
├── AI Application Development
│   ├── Real-Time Inference
│   └── Computer Vision Pipeline
│
├── Database Engineering
│   ├── SQL Server
│   ├── SQLAlchemy
│   └── Repository Layer
│
├── Web Application Development
│   ├── Streamlit
│   ├── Authentication
│   └── Dashboard Design
│
├── Automation
│   ├── Email Alerts
│   └── Twilio SMS
│
└── Software Engineering
    ├── Modular Architecture
    ├── Configuration Management
    ├── Logging
    ├── Health Checks
    └── Automated Testing
```

---

# Feature Matrix

| Component | Technology | Status |
|---|---|---|
| Webcam Capture | OpenCV | ✅ |
| Face Detection | YOLO / OpenCV Fallback | ✅ |
| Face Recognition | FaceNet | ✅ |
| Face Tracking | DeepSORT | ✅ |
| Duplicate Protection | Attendance Logic | ✅ |
| Database | SQL Server | ✅ |
| Database Layer | SQLAlchemy | ✅ |
| Dashboard | Streamlit | ✅ |
| Authentication | Security Module | ✅ |
| Email Alerts | SMTP | ✅ |
| SMS Alerts | Twilio | Optional |
| Employee Enrollment | Python Script | ✅ |
| Health Check | Python Script | ✅ |
| Automated Tests | Pytest | ✅ |
| Live Snapshot | Camera Pipeline | ✅ |

---

# Complete End-to-End Architecture

```text
                              SMART ATTENDANCE SYSTEM
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │       WEBCAM        │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   FRAME CAPTURE     │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │   FACE DETECTION    │
                              │   YOLO / OpenCV     │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  DEEPSORT TRACKING  │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ FACE REGION         │
                              │ EXTRACTION          │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │      FACENET        │
                              │ EMBEDDING GENERATOR │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ IDENTITY MATCHING   │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │ DUPLICATE CHECK     │
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              │                     │
                              ▼                     ▼
                       NEW ATTENDANCE          EXISTING
                           RECORD                EVENT
                              │                     │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │     SQL SERVER      │
                              │ SmartAttendanceDB   │
                              └──────────┬──────────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    │                    │                    │
                    ▼                    ▼                    ▼
             ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
             │   STREAMLIT  │    │    ALERTS    │    │  ANALYTICS   │
             │   DASHBOARD  │    │ EMAIL / SMS  │    │   & REPORTS  │
             └──────┬───────┘    └──────────────┘    └──────────────┘
                    │
                    ▼
             ┌──────────────┐
             │  USER / HR / │
             │    ADMIN     │
             └──────────────┘
```

---

# Recommended Operational Workflow

```text
1. Install Python
       ↓
2. Configure SQL Server
       ↓
3. Clone Repository
       ↓
4. Create Virtual Environment
       ↓
5. Install Dependencies
       ↓
6. Configure .env
       ↓
7. Bootstrap Database
       ↓
8. Run Health Check
       ↓
9. Add Employee Face Images
       ↓
10. Run Face Enrollment
       ↓
11. Verify FaceNet Embeddings
       ↓
12. Add YOLO Model (Optional)
       ↓
13. Start Camera Pipeline
       ↓
14. Start Streamlit Dashboard
       ↓
15. Login
       ↓
16. Monitor Attendance
```

---

# Default Configuration

The project is configured for the following local setup:

```text
SQL Server Instance : localhost\SQLEXPRESS
Database            : SmartAttendanceDB
Authentication      : Windows Authentication
Camera Source       : 0
Dashboard Brand     : Smart Attendance System
Theme               : Premium Dark
```

These settings can be adjusted through the project's configuration and environment files.

---

# Security Best Practices

Before pushing this project to GitHub:

```text
.env
   ↓
Keep Local Only

.env.example
   ↓
Use Placeholder Values

Employee Face Images
   ↓
Keep Private

Database Credentials
   ↓
Keep Private

SMTP Credentials
   ↓
Keep Private

Twilio Credentials
   ↓
Keep Private
```

Recommended `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
*.pyc
data/logs/*
data/exports/*
models/embeddings/*
```

Only add the last entries if those files contain private/generated data that should not be tracked.

---

# Production Considerations

Before using this application in a real organization, additional production controls should be considered.

These may include:

- Secure credential management
- Strong password policies
- Role-based authorization
- Encrypted database communication
- Secure biometric-data storage
- Data retention policies
- Employee consent
- Audit logging
- Database backups
- Recognition threshold calibration
- Monitoring and observability
- Privacy compliance
- Legal and organizational approval

---

# Project Highlights

This project demonstrates practical implementation of:

- Real-time computer vision
- Webcam processing
- Face detection
- Face recognition
- FaceNet embeddings
- DeepSORT tracking
- YOLO-ready detection
- Duplicate attendance protection
- SQL Server integration
- SQLAlchemy database architecture
- Streamlit dashboard development
- Authentication
- Employee enrollment
- Email automation
- Optional SMS automation
- Health monitoring
- Automated testing
- Modular Python architecture

---

# Project Summary

The Smart Attendance System brings together multiple AI and software-engineering components into a single attendance automation platform.

The complete processing chain is:

```text
CAPTURE
   ↓
DETECT
   ↓
TRACK
   ↓
RECOGNIZE
   ↓
VALIDATE
   ↓
RECORD
   ↓
STORE
   ↓
ANALYZE
   ↓
NOTIFY
```

The project demonstrates an end-to-end approach to building a real-time AI application where computer vision, face recognition, database persistence, analytics, authentication, and notification services work together.

---

# Quick Start

```powershell
git clone https://github.com/DarshanS2004/Smart-Attendance-System.git

cd Smart-Attendance-System

python -m venv .venv

.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip

pip install -r requirements.txt

python scripts\bootstrap_db.py

python scripts\healthcheck.py

python scripts\enroll_faces.py
```

Start the camera:

```powershell
.\.venv\Scripts\python run_camera.py
```

Open another terminal and start Streamlit:

```powershell
.\.venv\Scripts\python -m streamlit run app.py
```

Open:

```text
http://localhost:8501
```

---

# Author

**Darshan S**

GitHub:

https://github.com/DarshanS2004

---

# License

This project is intended for educational, portfolio, and demonstration purposes.

If the project is distributed or deployed publicly, add an appropriate open-source license and review the licenses of all third-party libraries, models, and dependencies used by the application.