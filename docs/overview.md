# API Overview

This API provides a full student management system with authentication, role-based access, and reporting.

## Built-in Docs
- Swagger UI: `/docs`
- ReDoc: `/redoc`

## Auth Flow
1. Register a user (student or teacher)
2. Login to get a JWT
3. Send `Authorization: Bearer <token>` on protected routes

## Roles
- Teacher: full access to student/teacher/course/subject/grade/enrollment CRUD and reports
- Student: can access their own student profile, GPA, transcript, and view courses/subjects/syllabus

## Data Storage
Local JSON files in `data/`:
- `students.json`, `teachers.json`, `courses.json`, `subjects.json`, `syllabi.json`
- `enrollments.json`, `grades.json`, `users.json`, `token_blacklist.json`
