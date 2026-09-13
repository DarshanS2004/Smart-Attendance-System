# Known Faces

Create one folder per person inside this directory.

Recommended structure:

```text
data/known_faces/
  EMP001_Alice_Johnson/
    profile.json
    1.jpg
    2.jpg
  EMP002_Bob_Singh/
    profile.json
    1.jpg
```

Sample `profile.json`:

```json
{
  "employee_code": "EMP001",
  "full_name": "Alice Johnson",
  "department": "Engineering",
  "email": "alice@example.com",
  "phone": "+910000000000"
}
```

After adding images, run:

```powershell
python scripts/enroll_faces.py
```

