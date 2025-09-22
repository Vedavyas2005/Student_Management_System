import customtkinter as ctk
from core.student import get_student_by_id

class StudentProfileView(ctk.CTkFrame):
    def __init__(self, master, student_id: int):
        super().__init__(master)
        self.student_id = student_id
        self._build()

    def _build(self):
        s = get_student_by_id(self.student_id)
        if not s:
            ctk.CTkLabel(self, text="Student not found").pack()
            return
        info = f"Roll: {s.roll_no}\nName: {s.first_name} {s.last_name or ''}\nDept: {s.department}\nBatch: {s.batch}\nGPA: {s.gpa}"
        ctk.CTkLabel(self, text=info).pack(pady=12)
