import customtkinter as ctk
from tkinter import messagebox

def info(title, msg):
    messagebox.showinfo(title, msg)

def warn(title, msg):
    messagebox.showwarning(title, msg)

def error(title, msg):
    messagebox.showerror(title, msg)

def confirm(title, msg) -> bool:
    return messagebox.askyesno(title, msg)
