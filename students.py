from typing import Optional, List

from models import Student

class StudentManager:
    def __init__(self):
        self.students = []

    def add_student(
        self,
        name: str,
        email: str,
        contact: str,
        student_class: Optional[int],
        faculty: Optional[str],
        degree: Optional[str],
        section: Optional[str],
    ):
        student = Student(
            name=name,
            email=email,
            contact=contact,
            student_class=student_class,
            faculty=faculty,
            degree=degree,
            section=section,
        )
        self.students.append(student)
        return student.to_dict()

    def view_students(
        self,
        faculty: Optional[str] = None,
        student_class: Optional[int] = None,
        degree: Optional[str] = None,
        section: Optional[str] = None,
    ) -> List[dict]:
        result = self.students
        if faculty:
            return [s.to_dict() for s in result if s.faculty == faculty]
        
        if student_class:
            return [s.to_dict() for s in result if s.student_class == student_class]
        
        if degree:
            return [s.to_dict() for s in result if s.degree == degree]
        
        if section:
            return [s.to_dict() for s in result if s.section == section]
        
        return [s.to_dict() for s in result]
    
    def view_student_by_id(self, student_id):
        for student in self.students:
            if student.id == student_id:
                return student.to_dict()
        return None
    
    def paginated_view(self, data: List[dict], page: int = 1, limit: int = 10):
        start = (page - 1) * limit
        end = start + limit
        return data[start:end]
    
    def search_student(self, keyword: str):
        keyword = keyword.lower()
        return [
            s.to_dict() for s in self.students
            if keyword in s.name.lower()
            or keyword in s.email.lower()
        ]

    def edit_student(self, student_id: str, **updates):
        for student in self.students:
            if student.id == student_id:
                for key, value in updates.items():
                    if hasattr(student, key) and value is not None:
                        setattr(student, key, value)
                return student.to_dict()
        return None
    
    def delete_student(self, student_id: str):
        for i, student in enumerate(self.students):
            if student.id == student_id:
                return self.students.pop(i).to_dict()
        return None
