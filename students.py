import uuid
import json
from typing import Optional, List

class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(self, name:str, email:str, contact:str, student_class:str, faculty:str, degree:str, section:str):
        student = {
            "id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "contact": contact,
            "student_class": student_class,
            "faculty": faculty,
            "degree": degree,
            "section": section
        }
        self.students.append(student)

    def view_students(self, faculty: Optional[str] = None, student_class: Optional[str] = None, degree: Optional[str] = None, section: Optional[str] = None) -> List[dict]:
        result = self.students
        if faculty:
            return [s for s in result if s["faculty"] == faculty]
        
        if student_class:
            return [s for s in result if s["student_class"] == student_class]
        
        if degree:
            return [s for s in result if s["degree"] == degree]
        
        if section:
            return [s for s in result if s["section"] == section]
        
        return result



    

