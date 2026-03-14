from typing import List, Optional

from data_store import DataStore
from models import Enrollment, Grade


class EnrollmentManager:
    def __init__(self, data_dir: str = "data"):
        self.enrollments: List[Enrollment] = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "enrollments.json"):
        data = self.store.load_list(filename)
        self.enrollments = [Enrollment(**item) for item in data]
        return [e.to_dict() for e in self.enrollments]

    def save(self, filename: str = "enrollments.json"):
        self.store.save_list(filename, [e.to_dict() for e in self.enrollments])

    def list_models(self):
        return self.enrollments

    def list_dicts(self):
        return [e.to_dict() for e in self.enrollments]

    def enroll_student(self, student_id: str, course_id: str, teacher_id: Optional[str] = None):
        enrollment = Enrollment(student_id=student_id, course_id=course_id, teacher_id=teacher_id)
        self.enrollments.append(enrollment)
        return enrollment.to_dict()

    def assign_teacher(self, enrollment_id: str, teacher_id: str):
        for e in self.enrollments:
            if e.id == enrollment_id:
                e.teacher_id = teacher_id
                return e.to_dict()
        return None

    def get_students_in_course(self, course_id: str):
        return [e.student_id for e in self.enrollments if e.course_id == course_id]

    def get_courses_of_student(self, student_id: str):
        return [e.course_id for e in self.enrollments if e.student_id == student_id]

    def list_enrollments(self):
        return [e.to_dict() for e in self.enrollments]

    def delete_enrollment(self, enrollment_id: str):
        for i, e in enumerate(self.enrollments):
            if e.id == enrollment_id:
                return self.enrollments.pop(i).to_dict()
        return None


class GradeManager:
    def __init__(self, data_dir: str = "data"):
        self.grades: List[Grade] = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "grades.json"):
        data = self.store.load_list(filename)
        self.grades = [Grade(**item) for item in data]
        return [g.to_dict() for g in self.grades]

    def save(self, filename: str = "grades.json"):
        self.store.save_list(filename, [g.to_dict() for g in self.grades])

    def list_models(self):
        return self.grades

    def list_dicts(self):
        return [g.to_dict() for g in self.grades]

    def record_grade(
        self,
        enrollment_id: str,
        grade_letter: Optional[str] = None,
        grade_numeric: Optional[float] = None,
        term: Optional[str] = None,
    ):
        grade = Grade(
            enrollment_id=enrollment_id,
            grade_letter=grade_letter,
            grade_numeric=grade_numeric,
            term=term,
        )
        self.grades.append(grade)
        return grade.to_dict()

    def list_grades(self):
        return [g.to_dict() for g in self.grades]

    def get_grades_for_enrollment(self, enrollment_id: str):
        return [g.to_dict() for g in self.grades if g.enrollment_id == enrollment_id]

    def gpa_for_student(self, student_id: str, enrollments: List[Enrollment]) -> Optional[float]:
        enrollment_ids = [e.id for e in enrollments if e.student_id == student_id]
        points = []
        for g in self.grades:
            if g.enrollment_id in enrollment_ids:
                numeric = self.to_numeric(g)
                if numeric is not None:
                    points.append(numeric)
        if not points:
            return None
        return sum(points) / len(points)

    def transcript(self, student_id: str, enrollments: List[Enrollment]):
        enrollment_ids = [e.id for e in enrollments if e.student_id == student_id]
        return [g.to_dict() for g in self.grades if g.enrollment_id in enrollment_ids]

    def to_numeric(self, grade: Grade) -> Optional[float]:
        if grade.grade_numeric is not None:
            return float(grade.grade_numeric)
        if grade.grade_letter is None:
            return None
        mapping = {
            "A+": 4.0,
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D": 1.0,
            "F": 0.0,
        }
        return mapping.get(grade.grade_letter.upper())
