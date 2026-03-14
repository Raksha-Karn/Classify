from collections import defaultdict
from typing import List, Optional

from data_store import DataStore
from models import Course


class CourseManager:
    def __init__(self, data_dir: str = "data"):
        self.courses = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "courses.json"):
        data = self.store.load_list(filename)
        self.courses = [Course(**item) for item in data]
        return self.view_courses()

    def save(self, filename: str = "courses.json"):
        self.store.save_list(filename, [c.to_dict() for c in self.courses])

    def add_course(
        self,
        course_name: str,
        course_code: str,
        faculty: str,
        degree: str,
        level_type: str,
        level_value: int,
        course_class: str,
    ):
        course = Course(
            course_name=course_name,
            course_code=course_code,
            faculty=faculty,
            degree=degree,
            level_type=level_type,
            level_value=level_value,
            course_class=course_class,
        )
        self.courses.append(course)
        return course.to_dict()

    def edit_course(self, course_id:str, **updates):
        for course in self.courses:
            if course.id == course_id:
                for key, value in updates.items():
                    if hasattr(course, key) and value is not None:
                        setattr(course, key, value)
                return course.to_dict()
        return None
    
    def view_courses(self):
        grouped = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(list)
            )
        )
        for course in self.courses:
            faculty = course.faculty
            degree = course.degree
            level = f"{course.level_type.capitalize()} {course.level_value}"
            grouped[faculty][degree][level].append(course.to_dict())
        return grouped

    def view_course_by_id(self, course_id):
        for course in self.courses:
            if course.id == course_id:
                return course.to_dict()
        return None
    
    def paginated_view(self, data: List[dict], page: int = 1, limit: int = 10):
        start = (page - 1)*limit
        end = start + limit
        return data[start:end]
    
    def filter_search(self, faculty: Optional[str] = None, degree: Optional[str] = None, course_class: Optional[str] = None):
        result = self.courses
        if faculty:
            result = [s for s in result if s.faculty == faculty]
        if degree:
            result = [s for s in result if s.degree == degree]
        if course_class:
            result = [s for s in result if s.course_class == course_class]
        return [s.to_dict() for s in result]
    
    def search_by_keyword(self, keyword:str):
        keyword = keyword.lower()
        return [
            course.to_dict() for course in self.courses
            if keyword in course.faculty.lower()
            or keyword in course.degree.lower()
            or keyword in course.course_class.lower()
            or keyword in course.course_name.lower()
            or keyword in course.course_code.lower()
        ]

    def delete_course(self, course_id):
        for i, course in enumerate(self.courses):
            if course.id == course_id:
                return self.courses.pop(i).to_dict()
        return None
