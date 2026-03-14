from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from students import StudentManager
from teachers import TeacherManager
from courses import CourseManager
from enrollment_and_grades import EnrollmentManager, GradeManager
from reports import ReportManager


app = FastAPI(title="Student Management System")

students = StudentManager()
teachers = TeacherManager()
courses = CourseManager()
enrollments = EnrollmentManager()
grades = GradeManager()
reports = ReportManager()


@app.on_event("startup")
def load_data():
    students.load()
    teachers.load()
    courses.load()
    enrollments.load()
    grades.load()


@app.on_event("shutdown")
def save_data():
    students.save()
    teachers.save()
    courses.save()
    enrollments.save()
    grades.save()


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


@app.get("/")
def root():
    return {"status": "ok"}


@app.post("/students")
def add_student(payload: StudentCreate):
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
):
    return students.view_students(
        faculty=faculty,
        student_class=student_class,
        degree=degree,
        section=section,
    )


@app.get("/students/{student_id}")
def get_student(student_id: str):
    student = students.view_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}")
def update_student(student_id: str, updates: Dict[str, Any]):
    try:
        student = students.edit_student(student_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    student = students.delete_student(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.get("/students/search")
def search_students(q: str):
    return students.search_student(q)


@app.post("/teachers")
def add_teacher(payload: TeacherCreate):
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
):
    return teachers.view_teachers(
        faculty=faculty,
        student_class=student_class,
        degree=degree,
        section=section,
    )


@app.get("/teachers/{teacher_id}")
def get_teacher(teacher_id: str):
    teacher = teachers.view_teacher_by_id(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.patch("/teachers/{teacher_id}")
def update_teacher(teacher_id: str, updates: Dict[str, Any]):
    try:
        teacher = teachers.edit_teacher(teacher_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: str):
    teacher = teachers.delete_teacher(teacher_id)
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return teacher


@app.post("/courses")
def add_course(payload: CourseCreate):
    try:
        return courses.add_course(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses")
def list_courses(
    faculty: Optional[str] = None,
    degree: Optional[str] = None,
    course_class: Optional[str] = None,
):
    if faculty or degree or course_class:
        return courses.filter_search(faculty=faculty, degree=degree, course_class=course_class)
    return courses.view_courses()


@app.get("/courses/{course_id}")
def get_course(course_id: str):
    course = courses.view_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.patch("/courses/{course_id}")
def update_course(course_id: str, updates: Dict[str, Any]):
    try:
        course = courses.edit_course(course_id, **updates)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.delete("/courses/{course_id}")
def delete_course(course_id: str):
    course = courses.delete_course(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@app.get("/courses/search")
def search_courses(q: str):
    return courses.search_by_keyword(q)


@app.post("/enrollments")
def enroll_student(payload: EnrollmentCreate):
    try:
        return enrollments.enroll_student(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/enrollments")
def list_enrollments():
    return enrollments.list_dicts()


@app.patch("/enrollments/{enrollment_id}/assign-teacher")
def assign_teacher(enrollment_id: str, teacher_id: str):
    enrollment = enrollments.assign_teacher(enrollment_id, teacher_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@app.delete("/enrollments/{enrollment_id}")
def delete_enrollment(enrollment_id: str):
    enrollment = enrollments.delete_enrollment(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment


@app.post("/grades")
def record_grade(payload: GradeCreate):
    try:
        return grades.record_grade(**payload.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/grades")
def list_grades():
    return grades.list_dicts()


@app.get("/grades/enrollment/{enrollment_id}")
def grades_for_enrollment(enrollment_id: str):
    return grades.get_grades_for_enrollment(enrollment_id)


@app.get("/students/{student_id}/gpa")
def gpa_for_student(student_id: str):
    gpa = grades.gpa_for_student(student_id, enrollments.list_models())
    return {"student_id": student_id, "gpa": gpa}


@app.get("/students/{student_id}/transcript")
def transcript_for_student(student_id: str):
    return grades.transcript(student_id, enrollments.list_models())


@app.get("/reports/students-per-class")
def report_students_per_class():
    return reports.students_per_class(students.list_models())


@app.get("/reports/students-per-faculty")
def report_students_per_faculty():
    return reports.students_per_faculty(students.list_models())


@app.get("/reports/courses-per-level")
def report_courses_per_level():
    return reports.courses_per_level(courses.list_models())


@app.get("/reports/enrollment-per-course")
def report_enrollment_per_course():
    return reports.enrollment_per_course(enrollments.list_models())


@app.get("/reports/grade-distribution")
def report_grade_distribution():
    return reports.grade_distribution(grades.list_models())


@app.post("/reports/export-json")
def export_report_json(filename: str, data: Dict[str, Any]):
    reports.export_json(filename, data)
    return {"status": "ok", "file": filename}


@app.post("/reports/export-csv")
def export_report_csv(filename: str, data: Dict[str, Any], header_key: str = "key", header_value: str = "value"):
    reports.export_csv(filename, data, header_key=header_key, header_value=header_value)
    return {"status": "ok", "file": filename}
