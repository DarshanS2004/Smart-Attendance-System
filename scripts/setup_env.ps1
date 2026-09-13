$ErrorActionPreference = "Stop"

python -m venv .venv
.\\.venv\\Scripts\\python -m pip install --upgrade pip
.\\.venv\\Scripts\\python -m pip install -r requirements.txt
.\\.venv\\Scripts\\python scripts\\bootstrap_db.py
.\\.venv\\Scripts\\python scripts\\healthcheck.py

Write-Host ""
Write-Host "Environment setup complete."
Write-Host "Start the camera pipeline with: .\\.venv\\Scripts\\python run_camera.py"
Write-Host "Start the dashboard with: .\\.venv\\Scripts\\python -m streamlit run app.py"

