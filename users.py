from typing import Optional, List

from data_store import DataStore
from models import User
from auth_utils import hash_password, verify_password


class UserManager:
    def __init__(self, data_dir: str = "data"):
        self.users: List[User] = []
        self.store = DataStore(data_dir)

    def load(self, filename: str = "users.json"):
        data = self.store.load_list(filename)
        self.users = [User(**item) for item in data]
        return [u.to_dict() for u in self.users]

    def save(self, filename: str = "users.json"):
        self.store.save_list(filename, [u.to_dict() for u in self.users])

    def list_dicts(self):
        return [u.to_dict() for u in self.users]

    def find_by_id(self, user_id: str) -> Optional[User]:
        for u in self.users:
            if u.id == user_id:
                return u
        return None

    def find_by_username(self, username: str) -> Optional[User]:
        for u in self.users:
            if u.username == username:
                return u
        return None

    def find_by_email(self, email: str) -> Optional[User]:
        for u in self.users:
            if u.email == email:
                return u
        return None

    def create_user(self, username: str, email: str, password: str, role: str, linked_id: Optional[str]):
        if self.find_by_username(username) or self.find_by_email(email):
            raise ValueError("username or email already exists")
        password_hash = hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            linked_id=linked_id,
        )
        self.users.append(user)
        return user.to_dict()

    def authenticate(self, login: str, password: str) -> Optional[User]:
        user = self.find_by_username(login) or self.find_by_email(login)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return user

    def reset_password(self, email: str, new_password: str) -> bool:
        user = self.find_by_email(email)
        if not user:
            return False
        user.password_hash = hash_password(new_password)
        return True
