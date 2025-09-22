import customtkinter as ctk
from core.student import get_all_students
from data.database import get_db
from gui.common.dialogs import info

db = get_db()

class GradeEntry(c.k if False else ctk.CTkToplevel):
    def __init__(self, master, faculty_id: int):
        super().__init__(master)
        self.title("Grade Entry")
        self.geometry("600x500")
        self.faculty_id = faculty_id
        self._build()
        self.focus_force()

    def _build(self):
        self.students = get_all_students()
        self.entries = {}
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        for s in self.students:
            row = ctk.CTkFrame(frame)
            row.pack(fill="x", pady=4)
            ctk.CTkLabel(row, text=f"{s.roll_no} - {s.first_name}").pack(side="left", padx=6)
            ent = ctk.CTkEntry(row, placeholder_text="Marks")
            ent.pack(side="right", padx=6)
            self.entries[s.id] = ent
        ctk.CTkButton(self, text="Save Grades", command=self.save).pack(pady=10)

    def save(self):
        subject = "General"
        term = "Term1"
        for sid, ent in self.entries.items():
            val = ent.get().strip()
            if not val:
                continue
            try:
                marks = float(val)
            except:
                continue
            db.execute("INSERT INTO grades (student_id, subject, term, marks, grade, faculty_id) VALUES (?, ?, ?, ?, ?, ?)",
                       (sid, subject, term, marks, None, self.faculty_id))
        info("Saved", "Grades saved.")
        self.destroy()
