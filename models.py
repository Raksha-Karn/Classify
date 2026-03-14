import re
import uuid
from dataclasses import dataclass, field, asdict
from typing import List, Optional


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _optional_non_empty(value: Optional[str], field_name: str) -> Optional[str]:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string when provided")
    return value.strip()


def _validate_email(value: str) -> str:
    value = _require_non_empty(value, "email")
    if not EMAIL_RE.match(value):
        raise ValueError("email must be a valid email address")
    return value


def _optional_int(value: Optional[int], field_name: str) -> Optional[int]:
    if value is None:
        return None
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer when provided")
    return value


def _generate_id() -> str:
    return str(uuid.uuid4())


@dataclass
class Student:
    name: str
    email: str
    contact: str
    student_class: Optional[int] = None
    faculty: Optional[str] = None
    degree: Optional[str] = None
    section: Optional[str] = None
    id: str = field(default_factory=_generate_id)

    def __post_init__(self):
        self.name = _require_non_empty(self.name, "name")
        self.email = _validate_email(self.email)
        self.contact = _require_non_empty(self.contact, "contact")
        self.student_class = _optional_int(self.student_class, "student_class")
        self.faculty = _optional_non_empty(self.faculty, "faculty")
        self.degree = _optional_non_empty(self.degree, "degree")
        self.section = _optional_non_empty(self.section, "section")

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Teacher:
    name: str
    classes: List[int]
    contact: str
    meta: str
    faculty: Optional[str] = None
    degree: Optional[str] = None
    student_class: Optional[int] = None
    section: Optional[str] = None
    id: str = field(default_factory=_generate_id)

    def __post_init__(self):
        self.name = _require_non_empty(self.name, "name")
        if not isinstance(self.classes, list) or not all(isinstance(c, int) for c in self.classes):
            raise ValueError("classes must be a list of integers")
        self.contact = _require_non_empty(self.contact, "contact")
        self.meta = _require_non_empty(self.meta, "meta")
        self.faculty = _optional_non_empty(self.faculty, "faculty")
        self.degree = _optional_non_empty(self.degree, "degree")
        self.student_class = _optional_int(self.student_class, "student_class")
        self.section = _optional_non_empty(self.section, "section")

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Course:
    course_name: str
    course_code: str
    faculty: str
    degree: str
    level_type: str
    level_value: int
    course_class: str
    id: str = field(default_factory=_generate_id)

    def __post_init__(self):
        self.course_name = _require_non_empty(self.course_name, "course_name")
        self.course_code = _require_non_empty(self.course_code, "course_code")
        self.faculty = _require_non_empty(self.faculty, "faculty")
        self.degree = _require_non_empty(self.degree, "degree")
        self.level_type = _require_non_empty(self.level_type, "level_type").lower()
        if self.level_type not in {"class", "semester", "year"}:
            raise ValueError("level_type must be one of: class, semester, year")
        self.level_value = _optional_int(self.level_value, "level_value")
        if self.level_value is None:
            raise ValueError("level_value is required and must be an integer")
        self.course_class = _require_non_empty(self.course_class, "course_class")

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Enrollment:
    student_id: str
    course_id: str
    teacher_id: Optional[str] = None
    status: str = "active"
    id: str = field(default_factory=_generate_id)

    def __post_init__(self):
        self.student_id = _require_non_empty(self.student_id, "student_id")
        self.course_id = _require_non_empty(self.course_id, "course_id")
        self.teacher_id = _optional_non_empty(self.teacher_id, "teacher_id")
        self.status = _require_non_empty(self.status, "status").lower()

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Grade:
    enrollment_id: str
    grade_letter: Optional[str] = None
    grade_numeric: Optional[float] = None
    term: Optional[str] = None
    id: str = field(default_factory=_generate_id)

    def __post_init__(self):
        self.enrollment_id = _require_non_empty(self.enrollment_id, "enrollment_id")
        if self.grade_letter is not None:
            self.grade_letter = _optional_non_empty(self.grade_letter, "grade_letter")
        if self.grade_numeric is not None and not isinstance(self.grade_numeric, (int, float)):
            raise ValueError("grade_numeric must be a number when provided")
        if self.term is not None:
            self.term = _optional_non_empty(self.term, "term")

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class User:
    username: str
    email: str
    password_hash: str
    role: str
    linked_id: Optional[str] = None
    id: str = field(default_factory=_generate_id)

    def __post_init__(self):
        self.username = _require_non_empty(self.username, "username")
        self.email = _validate_email(self.email)
        self.password_hash = _require_non_empty(self.password_hash, "password_hash")
        self.role = _require_non_empty(self.role, "role").lower()
        if self.role not in {"student", "teacher"}:
            raise ValueError("role must be student or teacher")
        self.linked_id = _optional_non_empty(self.linked_id, "linked_id")

    def to_dict(self) -> dict:
        return asdict(self)
