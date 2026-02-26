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

    def edit_teacher(self, teacher_id, **updates):
        for teacher in self.teachers:
            if teacher["id"] == teacher_id:
                for key, value in updates.items():
                    if key in teacher and value is not None:
                        teacher[key] = value
                return teacher
        return None
                