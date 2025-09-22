import customtkinter as ctk
from data.database import get_db
from gui.common.dialogs import info, error

db = get_db()

class FacultyPaymentForm(ctk.CTkToplevel):
    def __init__(self, master, faculty_id, on_success=None):
        super().__init__(master)
        self.title("Faculty Salary Payment")
        self.geometry("400x250")
        self.faculty_id = faculty_id
        self.on_success = on_success
        self._build()

    def _build(self):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.amount = ctk.CTkEntry(frame, placeholder_text="Payment Amount")
        self.amount.pack(pady=6, fill="x")

        pay_btn = ctk.CTkButton(frame, text="Pay", command=self._pay)
        pay_btn.pack(pady=10)

    def _pay(self):
        amt = self.amount.get().strip()
        try:
            amt = float(amt)
        except ValueError:
            error("Validation", "Enter a valid amount")
            return

        faculty = db.fetchone("SELECT salary, salary_pending FROM faculty WHERE id=?", (self.faculty_id,))
        if not faculty:
            error("Error", "Faculty not found")
            return

        if amt <= 0:
            error("Validation", "Amount must be positive")
            return

        if amt > faculty["salary_pending"]:
            error("Validation", "Amount exceeds pending salary")
            return

        # Insert into payments
        db.execute(
            "INSERT INTO faculty_salary_payments (faculty_id, amount) VALUES (?, ?)",
            (self.faculty_id, amt)
        )

        # Update pending salary
        db.execute(
            "UPDATE faculty SET salary_pending = salary_pending - ? WHERE id=?",
            (amt, self.faculty_id)
        )

        info("Success", f"Paid {amt} successfully")

        if self.on_success:
            self.on_success()

        self.destroy()
