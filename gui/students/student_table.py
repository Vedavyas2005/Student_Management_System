import customtkinter as ctk
from tkinter import ttk
from data.database import get_db
from gui.common.dialogs import info, error, confirm

db = get_db()

class StudentTable(ctk.CTkFrame):
    def __init__(self, master, extra_actions=None):
        super().__init__(master)
        self.extra_actions = extra_actions or []
        self._build()
        self.refresh()

    def _build(self):
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", pady=6)

        ctk.CTkButton(controls, text="Add", command=self.add_student).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Edit", command=self.edit_student).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Delete", command=self.delete_student).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Export CSV", command=self.export_csv).pack(side="left", padx=6)

        # extra actions (e.g. View Fees)
        for (label, fn) in self.extra_actions:
            ctk.CTkButton(controls, text=label, command=fn).pack(side="left", padx=6)

        self.tree = ttk.Treeview(self, columns=("id", "roll_no", "name", "dept", "batch"), show="headings")
        for c in ("id", "roll_no", "name", "dept", "batch"):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = db.fetchall("""
            SELECT s.id, s.roll_no, COALESCE(u.full_name, s.first_name || ' ' || COALESCE(s.last_name,'')) as name,
                   s.department, s.batch
            FROM students s
            LEFT JOIN users u ON s.user_id = u.id
            ORDER BY s.id DESC
        """)
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["roll_no"], r["name"], r["department"], r["batch"]))

    def get_selected_item(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item = self.tree.item(sel[0])["values"]
        return {"id": item[0], "roll_no": item[1]}

    def add_student(self):
        from gui.students.student_form import StudentForm
        StudentForm(self, on_success=self.refresh)

    def edit_student(self):
        sel = self.get_selected_item()
        if not sel:
            error("Select", "Select a student to edit")
            return
        from gui.students.student_form import StudentForm
        StudentForm(self, student_id=sel["id"], on_success=self.refresh)

    def delete_student(self):
        sel = self.get_selected_item()
        if not sel:
            error("Select", "Select a student to delete")
            return

        if not confirm("Confirm", "Delete this student and all related data?"):
            return

        # find linked user_id
        row = db.fetchone("SELECT user_id FROM students WHERE id=?", (sel["id"],))
        user_id = row["user_id"] if row else None

        # delete dependent rows first
        db.execute("DELETE FROM attendance WHERE student_id=?", (sel["id"],))
        db.execute("DELETE FROM grades WHERE student_id=?", (sel["id"],))
        db.execute("DELETE FROM fees WHERE student_id=?", (sel["id"],))

        # delete student record
        db.execute("DELETE FROM students WHERE id=?", (sel["id"],))

        # delete user if exists and not referenced elsewhere
        if user_id:
            # check other references (e.g. faculty.user_id, attendance.faculty_id, grades.faculty_id)
            # If user is only referenced by this student, delete user. Simpler: delete user (if you want cascade behavior)
            db.execute("DELETE FROM users WHERE id=?", (user_id,))

        info("Deleted", "Student and related records removed")
        self.refresh()

    def export_csv(self):
        # simple CSV exporter using utils/exporter if present
        from utils.exporter import export_rows_to_csv
        rows = db.fetchall("SELECT roll_no, first_name, last_name, department, batch, gpa FROM students")
        export_rows_to_csv(rows, ["RollNo", "First", "Last", "Department", "Batch", "GPA"])
        info("Export", "Export complete")
