import os
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field

from students import StudentManager
from teachers import TeacherManager
from courses import CourseManager
from enrollment_and_grades import EnrollmentManager, GradeManager
from reports import ReportManager
from users import UserManager
from auth_utils import create_jwt, decode_jwt
from token_blacklist import TokenBlacklist
from subjects import SubjectManager
from syllabus import SyllabusManager


app = FastAPI(title="Student Management System")

students = StudentManager()
teachers = TeacherManager()
courses = CourseManager()
enrollments = EnrollmentManager()
grades = GradeManager()
reports = ReportManager()
users = UserManager()
blacklist = TokenBlacklist()
subjects = SubjectManager()
syllabi = SyllabusManager()

JWT_SECRET = os.environ.get("JWT_SECRET", "dev_secret_change_me")


@app.on_event("startup")
def load_data():
    students.load()
    teachers.load()
    courses.load()
    enrollments.load()
    grades.load()
    users.load()
    blacklist.load()
    subjects.load()
    syllabi.load()


@app.on_event("shutdown")
def save_data():
    students.save()
    teachers.save()
    courses.save()
    enrollments.save()
    grades.save()
    users.save()
    blacklist.save()
    subjects.save()
    syllabi.save()


class StudentCreate(BaseModel):
    name: str
    email: str
    contact: str
    student_class: Optional[int] = None
    faculty: Optional[str] = None
    degree: Optional[str] = None
    section: Optional[str] = None


class TeacherCreate(BaseModel):
    name: str
    classes: List[int]
    contact: str
    meta: str
    faculty: Optional[str] = None
    degree: Optional[str] = None
    student_class: Optional[int] = None
    section: Optional[str] = None


class CourseCreate(BaseModel):
    course_name: str
    course_code: str
    faculty: str
    degree: str
    level_type: str
    level_value: int
    course_class: str


class EnrollmentCreate(BaseModel):
    student_id: str
    course_id: str
    teacher_id: Optional[str] = None


class GradeCreate(BaseModel):
    enrollment_id: str
    grade_letter: Optional[str] = None
    grade_numeric: Optional[float] = None
    term: Optional[str] = None


class SubjectCreate(BaseModel):
    name: str
    code: str
    faculty: str
    degree: str
    level_type: str
    level_value: int
    subject_class: str


class SyllabusCreate(BaseModel):
    subject_id: str
    content: str


class RegisterStudent(BaseModel):
    role: str = Field(default="student")
    username: str
    email: str
    password: str
    name: str
    contact: str
    student_class: Optional[int] = None
    faculty: Optional[str] = None
    degree: Optional[str] = None
    section: Optional[str] = None


class RegisterTeacher(BaseModel):
    role: str = Field(default="teacher")
    username: str
    email: str
    password: str
    name: str
    classes: List[int]
    contact: str
    meta: str
    faculty: Optional[str] = None
    degree: Optional[str] = None
    student_class: Optional[int] = None
    section: Optional[str] = None


class LoginPayload(BaseModel):
    login: str
    password: str


class ResetPasswordPayload(BaseModel):
    email: str
    new_password: str


