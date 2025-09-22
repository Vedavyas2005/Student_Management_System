from core.student import add_student, get_all_students, update_student, delete_student, get_student_by_id, map_student_to_user
from core import auth
from data.database import get_db
from config.settings import PLACEMENT_RULES
db = get_db()

def create_student_with_user(student_data: dict, username: str, password: str, full_name: str, email: str):
    # create user with role student
    user_id = auth.create_user(username, password, full_name, email, "student")
    student_data["user_id"] = user_id
    sid = add_student(student_data)
    return sid

def get_students(filters: dict = None):
    # simple filter support
    students = get_all_students()
    if not filters:
        return students
    out = []
    for s in students:
        ok = True
        if "department" in filters and filters["department"] and s.department != filters["department"]:
            ok = False
        if "min_gpa" in filters and s.gpa < float(filters["min_gpa"]):
            ok = False
        if ok:
            out.append(s)
    return out

def check_placement_eligible(student_id: int):
    s = get_student_by_id(student_id)
    if not s:
        return False
    # simple rules: gpa and attendance %
    min_gpa = float(PLACEMENT_RULES["min_gpa"])
    if s.gpa < min_gpa:
        return False
    # attendance calc
    total = db.fetchone("SELECT COUNT(*) as c FROM attendance WHERE student_id = ?", (student_id,))["c"] or 0
    present = db.fetchone("SELECT COUNT(*) as c FROM attendance WHERE student_id = ? AND status = 'present'", (student_id,))["c"] or 0
    percent = (present / total * 100) if total > 0 else 0.0
    if percent < float(PLACEMENT_RULES["min_attendance_percent"]):
        return False
    return True
