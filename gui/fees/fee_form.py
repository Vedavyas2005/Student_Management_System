import customtkinter as ctk
from data.database import get_db
from gui.common.dialogs import info, error

db = get_db()

class FeeForm(ctk.CTkToplevel):
    def __init__(self, parent, on_success=None):
        super().__init__(parent)
        from gui.common.theme_manager import theme_manager
        theme_manager.apply(self)

        self.title("Add Fee")
        self.geometry("400x300")
        self.resizable(False, False)

        # keep on top of parent
        self.transient(parent)
        self.lift()
        self.focus_force()

        self.on_success = on_success

        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(frame, text="Add Fee Record", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(6, 10))

        self.student_id = ctk.CTkEntry(frame, placeholder_text="Student ID")
        self.student_id.pack(pady=6, fill="x")
        self.amount = ctk.CTkEntry(frame, placeholder_text="Amount")
        self.amount.pack(pady=6, fill="x")
        self.due_date = ctk.CTkEntry(frame, placeholder_text="Due Date (YYYY-MM-DD)")
        self.due_date.pack(pady=6, fill="x")

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Save", command=self._save, width=100).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Cancel", command=self.destroy, width=100).pack(side="left", padx=6)

    def _save(self):
        sid = self.student_id.get().strip()
        amount = self.amount.get().strip()
        due_date = self.due_date.get().strip()

        if not sid or not amount:
            error("Validation", "Student ID and Amount are required")
            return

        try:
            sid = int(sid)
        except ValueError:
            error("Validation", "Student ID must be an integer")
            return

        row = db.fetchone("SELECT id FROM students WHERE id=?", (sid,))
        if not row:
            error("Not Found", "Invalid Student ID")
            return

        try:
            amount_val = float(amount)
        except ValueError:
            error("Validation", "Amount must be numeric")
            return

        db.execute(
            "INSERT INTO fees (student_id, amount, due_date) VALUES (?, ?, ?)",
            (sid, amount_val, due_date or None)
        )
        info("Success", "Fee record added")

        if self.on_success:
            try:
                self.on_success()
            except Exception:
                pass

        self.destroy()
