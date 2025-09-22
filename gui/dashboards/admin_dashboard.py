import customtkinter as ctk
from core.user import User
from data.database import get_db
from gui.students.student_table import StudentTable
from gui.faculty.faculty_table import FacultyTable
from gui.faculty.faculty_form import FacultyForm
from gui.fees.fee_manager import FeeManager
from gui.fees.fee_invoices import FeeInvoice
from gui.common.dialogs import error, info

db = get_db()

class AdminDashboard(ctk.CTkFrame):
    """
    Admin dashboard: Manage students, faculty and fees.
    Expects `user` to be a core.user.User instance representing the logged-in admin.
    """
    def __init__(self, master, user: User):
        super().__init__(master)
        self.user = user
        self._build()

    def _build(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(8, 6), padx=8)

        title = ctk.CTkLabel(header_frame, text="Admin Dashboard", font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(side="left", padx=6)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=8, pady=(6, 10))

        fees_btn = ctk.CTkButton(btn_frame, text="Manage Fees", command=self.open_fee_manager, width=120)
        fees_btn.pack(side="left", padx=6)

        add_faculty_btn = ctk.CTkButton(btn_frame, text="Add Faculty", command=self.add_faculty, width=120)
        add_faculty_btn.pack(side="left", padx=6)

        delete_faculty_btn = ctk.CTkButton(btn_frame, text="Delete Faculty", command=self.delete_faculty, width=120)
        delete_faculty_btn.pack(side="left", padx=6)

        refresh_btn = ctk.CTkButton(btn_frame, text="Refresh", command=self.refresh, width=120)
        refresh_btn.pack(side="left", padx=6)

        # main content in here: Student table (top) and Faculty table (bottom)
        self.student_section = ctk.CTkFrame(self, fg_color="transparent")
        self.student_section.pack(fill="both", expand=True, padx=8, pady=(6, 8))

        student_label = ctk.CTkLabel(self.student_section, text="Student Management", font=ctk.CTkFont(size=14, weight="bold"))
        student_label.pack(anchor="w", pady=(4, 6))

        # StudentTable supports extra actions; pass "View Fees" which will open FeeInvoice
        self.student_table = StudentTable(self.student_section, extra_actions=[("View Fees", self.open_fee_invoice)])
        self.student_table.pack(fill="both", expand=True, padx=6, pady=6)

        # faculty section
        self.faculty_section = ctk.CTkFrame(self, fg_color="transparent")
        self.faculty_section.pack(fill="both", expand=True, padx=8, pady=(6, 8))

        faculty_label = ctk.CTkLabel(self.faculty_section, text="Faculty Management", font=ctk.CTkFont(size=14, weight="bold"))
        faculty_label.pack(anchor="w", pady=(4, 6))

        self.fac_table = FacultyTable(self.faculty_section)
        self.fac_table.pack(fill="both", expand=True, padx=6, pady=6)

    def refresh(self):
        """Refresh both student and faculty tables"""
        try:
            if hasattr(self, "student_table") and self.student_table:
                self.student_table.refresh()
            if hasattr(self, "fac_table") and self.fac_table:
                self.fac_table.refresh()
        except Exception:
            # swallow unexpected refresh errors gracefully
            pass

    def add_faculty(self):
        """Open the Add Faculty form"""
        FacultyForm(self, on_success=self.refresh)

    def delete_faculty(self):
        """Trigger faculty deletion flow from faculty table"""
        try:
            self.fac_table.delete_faculty()
        except Exception as e:
            error("Delete Error", f"Could not delete faculty: {e}")

    def open_fee_manager(self):
        """Open fee manager window"""
        FeeManager(self)

    def open_fee_invoice(self):
        """Open fee invoice for currently selected student"""
        sel = self.student_table.get_selected_item()
        if not sel:
            error("Select", "Select a student first")
            return
        # FeeInvoice expects (master, student_id)
        FeeInvoice(self, sel["id"])
