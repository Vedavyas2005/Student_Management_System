from tkinter import filedialog
import csv

def ask_save_csv(default_name="export.csv"):
    return filedialog.asksaveasfilename(defaultextension=".csv", initialfile=default_name,
                                        filetypes=[("CSV files", "*.csv")])

def write_csv(filepath: str, rows: list, headers: list):
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
