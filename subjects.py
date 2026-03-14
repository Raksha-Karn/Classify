from typing import Optional, List

from data_store import DataStore
from models import Subject


class SubjectManager:
    def __init__(self, data_dir: str = "data"):
        self.subjects: List[Subject] = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "subjects.json"):
        data = self.store.load_list(filename)
        self.subjects = [Subject(**item) for item in data]
        return self.list_dicts()

    def save(self, filename: str = "subjects.json"):
        self.store.save_list(filename, [s.to_dict() for s in self.subjects])

    def list_models(self):
        return self.subjects

    def list_dicts(self):
        return [s.to_dict() for s in self.subjects]

    def add_subject(
        self,
        name: str,
        code: str,
        faculty: str,
        degree: str,
        level_type: str,
        level_value: int,
        subject_class: str,
    ):
        subject = Subject(
            name=name,
            code=code,
            faculty=faculty,
            degree=degree,
            level_type=level_type,
            level_value=level_value,
            subject_class=subject_class,
        )
        self.subjects.append(subject)
        return subject.to_dict()

    def view_subjects(
        self,
        faculty: Optional[str] = None,
        degree: Optional[str] = None,
        level_type: Optional[str] = None,
        level_value: Optional[int] = None,
        subject_class: Optional[str] = None,
    ):
        result = self.subjects
        if faculty:
            result = [s for s in result if s.faculty == faculty]
        if degree:
            result = [s for s in result if s.degree == degree]
        if level_type:
            result = [s for s in result if s.level_type == level_type]
        if level_value is not None:
            result = [s for s in result if s.level_value == level_value]
        if subject_class:
            result = [s for s in result if s.subject_class == subject_class]
        return [s.to_dict() for s in result]

    def view_subject_by_id(self, subject_id: str):
        for subject in self.subjects:
            if subject.id == subject_id:
                return subject.to_dict()
        return None

    def edit_subject(self, subject_id: str, **updates):
        for subject in self.subjects:
            if subject.id == subject_id:
                for key, value in updates.items():
                    if hasattr(subject, key) and value is not None:
                        setattr(subject, key, value)
                return subject.to_dict()
        return None

    def delete_subject(self, subject_id: str):
        for i, subject in enumerate(self.subjects):
            if subject.id == subject_id:
                return self.subjects.pop(i).to_dict()
        return None

    def search_subjects(self, keyword: str):
        keyword = keyword.lower()
        return [
            s.to_dict() for s in self.subjects
            if keyword in s.name.lower()
            or keyword in s.code.lower()
            or keyword in s.faculty.lower()
            or keyword in s.degree.lower()
            or keyword in s.subject_class.lower()
        ]
