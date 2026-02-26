import uuid
from collections import defaultdict
from typing import Optional, List


class TeacherManager:
    def __init__(self):
        self.teachers = []

    def add_teacher(self, name: str, classes: list, contact: str, meta: str):
        teacher = {
            "id": str(uuid.uuid4()),
            "name": name,
            "classes": classes,
            "contact": contact,
            "meta": meta
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
    
    def view_teachers(self, faculty: Optional[str] = None, student_class: Optional[str] = None, degree: Optional[str] = None, section: Optional[str] = None) -> List[dict]):
        result = self.teachers
        if faculty:
            return [s for s in result if s["faculty"] == faculty]
        
        if student_class:
            return [s for s in result if s["student_class"] == student_class]
        
        if degree:
            return [s for s in result if s["degree"] == degree]
        
        if section:
            return [s for s in result if s["section"] == section]
        
        return result

                