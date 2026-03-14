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


