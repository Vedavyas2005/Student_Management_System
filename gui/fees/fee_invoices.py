import customtkinter as ctk
from tkinter import ttk
from data.database import get_db
from gui.common.dialogs import info, error, confirm
from datetime import date

db = get_db()

class FeeInvoice(ctk.CTkToplevel):
    """
    Displays and manages all fees for a specific student.
    Admin can:
      - View all fee records
      - Add a new fee
      - Mark existing fees as paid
      - See summary: Total / Paid / Pending
    """
    def __init__(self, master, student_id: int):
        super().__init__(master)
        self.student_id = student_id
        self.title(f"Fees - Student {student_id}")
        self.geometry("750x520")
        self._build()
        self.refresh()

    def _build(self):
        # --- controls frame ---
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", pady=6, padx=8)

        self.amount_entry = ctk.CTkEntry(controls, placeholder_text="Amount")
        self.amount_entry.pack(side="left", padx=4)

        self.due_date_entry = ctk.CTkEntry(controls, placeholder_text="Due Date (YYYY-MM-DD)")
        self.due_date_entry.pack(side="left", padx=4)

        add_btn = ctk.CTkButton(controls, text="Add Fee", command=self.add_fee, width=100)
        add_btn.pack(side="left", padx=6)

        self.mark_btn = ctk.CTkButton(controls, text="Mark as Paid", command=self.mark_paid, width=120)
        self.mark_btn.pack(side="left", padx=6)

        self.refresh_btn = ctk.CTkButton(controls, text="Refresh", command=self.refresh, width=100)
        self.refresh_btn.pack(side="left", padx=6)

        # --- summary label ---
        self.summary_lbl = ctk.CTkLabel(self, text="Total: 0 | Paid: 0 | Pending: 0",
                                        font=ctk.CTkFont(size=13, weight="bold"))
        self.summary_lbl.pack(pady=(2,6))

        # --- table ---
        self.tree = ttk.Treeview(
            self,
            columns=("id", "amount", "due", "paid", "paid_on"),
            show="headings"
        )
        for col in ("id", "amount", "due", "paid", "paid_on"):
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh(self):
        # clear table
        for i in self.tree.get_children():
            self.tree.delete(i)

        # load fees
        rows = db.fetchall("""
            SELECT id, amount, due_date, paid, paid_on
            FROM fees WHERE student_id=? ORDER BY id DESC
        """, (self.student_id,))
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["amount"], r["due_date"], r["paid"], r["paid_on"]))

        # update summary
        summary = db.fetchone("""
            SELECT 
                SUM(amount) as total_fee,
                SUM(CASE WHEN paid=1 THEN amount ELSE 0 END) as total_paid,
                SUM(CASE WHEN paid=0 THEN amount ELSE 0 END) as pending_fee
            FROM fees WHERE student_id=?
        """, (self.student_id,))
        if summary:
            self.summary_lbl.configure(
                text=f"Total: {summary['total_fee'] or 0} | Paid: {summary['total_paid'] or 0} | Pending: {summary['pending_fee'] or 0}"
            )

    def get_selected_fee(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item = self.tree.item(sel[0])["values"]
        return {"id": item[0], "amount": item[1], "paid": item[3]}

    def add_fee(self):
        amt = self.amount_entry.get().strip()
        due = self.due_date_entry.get().strip()

        if not amt:
            error("Validation", "Amount is required")
            return

        try:
            amt_val = float(amt)
        except ValueError:
            error("Validation", "Amount must be numeric")
            return

        try:
            db.execute(
                "INSERT INTO fees (student_id, amount, due_date) VALUES (?, ?, ?)",
                (self.student_id, amt_val, due or None)
            )
            info("Added", f"Fee of {amt_val} added")
            self.amount_entry.delete(0, "end")
            self.due_date_entry.delete(0, "end")
            self.refresh()
        except Exception as e:
            error("DB Error", str(e))

    def mark_paid(self):
        fee = self.get_selected_fee()
        if not fee:
            error("Select", "Select a fee to mark as paid")
            return
        if fee["paid"]:
            info("Already Paid", "This fee is already paid")
            return
        if not confirm("Confirm", f"Mark fee {fee['id']} as paid?"):
            return

        db.execute("UPDATE fees SET paid=1, paid_on=? WHERE id=?", (date.today(), fee["id"]))
        info("Updated", "Fee marked as paid")
        self.refresh()
