import uuid 
from collections import defaultdict
from typing import List, Optional


class CourseManager:
    def __init__(self):
        self.courses = []

    def add_course(self, course_name:str, course_code:str, faculty:str, degree:str, level_type:str, level_value:str, course_class:str):
        course = {
            "id": str(uuid.uuid4()),
            "course_code": course_code,
            "course_name": course_name,
            "course_class": course_class,
            "faculty": faculty,
            "degree": degree,
            "level_type": level_type,
            "level_value": level_value
        }
        self.courses.append(course)

    def edit_course(self, course_id:str, **updates):
        for course in self.courses:
            if course["id"] == course_id:
                for key, value in updates.items():
                    if key in course and value is not None:
                        course[key] = value
                return course
        return None
    
    def view_courses(self):
        grouped = defaultdict(
            lambda: defaultdict(
                lambda: defaultdict(list)
            )
        )
        for course in self.courses:
            faculty = course["faculty"]
            degree = course["degree"]
            level = f"{course['level_type'].capitalize()} {course['level_value']}"
            grouped[faculty][degree][level].append(course)
        return grouped

    def view_course_by_id(self, course_id):
        for course in self.courses:
            if course["id"] == course_id:
                return course
        return None
    
    def paginated_view(self, data: List[dict], page: int = 1, limit: int = 10):
        start = (page - 1)*limit
        end = start + limit
        return data[start:end]
    
    def filter_search(self, faculty: Optional[str] = None, degree: Optional[str] = None, course_class: Optional[str] = None):
        result = self.courses
        if faculty:
            result = [s for s in result if s["faculty"] == faculty]
        if degree:
            result = [s for s in result if s["degree"] == degree]
        if course_class:
            result = [s for s in result if s["course_class"] == course_class]
        return result
    
    def search_by_keyword(self, keyword:str):
        keyword = keyword.lower()
        return [
            course for course in self.courses
            if keyword in course["faculty"].lower()
            or keyword in course["degree"].lower()
            or keyword in course["course_class"].lower()
            or keyword in course["course_name"].lower()
            or keyword in course["course_code"].lower()
        ]

    def delete_course(self, course_id):
        for i, course in enumerate(self.courses):
            if course["id"] == course_id:
                return self.courses.pop(i)
        return None

    def assign_teacher(self):
        pass

    def enroll_student(self):
        pass

    def get_students_in_course(self):
        pass

    def get_courses_of_student(self):
        pass
