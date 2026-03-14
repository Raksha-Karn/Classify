import uuid
from collections import defaultdict
from typing import Optional, List


class TeacherManager:
    def __init__(self):
        self.teachers = []

    def add_teacher(
        self,
        name: str,
        classes: list,
        contact: str,
        meta: str,
        faculty: Optional[str] = None,
        degree: Optional[str] = None,
        student_class: Optional[str] = None,
        section: Optional[str] = None,
    ):
        teacher = {
            "id": str(uuid.uuid4()),
            "name": name,
            "classes": classes,
            "contact": contact,
            "meta": meta,
            "faculty": faculty,
            "degree": degree,
            "student_class": student_class,
            "section": section,
        }

        self.teachers.append(teacher)

    def edit_teacher(self, teacher_id: str, **updates):
        for teacher in self.teachers:
            if teacher["id"] == teacher_id:
                for key, value in updates.items():
                    if key in teacher and value is not None:
                        teacher[key] = value
                return teacher
        return None
    
    def view_teachers(
        self,
        faculty: Optional[str] = None,
        student_class: Optional[str] = None,
        degree: Optional[str] = None,
        section: Optional[str] = None,
    ) -> List[dict]:
        result = self.teachers
        if faculty:
            return [s for s in result if s.get("faculty") == faculty]
        
        if student_class:
            return [s for s in result if s.get("student_class") == student_class or student_class in s.get("classes", [])]
        
        if degree:
            return [s for s in result if s.get("degree") == degree]
        
        if section:
            return [s for s in result if s.get("section") == section]
        
        return result
    
    def view_teacher_by_id(self, teacher_id):
        for teacher in self.teachers:
            if teacher["id"] == teacher_id:
                return teacher
        return None
    
    def delete_teacher(self, teacher_id):
        for i, teacher in enumerate(self.teachers):
            if teacher["id"] == teacher_id:
                return self.teachers.pop(i)
        return None
