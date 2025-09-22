import customtkinter as ctk
from core.auth import hash_password
from data.database import get_db
from gui.common.dialogs import info, error
from typing import Optional

db = get_db()

class StudentForm(ctk.CTkToplevel):
    """
    Add / Edit Student form.
    - If student_id is None -> create new student (optionally create linked user)
    - If student_id provided -> load and edit existing student (no user creation)
    """
    def __init__(self, parent, student_id: Optional[int] = None, on_success: Optional[callable] = None):
        super().__init__(parent)
        self.parent = parent
        self.student_id = student_id
        self.on_success = on_success
        self.title("Student Form")
        self.geometry("420x580")
        self.resizable(False, False)

        self.transient(parent)
        self.lift()
        self.focus_force()

        self._build()
        if self.student_id:
            self._load_student()

    def _build(self):
        frm = ctk.CTkFrame(self, corner_radius=8)
        frm.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(frm, text="Student Details", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(4,10))

        self.roll_no = ctk.CTkEntry(frm, placeholder_text="Roll No")
        self.roll_no.pack(fill="x", pady=6)

        self.first_name = ctk.CTkEntry(frm, placeholder_text="First Name")
        self.first_name.pack(fill="x", pady=6)

        self.last_name = ctk.CTkEntry(frm, placeholder_text="Last Name")
        self.last_name.pack(fill="x", pady=6)

        self.email = ctk.CTkEntry(frm, placeholder_text="Email")
        self.email.pack(fill="x", pady=6)

        self.phone = ctk.CTkEntry(frm, placeholder_text="Phone")
        self.phone.pack(fill="x", pady=6)

        self.department = ctk.CTkEntry(frm, placeholder_text="Department")
        self.department.pack(fill="x", pady=6)

        self.batch = ctk.CTkEntry(frm, placeholder_text="Batch (year)")
        self.batch.pack(fill="x", pady=6)

        self.gpa = ctk.CTkEntry(frm, placeholder_text="GPA (0-10)")
        self.gpa.pack(fill="x", pady=6)

        self.link_user_var = ctk.BooleanVar(value=False)
        self.link_user_chk = ctk.CTkCheckBox(frm, text="Create linked student user account?", variable=self.link_user_var, command=self._toggle_link_inputs)
        self.link_user_chk.pack(anchor="w", pady=(10,6))

        self.username = ctk.CTkEntry(frm, placeholder_text="Username for student")
        self.password = ctk.CTkEntry(frm, placeholder_text="Password for student", show="*")
        # hidden until checkbox selected
        self.username.pack_forget()
        self.password.pack_forget()

        btns = ctk.CTkFrame(frm, fg_color="transparent")
        btns.pack(fill="x", pady=12)
        save_btn = ctk.CTkButton(btns, text="Save", command=self._save, width=120)
        save_btn.pack(side="left", padx=6)
        cancel_btn = ctk.CTkButton(btns, text="Cancel", command=self.destroy, width=120)
        cancel_btn.pack(side="left", padx=6)

    def _toggle_link_inputs(self):
        if self.link_user_var.get():
            self.username.pack(fill="x", pady=6)
            self.password.pack(fill="x", pady=6)
        else:
            self.username.pack_forget()
            self.password.pack_forget()

    def _load_student(self):
        row = db.fetchone("SELECT * FROM students WHERE id=?", (self.student_id,))
        if not row:
            error("Not found", "Student not found")
            self.destroy()
            return
        self.roll_no.insert(0, row["roll_no"])
        self.first_name.insert(0, row["first_name"])
        if row.get("last_name"):
            self.last_name.insert(0, row["last_name"])
        if row.get("email"):
            self.email.insert(0, row["email"])
        if row.get("phone"):
            self.phone.insert(0, row["phone"])
        if row.get("department"):
            self.department.insert(0, row["department"])
        if row.get("batch"):
            self.batch.insert(0, str(row["batch"]))
        if row.get("gpa") is not None:
            self.gpa.insert(0, str(row["gpa"]))

    def _save(self):
        roll = self.roll_no.get().strip()
        first = self.first_name.get().strip()
        last = self.last_name.get().strip()
        email = self.email.get().strip()
        phone = self.phone.get().strip()
        dept = self.department.get().strip()
        batch = self.batch.get().strip()
        gpa = self.gpa.get().strip()

        if not (roll and first):
            error("Validation", "Roll number and first name are required")
            return

        try:
            gpa_val = float(gpa) if gpa else 0.0
        except ValueError:
            error("Validation", "GPA must be numeric")
            return

        if self.student_id:
            # update existing student
            db.execute(
                "UPDATE students SET roll_no=?, first_name=?, last_name=?, email=?, phone=?, department=?, batch=?, gpa=? WHERE id=?",
                (roll, first, last or None, email or None, phone or None, dept or None, int(batch) if batch else None, gpa_val, self.student_id)
            )
            info("Saved", "Student updated")
        else:
            # create user if requested
            user_id = None
            if self.link_user_var.get():
                uname = self.username.get().strip()
                pwd = self.password.get().strip()
                if not (uname and pwd):
                    error("Validation", "Username and password required to create linked account")
                    return
                # check username exists
                if db.fetchone("SELECT id FROM users WHERE username=?", (uname,)):
                    error("Exists", "Username already taken")
                    return
                db.execute(
                    "INSERT INTO users (username, password_hash, full_name, email, role_id) "
                    "VALUES (?, ?, ?, ?, (SELECT id FROM roles WHERE name='student'))",
                    (uname, hash_password(pwd), f"{first} {last}".strip(), email or None)
                )
                user_id = db.fetchone("SELECT id FROM users WHERE username=?", (uname,))["id"]

            # create student record
            db.execute(
                "INSERT INTO students (user_id, roll_no, first_name, last_name, email, phone, department, batch, gpa) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, roll, first, last or None, email or None, phone or None, dept or None, int(batch) if batch else None, gpa_val)
            )
            info("Saved", "Student created")

        if self.on_success:
            try:
                self.on_success()
            except Exception:
                pass

        self.destroy()
