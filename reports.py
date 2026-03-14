from collections import Counter
from typing import List, Dict, Any
from datetime import datetime

from data_store import DataStore

from models import Student, Course, Grade, Enrollment


class ReportManager:
    def __init__(self, data_dir: str = "data"):
        self.store = DataStore(data_dir)

    def get_attr(self, item: Any, key: str):
        if isinstance(item, dict):
            return item.get(key)
        return getattr(item, key, None)

    def students_per_class(self, students: List[Any]) -> Dict[int, int]:
        counter = Counter()
        for s in students:
            student_class = self.get_attr(s, "student_class")
            if student_class is not None:
                counter[student_class] += 1
        return dict(counter)

    def students_per_faculty(self, students: List[Any]) -> Dict[str, int]:
        counter = Counter()
        for s in students:
            faculty = self.get_attr(s, "faculty")
            if faculty:
                counter[faculty] += 1
        return dict(counter)

    def courses_per_level(self, courses: List[Any]) -> Dict[str, int]:
        counter = Counter()
        for c in courses:
            level_type = self.get_attr(c, "level_type")
            level_value = self.get_attr(c, "level_value")
            key = f"{level_type}:{level_value}"
            counter[key] += 1
        return dict(counter)

    def enrollment_per_course(self, enrollments: List[Any]) -> Dict[str, int]:
        counter = Counter()
        for e in enrollments:
            course_id = self.get_attr(e, "course_id")
            counter[course_id] += 1
        return dict(counter)

    def grade_distribution(self, grades: List[Any]) -> Dict[str, int]:
        counter = Counter()
        for g in grades:
            grade_letter = self.get_attr(g, "grade_letter")
            grade_numeric = self.get_attr(g, "grade_numeric")
            if grade_letter:
                counter[str(grade_letter).upper()] += 1
            elif grade_numeric is not None:
                key = self.numeric_bucket(grade_numeric)
                counter[key] += 1
        return dict(counter)

    def export_json(self, filename: str, data: Dict[str, Any]):
        filepath = self.store.get_path(filename)
        self.store.backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            import json
            json.dump(data, f, indent=2)

    def export_csv(self, filename: str, data: Dict[str, Any], header_key: str = "key", header_value: str = "value"):
        filepath = self.store.get_path(filename)
        self.store.backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"{header_key},{header_value}\n")
            for key, value in data.items():
                f.write(f"{key},{value}\n")

    def gpa_stats(self, gpa_values: List[float]) -> Dict[str, Any]:
        if not gpa_values:
            return {"count": 0, "min": None, "max": None, "avg": None}
        return {
            "count": len(gpa_values),
            "min": min(gpa_values),
            "max": max(gpa_values),
            "avg": sum(gpa_values) / len(gpa_values),
        }

    def monthly_enrollments(self, enrollments: List[Any]) -> Dict[str, int]:
        counter = Counter()
        for e in enrollments:
            enrolled_at = self.get_attr(e, "enrolled_at")
            month = self.month_key(enrolled_at)
            if month:
                counter[month] += 1
        return dict(counter)

    def monthly_grades(self, grades: List[Any]) -> Dict[str, int]:
        counter = Counter()
        for g in grades:
            recorded_at = self.get_attr(g, "recorded_at")
            month = self.month_key(recorded_at)
            if month:
                counter[month] += 1
        return dict(counter)

    def month_key(self, date_str: Any) -> Any:
        if not date_str:
            return None
        try:
            dt = datetime.fromisoformat(str(date_str))
            return f"{dt.year:04d}-{dt.month:02d}"
        except ValueError:
            return None

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
