import uuid


class TeacherManager:
    def __init__(self):
        self.teachers = []

    def add_teacher(self, name, classes, contact, meta):
        teacher = {
            "id": str(uuid.uuid4()),
            "name": name,
            "classes": classes,
            "contact": contact,
            "meta": meta
        }

        self.teachers.append(teacher)