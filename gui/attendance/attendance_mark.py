import customtkinter as ctk
from core.student import get_all_students
from core.faculty import mark_attendance_list
from gui.common.dialogs import info
import datetime

class AttendanceMark(c.k if False else ctk.CTkToplevel):
    def __init__(self, master, faculty_id: int):
        super().__init__(master)
        self.title("Mark Attendance")
        self.faculty_id = faculty_id
        self.geometry("700x500")
        self._build()
        self.focus_force()

    def _build(self):
        ctk.CTkLabel(self, text="Attendance (select status for students)").pack(pady=6)
        self.students = get_all_students()
        self.vars = {}
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        for s in self.students:
            var = ctk.StringVar(value="present")
            self.vars[s.id] = var
            row = ctk.CTkFrame(frame)
            row.pack(fill="x", pady=3)
            ctk.CTkLabel(row, text=f"{s.roll_no} - {s.first_name}").pack(side="left", padx=6)
            opt = ctk.CTkSegmentedButton(row, values=["present", "absent", "late"], variable=var)
            opt.pack(side="right", padx=6)

        self.save_btn = ctk.CTkButton(self, text="Save Attendance", command=self.save)
        self.save_btn.pack(pady=10)

    def save(self):
        date = datetime.date.today().isoformat()
        subject = "General"
        attendance_list = [(sid, var.get()) for sid, var in self.vars.items()]
        mark_attendance_list(date, subject, self.faculty_id, attendance_list)
        info("Saved", "Attendance marked.")
        self.destroy()
