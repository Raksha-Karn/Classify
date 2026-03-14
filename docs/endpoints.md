# Endpoints

## Auth
- `POST /auth/register/student`
- `POST /auth/register/teacher`
- `POST /auth/login`
- `POST /auth/reset-password`
- `POST /auth/logout`
- `GET /me`

## Students
- `POST /students` (teacher)
- `GET /students` (teacher)
- `GET /students/{student_id}` (teacher or self)
- `PATCH /students/{student_id}` (teacher or self)
- `DELETE /students/{student_id}` (teacher)
- `GET /students/search?q=...` (teacher)
- `GET /students/{student_id}/gpa` (teacher or self)
- `GET /students/{student_id}/transcript` (teacher or self)

## Teachers
- `POST /teachers` (teacher)
- `GET /teachers` (teacher)
- `GET /teachers/{teacher_id}` (auth)
- `PATCH /teachers/{teacher_id}` (teacher)
- `DELETE /teachers/{teacher_id}` (teacher)
- `GET /teachers/search?q=...` (teacher)

## Courses
- `POST /courses` (teacher)
- `GET /courses` (auth)
- `GET /courses/{course_id}` (auth)
- `PATCH /courses/{course_id}` (teacher)
- `DELETE /courses/{course_id}` (teacher)
- `GET /courses/search?q=...` (auth)

## Subjects
- `POST /subjects` (teacher)
- `GET /subjects` (auth)
- `GET /subjects/{subject_id}` (auth)
- `PATCH /subjects/{subject_id}` (teacher)
- `DELETE /subjects/{subject_id}` (teacher)
- `GET /subjects/search?q=...` (auth)

## Syllabus
- `POST /syllabus` (teacher)
- `GET /syllabus/{subject_id}` (auth)
- `DELETE /syllabus/{subject_id}` (teacher)

## Enrollments
- `POST /enrollments` (teacher)
- `GET /enrollments` (teacher)
- `PATCH /enrollments/{enrollment_id}/assign-teacher` (teacher)
- `DELETE /enrollments/{enrollment_id}` (teacher)

## Grades
- `POST /grades` (teacher)
- `GET /grades` (teacher)
- `GET /grades/enrollment/{enrollment_id}` (teacher)

## Reports
- `GET /reports/students-per-class` (teacher)
- `GET /reports/students-per-faculty` (teacher)
- `GET /reports/courses-per-level` (teacher)
- `GET /reports/enrollment-per-course` (teacher)
- `GET /reports/grade-distribution` (teacher)
- `GET /reports/gpa-stats` (teacher)
- `GET /reports/monthly-enrollments` (teacher)
- `GET /reports/monthly-grades` (teacher)
- `POST /reports/export-json` (teacher)
- `POST /reports/export-csv` (teacher)
