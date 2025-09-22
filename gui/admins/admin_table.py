import customtkinter as ctk
from tkinter import ttk
from data.database import get_db
from gui.common.dialogs import info, error, confirm

db = get_db()

class AdminTable(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self._build()
        self.refresh()

    def _build(self):
        controls = ctk.CTkFrame(self, fg_color="transparent")
        controls.pack(fill="x", pady=6)
        ctk.CTkButton(controls, text="Refresh", command=self.refresh).pack(side="left", padx=6)
        ctk.CTkButton(controls, text="Delete", command=self.delete_admin).pack(side="left", padx=6)

        self.tree = ttk.Treeview(self, columns=("id","username","name","email"), show="headings")
        for col in ("id","username","name","email"):
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=140, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=8, pady=8)

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        rows = db.fetchall("""
            SELECT u.id, u.username, u.full_name, u.email
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE r.name = 'admin'
            ORDER BY u.id DESC
        """)
        for r in rows:
            self.tree.insert("", "end", values=(r["id"], r["username"], r["full_name"], r["email"]))

    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        item = self.tree.item(sel[0])["values"]
        return {"id": item[0]}

    def delete_admin(self):
        sel = self.get_selected()
        if not sel:
            error("Select", "Select an admin to delete")
            return
        if not confirm("Confirm", "Delete admin and related records?"):
            return

        db.execute("DELETE FROM users WHERE id=?", (sel["id"],))
        info("Deleted", "Admin user deleted")
        self.refresh()
