# Student Management System API

A clean, full-featured Student Management System API with authentication, role-based access control, enrollment, grades, reporting, and JSON persistence. Built with FastAPI and designed to be easy to extend.

## Highlights
- JWT authentication with role-based access control
- Students, teachers, courses, subjects, syllabus CRUD
- Enrollment and grade tracking with GPA + transcript
- Reports (counts, distributions, GPA stats, monthly activity)
- JSON persistence with automatic backups
- Built-in interactive docs (`/docs`, `/redoc`)

## Quick Start
```bash
pip install fastapi uvicorn
uvicorn main:app --reload
```

Open:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Authentication Flow
1. Register a student or teacher
2. Login to get a JWT
3. Send `Authorization: Bearer <token>` to protected endpoints

## Roles
- **Teacher**: full access to all resources and reports
- **Student**: can access their own profile, GPA, transcript, and view courses/subjects/syllabus

## Data Storage
The API stores data in local JSON files under `data/`:
- `students.json`, `teachers.json`, `courses.json`, `subjects.json`, `syllabi.json`
- `enrollments.json`, `grades.json`, `users.json`, `token_blacklist.json`

Backups are created automatically on save.

## Endpoints
See:
- `docs/overview.md`
- `docs/endpoints.md`

## Project Structure
- `main.py` FastAPI app and endpoints
- `models.py` data models and validation
- `students.py`, `teachers.py`, `courses.py`
- `subjects.py`, `syllabus.py`
- `enrollment_and_grades.py`
- `reports.py`
- `data_store.py`
- `users.py`, `auth_utils.py`, `token_blacklist.py`

## License
MIT
