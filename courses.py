import uuid 
from collections import defaultdict
from typing import List


class CourseManager:
    def __init__(self):
        self.courses = []

    def add_course(self, course_name:str, course_code:str, faculty:str, degree:str, level_type:str, level_value:str):
        course = {
            "id": uuid.uuid4(),
            "course_code": course_code,
            "course_name": course_name,
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
            level = f"{course["level_type"].capitalize()} {course["level_value"]}"
            grouped = [faculty][degree][level].append(course)
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

    def delete_course(self):
        pass

    def assign_teacher(self):
        pass

    def enroll_student(self):
        pass

    def get_students_in_course(self):
        pass

    def get_courses_of_student(self):
        pass