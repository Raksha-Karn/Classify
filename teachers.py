from typing import Optional, List

from data_store import DataStore
from models import Teacher

class TeacherManager:
    def __init__(self, data_dir: str = "data"):
        self.teachers = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "teachers.json"):
        data = self.store.load_list(filename)
        self.teachers = [Teacher(**item) for item in data]
        return self.view_teachers()

    def save(self, filename: str = "teachers.json"):
        self.store.save_list(filename, [t.to_dict() for t in self.teachers])

    def add_teacher(
        self,
        name: str,
        classes: list,
        contact: str,
        meta: str,
        faculty: Optional[str] = None,
        degree: Optional[str] = None,
        student_class: Optional[int] = None,
        section: Optional[str] = None,
    ):
        teacher = Teacher(
            name=name,
            classes=classes,
            contact=contact,
            meta=meta,
            faculty=faculty,
            degree=degree,
            student_class=student_class,
            section=section,
        )
        self.teachers.append(teacher)
        return teacher.to_dict()

    def edit_teacher(self, teacher_id: str, **updates):
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                for key, value in updates.items():
                    if hasattr(teacher, key) and value is not None:
                        setattr(teacher, key, value)
                return teacher.to_dict()
        return None
    
    def view_teachers(
        self,
        faculty: Optional[str] = None,
        student_class: Optional[int] = None,
        degree: Optional[str] = None,
        section: Optional[str] = None,
    ) -> List[dict]:
        result = self.teachers
        if faculty:
            return [s.to_dict() for s in result if s.faculty == faculty]
        
        if student_class:
            return [s.to_dict() for s in result if s.student_class == student_class or student_class in s.classes]
        
        if degree:
            return [s.to_dict() for s in result if s.degree == degree]
        
        if section:
            return [s.to_dict() for s in result if s.section == section]
        
        return [s.to_dict() for s in result]
    
    def view_teacher_by_id(self, teacher_id):
        for teacher in self.teachers:
            if teacher.id == teacher_id:
                return teacher.to_dict()
        return None
    
    def delete_teacher(self, teacher_id):
        for i, teacher in enumerate(self.teachers):
            if teacher.id == teacher_id:
                return self.teachers.pop(i).to_dict()
        return None
