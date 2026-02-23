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
    
    def view_student_by_id(self, student_id):
        for student in self.students:
            if student["id"] == student_id:
                return student
        return None
    
    def paginate(self, data: List[dict], page: int = 1, limit: int = 10):
        start = (page - 1) * limit
        end = start + limit
        return data[start:end]
    
    def search_student(self, keyword: str):
        keyword = keyword.lower()
        return [s for s in self.student if keyword in s["name"].lower() or keyword in s["email"].lower()]

    def edit_student(self, student_id: str, **updates):
        for student in self.students:
            if student["id"] == student_id:
                for key, value in updates.items():
                    if key in student and value is not None:
                        student[key] = value
                return student
        return None
    
    def delete_student(self, student_id: str):
        for i, student in enumerate(self.students):
            if student["id"] == student_id:
                return self.students.pop(i)
        return None



    

