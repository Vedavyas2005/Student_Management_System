import customtkinter as ctk
from core.user import User
from core.manager import check_placement_eligible
from data.database import get_db
from tkinter import ttk
from utils.helpers import ask_save_csv

db = get_db()

class StudentDashboard(ctk.CTkFrame):
    def __init__(self, master, user: User):
        super().__init__(master)
        self.user = user
        self._build()

    def _build(self):
        header = ctk.CTkLabel(self, text="Student Dashboard", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=8, anchor="w")

        row = db.fetchone("SELECT * FROM students WHERE user_id = ?", (self.user.id,))
        if not row:
            ctk.CTkLabel(self, text="No student profile linked to your account.").pack(pady=8)
            return

        def safe(r, key):
            return r[key] if key in r.keys() else None

        profile_text = (
            f"Name: {row['first_name']} {safe(row, 'last_name') or ''}\n"
            f"Roll: {row['roll_no']}\n"
            f"Dept: {safe(row, 'department')}\n"
            f"GPA: {safe(row, 'gpa')}"
        )
        ctk.CTkLabel(self, text=profile_text).pack(pady=8)

        eligible = check_placement_eligible(row["id"])
        ctk.CTkLabel(self, text=f"Placement Eligible: {'Yes' if eligible else 'No'}").pack(pady=8)

        # Buttons
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", pady=10)

        ctk.CTkButton(controls, text="View Attendance", command=lambda: self.view_attendance(row["id"]), width=150).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="View Grades", command=lambda: self.view_grades(row["id"]), width=150).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="View Fees", command=lambda: self.view_fees(row["id"]), width=150).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Export Report (CSV)", command=lambda: self.export_report(row["id"]), width=180).pack(side="left", padx=6)

    def view_attendance(self, student_id):
        self.lift()
        win = ctk.CTkToplevel(self)
        win.title("My Attendance")
        win.geometry("600x400")
        rows = db.fetchall("SELECT date, status, subject FROM attendance WHERE student_id=? ORDER BY date DESC", (student_id,))
        tree = ttk.Treeview(win, columns=("date", "status", "subject"), show="headings")
        for c in ("date", "status", "subject"):
            tree.heading(c, text=c.title())
        tree.pack(fill="both", expand=True)
        for r in rows:
            tree.insert("", "end", values=(r["date"], r["status"], r["subject"]))

    def view_grades(self, student_id):
        self.lift()
        win = ctk.CTkToplevel(self)
        win.title("My Grades")
        win.geometry("600x400")
        rows = db.fetchall("SELECT subject, term, marks, grade FROM grades WHERE student_id=? ORDER BY created_at DESC", (student_id,))
        tree = ttk.Treeview(win, columns=("subject", "term", "marks", "grade"), show="headings")
        for c in ("subject", "term", "marks", "grade"):
            tree.heading(c, text=c.title())
        tree.pack(fill="both", expand=True)
        for r in rows:
            tree.insert("", "end", values=(r["subject"], r["term"], r["marks"], r["grade"]))

    def view_fees(self, student_id):
        self.lift()
        win = ctk.CTkToplevel(self)
        win.title("My Fees")
        win.geometry("600x400")
        rows = db.fetchall("SELECT amount, due_date, paid, paid_on FROM fees WHERE student_id=? ORDER BY due_date", (student_id,))
        tree = ttk.Treeview(win, columns=("amount", "due_date", "paid", "paid_on"), show="headings")
        for c in ("amount", "due_date", "paid", "paid_on"):
            tree.heading(c, text=c.title())
        tree.pack(fill="both", expand=True)
        for r in rows:
            tree.insert("", "end", values=(r["amount"], r["due_date"], "Yes" if r["paid"] else "No", r["paid_on"] or ""))

    def export_report(self, student_id):
        self.lift()
        path = ask_save_csv("student_report.csv")
        if not path:
            return
        rows_att = db.fetchall("SELECT date, status, subject FROM attendance WHERE student_id=?", (student_id,))
        rows_grades = db.fetchall("SELECT subject, term, marks, grade FROM grades WHERE student_id=?", (student_id,))
        rows_fees = db.fetchall("SELECT amount, due_date, paid, paid_on FROM fees WHERE student_id=?", (student_id,))

        with open(path, "w", encoding="utf-8") as f:
            # Attendance
            f.write("Attendance Records\n")
            f.write("Date,Status,Subject\n")
            for r in rows_att:
                f.write(f"{r['date']},{r['status']},{r['subject']}\n")

            # Grades
            f.write("\nGrades Records\n")
            f.write("Subject,Term,Marks,Grade\n")
            for g in rows_grades:
                f.write(f"{g['subject']},{g['term']},{g['marks']},{g['grade']}\n")

            # Fees
            f.write("\nFee Records\n")
            f.write("Amount,Due Date,Paid,Paid On\n")
            for frow in rows_fees:
                f.write(f"{frow['amount']},{frow['due_date']},{'Yes' if frow['paid'] else 'No'},{frow['paid_on'] or ''}\n")
