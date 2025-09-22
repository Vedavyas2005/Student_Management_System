import customtkinter as ctk
from core.user import User
from gui.dashboards.superadmin_dashboard import SuperAdminDashboard
from gui.dashboards.admin_dashboard import AdminDashboard
from gui.dashboards.faculty_dashboard import FacultyDashboard
from gui.dashboards.student_dashboard import StudentDashboard
from config.settings import APP_TITLE, WINDOW_SIZE, THEME
from gui.common.theme_manager import theme_manager       #USE THIS THEME_MANAGER to make changes to theme
from gui.common.dialogs import info
import tkinter as tk

class MainWindow(ctk.CTk):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.title(f"{APP_TITLE} — {user.full_name or user.username} ({user.role_name})")
        self.geometry(WINDOW_SIZE)
        theme_manager.apply(self)
        self._build_ui()
        self.mainloop()

    def _build_ui(self):
        # left nav
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=8)
        self.sidebar.pack(side="left", fill="y", padx=12, pady=12)

        self.content = ctk.CTkFrame(self, corner_radius=8)
        self.content.pack(side="left", fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(self.sidebar, text=f"Hello, {self.user.full_name or self.user.username}", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=8)

        if self.user.is_superadmin():
            btn = ctk.CTkButton(self.sidebar, text="Super Admin Dashboard", command=self.show_superadmin)
            btn.pack(pady=6, fill="x")
        if self.user.is_admin() or self.user.is_superadmin():
            btn = ctk.CTkButton(self.sidebar, text="Admin Dashboard", command=self.show_admin)
            btn.pack(pady=6, fill="x")
        if self.user.is_faculty() or self.user.is_admin():
            btn = ctk.CTkButton(self.sidebar, text="Faculty Dashboard", command=self.show_faculty)
            btn.pack(pady=6, fill="x")
        if self.user.is_student():
            btn = ctk.CTkButton(self.sidebar, text="Student Dashboard", command=self.show_student)
            btn.pack(pady=6, fill="x")

        # logout and theme toggle
        ctk.CTkButton(self.sidebar, text="Toggle Theme", command=self.toggle_theme).pack(side="bottom", pady=6, padx=12, fill="x")
        ctk.CTkButton(self.sidebar, text="Logout", command=self.logout).pack(side="bottom", pady=6, padx=12, fill="x")

        # default view
        self.current_view = None
        self.show_default()

    def clear_content(self):
        for w in self.content.winfo_children():
            w.destroy()

    def show_default(self):
        self.clear_content()
        lbl = ctk.CTkLabel(self.content, text=f"Welcome to {APP_TITLE}\nRole: {self.user.role_name}", font=ctk.CTkFont(size=20, weight="bold"))
        lbl.pack(expand=True)

    def show_superadmin(self):
        self.clear_content()
        SuperAdminDashboard(self.content, self.user).pack(fill="both", expand=True)

    def show_admin(self):
        self.clear_content()
        AdminDashboard(self.content, self.user).pack(fill="both", expand=True)

    def show_faculty(self):
        self.clear_content()
        FacultyDashboard(self.content, self.user).pack(fill="both", expand=True)

    def show_student(self):
        self.clear_content()
        StudentDashboard(self.content, self.user).pack(fill="both", expand=True)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")


    def logout(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        from gui.login_window import LoginWindow
        self.destroy()   # close main window
        LoginWindow().mainloop()
