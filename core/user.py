from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class User:
    id: int
    username: str
    full_name: Optional[str]
    email: Optional[str]
    role_id: int
    role_name: str
    last_login: Optional[str] = None

    @staticmethod
    def from_row(row):
        def safe(r, key):
            return r[key] if key in r.keys() else None

        return User(
            id=row["id"],
            username=row["username"],
            full_name=safe(row, "full_name"),
            email=safe(row, "email"),
            role_id=row["role_id"],
            role_name=safe(row, "role_name"),
            last_login=safe(row, "last_login")
        )


    def is_superadmin(self):
        return self.role_name == "superadmin"

    def is_admin(self):
        return self.role_name == "admin"

    def is_faculty(self):
        return self.role_name == "faculty"

    def is_student(self):
        return self.role_name == "student"
