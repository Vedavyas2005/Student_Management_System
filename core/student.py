from dataclasses import dataclass
from typing import Optional
from data.database import get_db
db = get_db()

@dataclass
class Student:
    id: int
    user_id: Optional[int]
    roll_no: str
    first_name: str
    last_name: Optional[str]
    dob: Optional[str]
    department: Optional[str]
    batch: Optional[int]
    email: Optional[str]
    phone: Optional[str]
    gpa: float

    @staticmethod
    def from_row(row):
        def safe(r, key):
            return r[key] if key in r.keys() else None

        return Student(
            id=row["id"],
            user_id=safe(row, "user_id"),
            roll_no=row["roll_no"],
            first_name=row["first_name"],
            last_name=safe(row, "last_name"),
            dob=safe(row, "dob"),
            department=safe(row, "department"),
            batch=safe(row, "batch"),
            email=safe(row, "email"),
            phone=safe(row, "phone"),
            gpa=safe(row, "gpa") or 0.0
        )

def add_student(data: dict) -> int:
    cur = db.execute(
        """INSERT INTO students (user_id, roll_no, first_name, last_name, dob, department, batch, email, phone, gpa)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (data.get("user_id"),
         data["roll_no"],
         data["first_name"],
         data.get("last_name"),
         data.get("dob"),
         data.get("department"),
         data.get("batch"),
         data.get("email"),
         data.get("phone"),
         data.get("gpa", 0.0))
    )
    sid = cur.lastrowid
    _log_action(None, "add_student", "students", sid, f"Added student {data['roll_no']}")
    return sid

def update_student(student_id: int, data: dict):
    db.execute(
        """UPDATE students SET roll_no=?, first_name=?, last_name=?, dob=?, department=?, batch=?, email=?, phone=?, gpa=?, user_id=?
           WHERE id=?""",
        (data["roll_no"], data["first_name"], data.get("last_name"), data.get("dob"), data.get("department"),
         data.get("batch"), data.get("email"), data.get("phone"), data.get("gpa", 0.0), data.get("user_id"), student_id)
    )
    _log_action(None, "update_student", "students", student_id, f"Updated student {student_id}")

def delete_student(student_id: int):
    db.execute("DELETE FROM students WHERE id=?", (student_id,))
    _log_action(None, "delete_student", "students", student_id, f"Deleted student {student_id}")

def get_all_students() -> list:
    rows = db.fetchall("SELECT * FROM students ORDER BY roll_no")
    return [Student.from_row(r) for r in rows]

def get_student_by_id(student_id: int):
    row = db.fetchone("SELECT * FROM students WHERE id=?", (student_id,))
    return Student.from_row(row) if row else None

def map_student_to_user(student_id: int, user_id: int):
    db.execute("UPDATE students SET user_id = ? WHERE id = ?", (user_id, student_id))
    _log_action(None, "map_student", "students", student_id, f"Mapped student to user {user_id}")

def _log_action(user_id, action, table, target_id, details):
    db.execute("INSERT INTO audit_logs (user_id, action, target_table, target_id, details) VALUES (?, ?, ?, ?, ?)",
               (user_id, action, table, target_id, details))
