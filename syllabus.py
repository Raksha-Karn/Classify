from typing import List, Optional

from data_store import DataStore
from models import Syllabus


class SyllabusManager:
    def __init__(self, data_dir: str = "data"):
        self.syllabi: List[Syllabus] = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "syllabi.json"):
        data = self.store.load_list(filename)
        self.syllabi = [Syllabus(**item) for item in data]
        return self.list_dicts()

    def save(self, filename: str = "syllabi.json"):
        self.store.save_list(filename, [s.to_dict() for s in self.syllabi])

    def list_models(self):
        return self.syllabi

    def list_dicts(self):
        return [s.to_dict() for s in self.syllabi]

    def set_syllabus(self, subject_id: str, content: str):
        for s in self.syllabi:
            if s.subject_id == subject_id:
                s.content = content
                return s.to_dict()
        syllabus = Syllabus(subject_id=subject_id, content=content)
        self.syllabi.append(syllabus)
        return syllabus.to_dict()

    def get_syllabus(self, subject_id: str):
        for s in self.syllabi:
            if s.subject_id == subject_id:
                return s.to_dict()
        return None

    def delete_syllabus(self, subject_id: str):
        for i, s in enumerate(self.syllabi):
            if s.subject_id == subject_id:
                return self.syllabi.pop(i).to_dict()
        return None
