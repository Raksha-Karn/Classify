from collections import Counter, defaultdict
from typing import List, Dict

from models import Student, Course, Grade, Enrollment


class ReportManager:
    def __init__(self):
        pass

    def students_per_class(self, students: List[Student]) -> Dict[int, int]:
        counter = Counter()
        for s in students:
            if s.student_class is not None:
                counter[s.student_class] += 1
        return dict(counter)

    def students_per_faculty(self, students: List[Student]) -> Dict[str, int]:
        counter = Counter()
        for s in students:
            if s.faculty:
                counter[s.faculty] += 1
        return dict(counter)

    def courses_per_level(self, courses: List[Course]) -> Dict[str, int]:
        counter = Counter()
        for c in courses:
            key = f"{c.level_type}:{c.level_value}"
            counter[key] += 1
        return dict(counter)

    def enrollment_per_course(self, enrollments: List[Enrollment]) -> Dict[str, int]:
        counter = Counter()
        for e in enrollments:
            counter[e.course_id] += 1
        return dict(counter)

    def grade_distribution(self, grades: List[Grade]) -> Dict[str, int]:
        counter = Counter()
        for g in grades:
            if g.grade_letter:
                counter[g.grade_letter.upper()] += 1
            elif g.grade_numeric is not None:
                key = self.numeric_bucket(g.grade_numeric)
                counter[key] += 1
        return dict(counter)

    def numeric_bucket(self, value: float) -> str:
        if value >= 90:
            return "90-100"
        if value >= 80:
            return "80-89"
        if value >= 70:
            return "70-79"
        if value >= 60:
            return "60-69"
        return "<60"
