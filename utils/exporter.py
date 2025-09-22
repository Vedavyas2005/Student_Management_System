from data.database import get_db
from utils.helpers import write_csv
db = get_db()

def export_students_to_csv(filepath: str, filters: dict = None):
    query = "SELECT roll_no, first_name, last_name, department, batch, email, phone, gpa FROM students ORDER BY roll_no"
    rows = db.fetchall(query)
    out = []
    for r in rows:
        out.append([r["roll_no"], r["first_name"], r["last_name"], r["department"], r["batch"], r["email"], r["phone"], r["gpa"]])
    headers = ["Roll No", "First Name", "Last Name", "Department", "Batch", "Email", "Phone", "GPA"]
    write_csv(filepath, out, headers)
