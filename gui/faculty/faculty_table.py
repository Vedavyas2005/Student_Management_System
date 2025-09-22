import customtkinter as ctk
from tkinter import ttk
from data.database import get_db
from gui.common.dialogs import info, error, confirm
from gui.faculty.faculty_payment_form import FacultyPaymentForm

db = get_db()

class FacultyTable(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self.refresh()

    def _build(self):
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", pady=6)

        ctk.CTkButton(controls, text="Add", command=self.add_faculty).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Delete", command=self.delete_faculty).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Pay Salary", command=self.pay_salary).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Refresh", command=self.refresh).pack(side="left", padx=6)

        self.tree = ttk.Treeview(self, columns=("id","name","email","username","dept","salary","pending"), show="headings")
        for col in ("id","name","email","username","dept","salary","pending"):
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        rows = db.fetchall("""
            SELECT f.id, u.full_name, u.email, u.username, f.department, f.salary, f.salary_pending
            FROM faculty f
            JOIN users u ON f.user_id = u.id
            ORDER BY f.id DESC
        """)
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["full_name"], r["email"], r["username"], r["department"], r["salary"], r["salary_pending"]))

    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item = self.tree.item(sel[0])["values"]
        return {"id": item[0], "username": item[3]}

    def add_faculty(self):
        from gui.faculty.faculty_form import FacultyForm
        FacultyForm(self, on_success=self.refresh)

    def delete_faculty(self):
        sel = self.get_selected()
        if not sel:
            error("Select", "Select a faculty to delete")
            return
        if not confirm("Confirm", "Delete this faculty and related records?"):
            return

        row = db.fetchone("SELECT user_id FROM faculty WHERE id=?", (sel["id"],))
        user_id = row["user_id"] if row else None

        # delete dependent payment records first
        db.execute("DELETE FROM faculty_salary_payments WHERE faculty_id=?", (sel["id"],))
        # delete faculty row
        db.execute("DELETE FROM faculty WHERE id=?", (sel["id"],))

        # delete user
        if user_id:
            db.execute("DELETE FROM users WHERE id=?", (user_id,))

        info("Deleted", "Faculty and related records removed")
        self.refresh()

    def pay_salary(self):
        sel = self.get_selected()
        if not sel:
            error("Select", "Select a faculty to pay")
            return
        FacultyPaymentForm(self, faculty_id=sel["id"], on_success=self.refresh)
