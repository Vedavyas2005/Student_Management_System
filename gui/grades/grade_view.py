import customtkinter as ctk
from data.database import get_db
from tkinter import ttk

db = get_db()

class GradeView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self.lift()

    def _build(self):
        rows = db.fetchall("SELECT g.*, s.roll_no, s.first_name FROM grades g JOIN students s ON g.student_id=s.id ORDER BY g.created_at DESC")
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("roll", "name", "subject", "term", "marks"), show="headings")
        for c in ("roll", "name", "subject", "term", "marks"):
            tree.heading(c, text=c.title())
        tree.pack(fill="both", expand=True)
        for r in rows:
            tree.insert("", "end", values=(r["roll_no"], r["first_name"], r["subject"], r["term"], r["marks"]))
