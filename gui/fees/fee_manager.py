import customtkinter as ctk
from data.database import get_db
from gui.common.dialogs import info, error
from datetime import date

db = get_db()

class FeeManager(ctk.CTkToplevel):
    """
    Manage student fees: view, add, update.
    """
    def __init__(self, master):
        super().__init__(master)
        self.title("Fee Manager")
        self.geometry("700x500")
        self._build()
        self.refresh()

    def _build(self):
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=8, pady=8)

        self.student_id_entry = ctk.CTkEntry(top_frame, placeholder_text="Student ID")
        self.student_id_entry.pack(side="left", padx=4)

        self.amount_entry = ctk.CTkEntry(top_frame, placeholder_text="Amount")
        self.amount_entry.pack(side="left", padx=4)

        self.due_date_entry = ctk.CTkEntry(top_frame, placeholder_text="Due Date (YYYY-MM-DD)")
        self.due_date_entry.pack(side="left", padx=4)

        add_btn = ctk.CTkButton(top_frame, text="Add Fee", command=self.add_fee)
        add_btn.pack(side="left", padx=6)

        mark_paid_btn = ctk.CTkButton(top_frame, text="Mark Paid", command=self.mark_paid)
        mark_paid_btn.pack(side="left", padx=6)

        # table
        self.table = ctk.CTkTextbox(self, width=680, height=360)
        self.table.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh(self):
        rows = db.fetchall("""
            SELECT f.id, f.student_id, f.amount, f.due_date, f.paid, f.paid_on
            FROM fees f ORDER BY f.id DESC
        """)
        self.table.delete("1.0", "end")
        for r in rows:
            self.table.insert("end", f"ID:{r['id']} | Student:{r['student_id']} | Amount:{r['amount']} | "
                                     f"Due:{r['due_date']} | Paid:{r['paid']} | Paid On:{r['paid_on']}\n")

    def add_fee(self):
        sid = self.student_id_entry.get().strip()
        amt = self.amount_entry.get().strip()
        due = self.due_date_entry.get().strip()

        if not (sid and amt):
            error("Missing", "Student ID and Amount required")
            return
        try:
            amt = float(amt)
        except:
            error("Invalid", "Amount must be number")
            return
        try:
            db.execute("INSERT INTO fees (student_id, amount, due_date) VALUES (?, ?, ?)",
                       (sid, amt, due or None))
            info("Added", "Fee record added")
            self.refresh()
        except Exception as e:
            error("DB Error", str(e))

    def mark_paid(self):
        try:
            text = self.table.get("sel.first", "sel.last")
            if not text:
                error("Select", "Select a row ID from table text")
                return
            fid = text.split("|")[0].split(":")[1].strip()
            db.execute("UPDATE fees SET paid=1, paid_on=? WHERE id=?", (date.today(), fid))
            info("Updated", "Marked as paid")
            self.refresh()
        except Exception as e:
            error("Error", str(e))
