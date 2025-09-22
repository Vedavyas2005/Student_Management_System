import customtkinter as ctk
from core.user import User
from gui.attendance.attendance_mark import AttendanceMark
from gui.attendance.attendance_view import AttendanceView
from gui.grades.grade_entry import GradeEntry
from gui.grades.grade_view import GradeView

class FacultyDashboard(ctk.CTkFrame):
    def __init__(self, master, user: User):
        super().__init__(master)
        self.user = user
        self._build()

    def _build(self):
        header = ctk.CTkLabel(self, text="Faculty Dashboard", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=8, anchor="w")

        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", padx=12, pady=(6, 0))

        ctk.CTkButton(controls, text="Mark Attendance", command=self.open_attendance, width=150).pack(side="left", padx=6, pady=6)
        ctk.CTkButton(controls, text="Enter Grades", command=self.open_grades, width=150).pack(side="left", padx=6, pady=6)
        ctk.CTkButton(controls, text="View Attendance Records", command=self.view_attendance, width=200).pack(side="left", padx=6, pady=6)
        ctk.CTkButton(controls, text="View Grades Records", command=self.view_grades, width=200).pack(side="left", padx=6, pady=6)

    def open_attendance(self):
        AttendanceMark(self, self.user.id)
        self.lift()

    def open_grades(self):
        GradeEntry(self, self.user.id)
        self.lift()

    def view_attendance(self):
        win = ctk.CTkToplevel(self)
        win.title("Attendance Records")
        win.geometry("700x500")
        AttendanceView(win).pack(fill="both", expand=True)
        self.lift()

    def view_grades(self):
        win = ctk.CTkToplevel(self)
        win.title("Grades Records")
        win.geometry("700x500")
        GradeView(win).pack(fill="both", expand=True)
        self.lift()
