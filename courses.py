import uuid 


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

    