from tkinter import filedialog
from utils.exporter import export_students_to_csv
from gui.common.dialogs import info

def export_students_ui(parent):
    path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV","*.csv")], initialfile="students.csv")
    if not path:
        return
    export_students_to_csv(path)
    info("Export", f"Exported students to {path}")
