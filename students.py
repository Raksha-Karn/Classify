import uuid


class StudentManager:
    def __init__(self, name, email, contact):
        self.name = name
        self.email = email
        self.contact = contact
        self.enrolled_courses = []
        self.students = [{}]

    def add_student(self):
        self.students.append({
            "Id": uuid.uuid4(),
            "Name": self.name,
            "Email": self.email,
            "Contact": self.contact
        })