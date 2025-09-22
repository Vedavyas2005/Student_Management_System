import customtkinter as ctk
from data.database import get_db
from gui.common.dialogs import info, error
import datetime

db = get_db()

class FeePaymentForm(ctk.CTkToplevel):
    def __init__(self, parent, fee_id, on_success=None):
        super().__init__(parent)
        from gui.common.theme_manager import theme_manager
        theme_manager.apply(self)

        self.title("Mark Fee as Paid")
        self.geometry("400x220")
        self.resizable(False, False)

        self.transient(parent)
        self.lift()
        self.focus_force()

        self.fee_id = fee_id
        self.on_success = on_success

        frame = ctk.CTkFrame(self, corner_radius=10)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        ctk.CTkLabel(frame, text="Confirm Payment", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(6, 10))

        self.date_entry = ctk.CTkEntry(frame, placeholder_text="Paid On (YYYY-MM-DD)")
        self.date_entry.insert(0, datetime.date.today().isoformat())  # default today
        self.date_entry.pack(pady=6, fill="x")

        btns = ctk.CTkFrame(frame, fg_color="transparent")
        btns.pack(fill="x", pady=10)
        ctk.CTkButton(btns, text="Confirm", command=self._mark_paid, width=100).pack(side="left", padx=6)
        ctk.CTkButton(btns, text="Cancel", command=self.destroy, width=100).pack(side="left", padx=6)

    def _mark_paid(self):
        date_val = self.date_entry.get().strip()
        if not date_val:
            error("Validation", "Please enter a date")
            return

        try:
            db.execute("UPDATE fees SET paid=1, paid_on=? WHERE id=?", (date_val, self.fee_id))
            info("Success", "Fee marked as paid")
            if self.on_success:
                try:
                    self.on_success()
                except Exception:
                    pass
            self.destroy()
        except Exception as e:
            error("Error", f"Failed to mark fee: {e}")
