import customtkinter as ctk
from data.database import get_db
from tkinter import ttk

db = get_db()

class AttendanceView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self.lift()

    def _build(self):
        rows = db.fetchall("SELECT a.*, s.roll_no, s.first_name FROM attendance a JOIN students s ON a.student_id=s.id ORDER BY a.date DESC")
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True)
        tree = ttk.Treeview(frame, columns=("roll", "name", "date", "status", "subject"), show="headings")
        for c in ("roll", "name", "date", "status", "subject"):
            tree.heading(c, text=c.title())
        tree.pack(fill="both", expand=True)
        for r in rows:
            tree.insert("", "end", values=(r["roll_no"], r["first_name"], r["date"], r["status"], r["subject"]))
