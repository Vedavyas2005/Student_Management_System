from data.database import get_db
db = get_db()

def mark_attendance_list(date: str, subject: str, faculty_id: int, attendance_list: list):
    """
    attendance_list: list of tuples (student_id, status) where status in {"present","absent","late"}
    """
    for sid, status in attendance_list:
        db.execute(
            "INSERT INTO attendance (student_id, date, status, subject, faculty_id) VALUES (?, ?, ?, ?, ?)",
            (sid, date, status, subject, faculty_id)
        )
    db.execute("INSERT INTO audit_logs (user_id, action, target_table, target_id, details) VALUES (?, ?, ?, ?, ?)",
               (faculty_id, "mark_attendance", "attendance", None, f"Marked attendance for {subject} on {date}"))

def get_attendance_for_student(student_id: int):
    rows = db.fetchall("SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC", (student_id,))
    return rows
