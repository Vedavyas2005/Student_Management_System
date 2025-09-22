import customtkinter as ctk
from core import auth
from gui.main_window import MainWindow
from config.settings import APP_TITLE, WINDOW_SIZE, THEME
from gui.common.theme_manager import theme_manager
from core.user import User
from gui.common.dialogs import info, error
import tkinter as tk
from data.database import get_db

db = get_db()
class SetupSuperAdmin(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Superadmin Setup")
        self.geometry("400x400")

        ctk.CTkLabel(self, text="Create Superadmin Account", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)

        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=8)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=8)

        self.fullname = ctk.CTkEntry(self, placeholder_text="Full Name")
        self.fullname.pack(pady=8)

        self.email = ctk.CTkEntry(self, placeholder_text="Email")
        self.email.pack(pady=8)

        self.save_btn = ctk.CTkButton(self, text="Create Superadmin", command=self.save)
        self.save_btn.pack(pady=15)

    def save(self):
        from core import auth
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        full = self.fullname.get().strip()
        email = self.email.get().strip()

        if not uname or not pwd:
            from gui.common.dialogs import error
            error("Validation", "Username and Password are required")
            return
        try:
            auth.create_user(uname, pwd, full or uname, email or None, "superadmin")
            from gui.common.dialogs import info
            info("Success", "Superadmin created. Please login now.")
            self.destroy()
        except Exception as e:
            from gui.common.dialogs import error
            error("Error", f"Failed: {e}")

class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE + " — Login")
        self.geometry(WINDOW_SIZE)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # DPI awareness for Windows
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

        theme_manager.apply(self)

        # header
        self.header = ctk.CTkLabel(self, text="Welcome to SMS", font=ctk.CTkFont(size=24, weight="bold"))
        self.header.pack(pady=(30,10))

        # username/password
        self.username = ctk.CTkEntry(self, placeholder_text="Username")
        self.username.pack(pady=8, ipadx=10, ipady=6)

        self.password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password.pack(pady=8, ipadx=10, ipady=6)

        # login button
        self.login_btn = ctk.CTkButton(self, text="Login", command=self._try_login)
        self.login_btn.pack(pady=12, ipadx=10, ipady=6)

        # theme toggle
        self.theme_btn = ctk.CTkButton(self, text="Toggle Theme", command=self.toggle_theme, width=130)
        self.theme_btn.pack(side="bottom", pady=10)

        # on first-run this will get executed, if no superadmin exists - it will prompt creation
        self._ensure_superadmin_exists()

    def _ensure_superadmin_exists(self):
        row = db.fetchone("SELECT u.* FROM users u JOIN roles r ON u.role_id=r.id WHERE r.name='superadmin' LIMIT 1")
        if not row:
            SetupSuperAdmin(self)
            
            """
            # create a minimal superadmin via basic tkinter module
            from tkinter.simpledialog import askstring
            info("First time setup", "No superadmin found. Create a superadmin account.")
            username = askstring("Superadmin Setup", "Choose username (eg: superadmin)")
            if not username:
                error("Setup Cancelled", "Superadmin setup is required. Exiting.")
                self.destroy()
                return
            pwd = askstring("Superadmin Setup", f"Choose password for {username}", show="*")
            if not pwd:
                error("Setup Cancelled", "Superadmin setup is required. Exiting.")
                self.destroy()
                return
            full = askstring("Superadmin Setup", "Full name (optional)")
            email = askstring("Superadmin Setup", "Email (optional)")
            try:
                auth.create_user(username, pwd, full or username, email or None, "superadmin")
                info("Success", "Superadmin created. You can login now.")
            except Exception as e:
                error("Error", f"Failed to create superadmin: {e}")
                self.destroy()
                """

    def _try_login(self):
        uname = self.username.get().strip()
        pwd = self.password.get().strip()
        if not uname or not pwd:
            error("Validation", "Enter username and password.")
            return
        user = auth.login(uname, pwd)
        if not user:
            error("Login Failed", "Wrong credentials.")
            return
        self.destroy()
        MainWindow(user)

    def toggle_theme(self):
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
        else:
            ctk.set_appearance_mode("dark")

    
    def on_close(self):
        self.destroy()