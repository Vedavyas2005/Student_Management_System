import customtkinter as ctk
from typing import Optional
from data.database import get_db
from core.auth import hash_password
from gui.common.dialogs import info, error, confirm
from gui.admins.admin_table import AdminTable

db = get_db()

class SuperAdminDashboard(ctk.CTkFrame):
    """
    SuperAdmin dashboard: add / list / delete admin accounts.
    Contains a small embedded AdminCreate form to avoid needing an extra file.
    """
    def __init__(self, master, user):
        super().__init__(master)
        self.user = user
        self._build()

    def _build(self):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=8, pady=(8,6))

        title = ctk.CTkLabel(header, text="Super Admin Dashboard", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(side="left", padx=6)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=(6, 10))

        add_admin_btn = ctk.CTkButton(btn_frame, text="Add Admin", command=self.open_add_admin, width=120)
        add_admin_btn.pack(side="left", padx=6)

        refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=self.refresh_admins, width=120)
        refresh_btn.pack(side="left", padx=6)

        # Admin listing
        self.admin_section = ctk.CTkFrame(self, fg_color="transparent")
        self.admin_section.pack(fill="both", expand=True, padx=8, pady=6)

        admin_label = ctk.CTkLabel(self.admin_section, text="Admins", font=ctk.CTkFont(size=14, weight="bold"))
        admin_label.pack(anchor="w", pady=(4,6))

        self.admin_table = AdminTable(self.admin_section)
        self.admin_table.pack(fill="both", expand=True, padx=6, pady=6)

    def refresh_admins(self):
        try:
            self.admin_table.refresh()
        except Exception:
            pass

    def open_add_admin(self):
        """Open a small modal to create an admin account"""
        AdminCreateForm(self, on_success=self.refresh_admins)

# ---- small modal form embedded to avoid external dependency ----
class AdminCreateForm(ctk.CTkToplevel):
    """
    Minimal admin creation dialog. Creates a users row with role 'admin'.
    """
    def __init__(self, parent, on_success: Optional[callable] = None):
        super().__init__(parent)
        self.parent = parent
        self.on_success = on_success
        self.title("Create Admin")
        self.geometry("420x300")
        self.transient(parent)
        self.lift()
        self.focus_force()
        self._build()

    def _build(self):
        frm = ctk.CTkFrame(self)
        frm.pack(fill="both", expand=True, padx=16, pady=16)

        ctk.CTkLabel(frm, text="Create Admin Account", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(4,8))

        self.full_name = ctk.CTkEntry(frm, placeholder_text="Full name")
        self.full_name.pack(fill="x", pady=6)

        self.email = ctk.CTkEntry(frm, placeholder_text="Email")
        self.email.pack(fill="x", pady=6)

        self.username = ctk.CTkEntry(frm, placeholder_text="Username")
        self.username.pack(fill="x", pady=6)

        self.password = ctk.CTkEntry(frm, placeholder_text="Password", show="*")
        self.password.pack(fill="x", pady=6)

        btn_frame = ctk.CTkFrame(frm, fg_color="transparent")
        btn_frame.pack(fill="x", pady=12)
        ctk.CTkButton(btn_frame, text="Create", command=self._create_admin, width=120).pack(side="left", padx=6)
        ctk.CTkButton(btn_frame, text="Cancel", command=self.destroy, width=120).pack(side="left", padx=6)

    def _create_admin(self):
        name = self.full_name.get().strip()
        email = self.email.get().strip()
        uname = self.username.get().strip()
        pwd = self.password.get().strip()

        if not (name and uname and pwd):
            error("Validation", "Name, username and password are required")
            return

        if db.fetchone("SELECT id FROM users WHERE username=?", (uname,)):
            error("Exists", "Username is already taken")
            return

        # Insert user with role admin
        try:
            db.execute(
                "INSERT INTO users (username, password_hash, full_name, email, role_id) "
                "VALUES (?, ?, ?, ?, (SELECT id FROM roles WHERE name='admin'))",
                (uname, hash_password(pwd), name, email or None)
            )
        except Exception as e:
            error("DB Error", f"Failed to create admin: {e}")
            return

        info("Created", "Admin account created")
        if self.on_success:
            try:
                self.on_success()
            except Exception:
                pass
        self.destroy()
