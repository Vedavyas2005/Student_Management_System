import customtkinter as ctk
from core.auth import hash_password
from data.database import get_db
from gui.common.dialogs import info, error
from typing import Optional

db = get_db()

class FacultyForm(ctk.CTkToplevel):
    def __init__(self, parent, on_success: Optional[callable] = None):
        super().__init__(parent)
        self.on_success = on_success
        self.title("Add Faculty")
        self.geometry("420x460")
        self.transient(parent)
        self.lift()
        self.focus_force()
        self._build()

    def _build(self):
        frm = ctk.CTkFrame(self)
        frm.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(frm, text="Add Faculty", font=ctk.CTkFont(size=15, weight="bold")).pack(pady=(4,10))

        self.full_name = ctk.CTkEntry(frm, placeholder_text="Full Name")
        self.full_name.pack(fill="x", pady=6)

        self.email = ctk.CTkEntry(frm, placeholder_text="Email")
        self.email.pack(fill="x", pady=6)

        self.username = ctk.CTkEntry(frm, placeholder_text="Username")
        self.username.pack(fill="x", pady=6)

        self.password = ctk.CTkEntry(frm, placeholder_text="Password", show="*")
        self.password.pack(fill="x", pady=6)

        self.department = ctk.CTkEntry(frm, placeholder_text="Department")
        self.department.pack(fill="x", pady=6)

        self.salary = ctk.CTkEntry(frm, placeholder_text="Salary")
        self.salary.pack(fill="x", pady=6)

        btns = ctk.CTkFrame(frm, fg_color="transparent")
        btns.pack(fill="x", pady=12)
        ctk.CTkButton(btns, text="Save", command=self._save, width=120).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Cancel", command=self.destroy, width=120).pack(side="left", padx=6)

    def _save(self):
        name = self.full_name.get().strip()
        email = self.email.get().strip()
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        dept = self.department.get().strip()
        salary_text = self.salary.get().strip()

        if not (name and uname and pwd):
            error("Validation", "Full name, username and password are required")
            return

        try:
            salary_val = float(salary_text) if salary_text else 0.0
        except ValueError:
            error("Validation", "Salary must be numeric")
            return

        if db.fetchone("SELECT id FROM users WHERE username=?", (uname,)):
            error("Exists", "Username taken")
            return


        db.execute(
            "INSERT INTO users (username, password_hash, full_name, email, role_id) "
            "VALUES (?, ?, ?, ?, (SELECT id FROM roles WHERE name='faculty'))",
            (uname, hash_password(pwd), name, email or None)
        )

        user_id = db.fetchone("SELECT id FROM users WHERE username=?", (uname,))["id"]

        db.execute(
            "INSERT INTO faculty (user_id, department, salary, salary_pending) VALUES (?, ?, ?, ?)",
            (user_id, dept or None, salary_val, salary_val)
        )

        info("Success", "Faculty created")
        if self.on_success:
            try:
                self.on_success()
            except Exception:
                pass

        self.destroy()