def get_current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    token = authorization.split(" ", 1)[1].strip()
    if blacklist.contains(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    payload = decode_jwt(token, JWT_SECRET)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = users.find_by_id(payload.get("user_id"))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_current_token(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    return authorization.split(" ", 1)[1].strip()


def require_teacher(user=Depends(get_current_user)):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Teacher role required")
    return user


def require_self_or_teacher(student_id: str, user=Depends(get_current_user)):
    if user.role == "teacher":
        return user
    if user.role == "student" and user.linked_id == student_id:
        return user
    raise HTTPException(status_code=403, detail="Not allowed")


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/auth/register/student")
def register_student(payload: RegisterStudent):
    try:
        student = students.add_student(
            name=payload.name,
            email=payload.email,
            contact=payload.contact,
            student_class=payload.student_class,
            faculty=payload.faculty,
            degree=payload.degree,
            section=payload.section,
        )
        user = users.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            role="student",
            linked_id=student["id"],
        )
        return {"user": user, "student": student}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/register/teacher")
def register_teacher(payload: RegisterTeacher):
    try:
        teacher = teachers.add_teacher(
            name=payload.name,
            classes=payload.classes,
            contact=payload.contact,
            meta=payload.meta,
            faculty=payload.faculty,
            degree=payload.degree,
            student_class=payload.student_class,
            section=payload.section,
        )
        user = users.create_user(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            role="teacher",
            linked_id=teacher["id"],
        )
        return {"user": user, "teacher": teacher}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/auth/login")
def login(payload: LoginPayload):
    user = users.authenticate(payload.login, payload.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt(
        {"user_id": user.id, "role": user.role, "linked_id": user.linked_id},
        JWT_SECRET,
        expires_in_seconds=3600,
    )
    return {"access_token": token, "token_type": "bearer"}


@app.post("/auth/reset-password")
def reset_password(payload: ResetPasswordPayload):
    ok = users.reset_password(payload.email, payload.new_password)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "ok"}


@app.post("/auth/logout")
def logout(user=Depends(get_current_user), token: str = Depends(get_current_token)):
    blacklist.add(token)
    return {"status": "ok"}


@app.get("/me")
def me(user=Depends(get_current_user)):
    return user.to_dict()


@app.post("/students")
def add_student(payload: StudentCreate, _=Depends(require_teacher)):
    try:
        return students.add_student(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students")
def list_students(
    faculty: Optional[str] = None,
    student_class: Optional[int] = None,
    degree: Optional[str] = None,
    section: Optional[str] = None,
    _=Depends(require_teacher),
):
    return students.view_students(
        faculty=faculty,
        student_class=student_class,
        degree=degree,
        section=section,
    )


@app.get("/students/{student_id}")
def get_student(student_id: str, _=Depends(require_self_or_teacher)):
    student = students.view_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}")
def update_student(student_id: str, updates: Dict[str, Any], _=Depends(require_self_or_teacher)):
    allowed = {"name", "email", "contact", "student_class", "faculty", "degree", "section"}
    updates = {k: v for k, v in updates.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    try:
        student = students.edit_student(student_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: str, _=Depends(require_teacher)):
    student = students.delete_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students/search")
def search_students(q: str, _=Depends(require_teacher)):
    return students.search_student(q)


@app.post("/teachers")
def add_teacher(payload: TeacherCreate, _=Depends(require_teacher)):
    try:
        return teachers.add_teacher(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/teachers")
def list_teachers(
    faculty: Optional[str] = None,
    student_class: Optional[int] = None,
    degree: Optional[str] = None,
    section: Optional[str] = None,
    _=Depends(require_teacher),
):
    return teachers.view_teachers(
        faculty=faculty,
        student_class=student_class,
        degree=degree,
        section=section,
    )


@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: str, _=Depends(get_current_user)):
    teacher = teachers.view_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.patch("/teachers/{teacher_id}")
def update_teacher(teacher_id: str, updates: Dict[str, Any], _=Depends(require_teacher)):
    allowed = {"name", "classes", "contact", "meta", "faculty", "degree", "student_class", "section"}
    updates = {k: v for k, v in updates.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    try:
        teacher = teachers.edit_teacher(teacher_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: str, _=Depends(require_teacher)):
    teacher = teachers.delete_teacher(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.post("/courses")
def add_course(payload: CourseCreate, _=Depends(require_teacher)):
    try:
        return courses.add_course(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses")
def list_courses(
    faculty: Optional[str] = None,
    degree: Optional[str] = None,
    course_class: Optional[str] = None,
    _=Depends(get_current_user),
):
    if faculty or degree or course_class:
        return courses.filter_search(faculty=faculty, degree=degree, course_class=course_class)
    return courses.view_courses()


@app.get("/courses/{course_id}")
def get_course(course_id: str, _=Depends(get_current_user)):
    course = courses.view_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.patch("/courses/{course_id}")
def update_course(course_id: str, updates: Dict[str, Any], _=Depends(require_teacher)):
    allowed = {"course_name", "course_code", "faculty", "degree", "level_type", "level_value", "course_class"}
    updates = {k: v for k, v in updates.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    try:
        course = courses.edit_course(course_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: str, _=Depends(require_teacher)):
    course = courses.delete_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses/search")
def search_courses(q: str, _=Depends(get_current_user)):
    return courses.search_by_keyword(q)


@app.post("/enrollments")
def enroll_student(payload: EnrollmentCreate, _=Depends(require_teacher)):
    try:
        return enrollments.enroll_student(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/enrollments")
def list_enrollments(_=Depends(require_teacher)):
    return enrollments.list_dicts()


@app.patch("/enrollments/{enrollment_id}/assign-teacher")
def assign_teacher(enrollment_id: str, teacher_id: str, _=Depends(require_teacher)):
    enrollment = enrollments.assign_teacher(enrollment_id, teacher_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: str, _=Depends(require_teacher)):
    enrollment = enrollments.delete_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@app.post("/grades")
def record_grade(payload: GradeCreate, _=Depends(require_teacher)):
    try:
        return grades.record_grade(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/grades")
def list_grades(_=Depends(require_teacher)):
    return grades.list_dicts()


@app.get("/grades/enrollment/{enrollment_id}")
def grades_for_enrollment(enrollment_id: str, _=Depends(require_teacher)):
    return grades.get_grades_for_enrollment(enrollment_id)


@app.get("/students/{student_id}/gpa")
def gpa_for_student(student_id: str, _=Depends(require_self_or_teacher)):
    gpa = grades.gpa_for_student(student_id, enrollments.list_models())
    return {"student_id": student_id, "gpa": gpa}


@app.get("/students/{student_id}/transcript")
def transcript_for_student(student_id: str, _=Depends(require_self_or_teacher)):
    return grades.transcript(student_id, enrollments.list_models())


@app.get("/reports/students-per-class")
def report_students_per_class(_=Depends(require_teacher)):
    return reports.students_per_class(students.list_models())


@app.get("/reports/students-per-faculty")
def report_students_per_faculty(_=Depends(require_teacher)):
    return reports.students_per_faculty(students.list_models())


@app.get("/reports/courses-per-level")
def report_courses_per_level(_=Depends(require_teacher)):
    return reports.courses_per_level(courses.list_models())


@app.get("/reports/enrollment-per-course")
def report_enrollment_per_course(_=Depends(require_teacher)):
    return reports.enrollment_per_course(enrollments.list_models())


@app.get("/reports/grade-distribution")
def report_grade_distribution(_=Depends(require_teacher)):
    return reports.grade_distribution(grades.list_models())


@app.post("/reports/export-json")
def export_report_json(filename: str, data: Dict[str, Any], _=Depends(require_teacher)):
    reports.export_json(filename, data)
    return {"status": "ok", "file": filename}


@app.post("/reports/export-csv")
def export_report_csv(filename: str, data: Dict[str, Any], header_key: str = "key", header_value: str = "value", _=Depends(require_teacher)):
    reports.export_csv(filename, data, header_key=header_key, header_value=header_value)
    return {"status": "ok", "file": filename}


@app.post("/subjects")
def add_subject(payload: SubjectCreate, _=Depends(require_teacher)):
    try:
        return subjects.add_subject(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/subjects")
def list_subjects(
    faculty: Optional[str] = None,
    degree: Optional[str] = None,
    level_type: Optional[str] = None,
    level_value: Optional[int] = None,
    subject_class: Optional[str] = None,
    _=Depends(get_current_user),
):
    return subjects.view_subjects(
        faculty=faculty,
        degree=degree,
        level_type=level_type,
        level_value=level_value,
        subject_class=subject_class,
    )


@app.get("/subjects/{subject_id}")
def get_subject(subject_id: str, _=Depends(get_current_user)):
    subject = subjects.view_subject_by_id(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@app.patch("/subjects/{subject_id}")
def update_subject(subject_id: str, updates: Dict[str, Any], _=Depends(require_teacher)):
    allowed = {"name", "code", "faculty", "degree", "level_type", "level_value", "subject_class"}
    updates = {k: v for k, v in updates.items() if k in allowed}
    if not updates:
        raise HTTPException(status_code=400, detail="No valid fields to update")
    try:
        subject = subjects.edit_subject(subject_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: str, _=Depends(require_teacher)):
    subject = subjects.delete_subject(subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject


@app.get("/subjects/search")
def search_subjects(q: str, _=Depends(get_current_user)):
    return subjects.search_subjects(q)


@app.post("/syllabus")
def set_syllabus(payload: SyllabusCreate, _=Depends(require_teacher)):
    try:
        return syllabi.set_syllabus(payload.subject_id, payload.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/syllabus/{subject_id}")
def get_syllabus(subject_id: str, _=Depends(get_current_user)):
    data = syllabi.get_syllabus(subject_id)
    if not data:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    return data


@app.delete("/syllabus/{subject_id}")
def delete_syllabus(subject_id: str, _=Depends(require_teacher)):
    data = syllabi.delete_syllabus(subject_id)
    if not data:
        raise HTTPException(status_code=404, detail="Syllabus not found")
    return data
