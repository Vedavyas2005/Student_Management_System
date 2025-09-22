import customtkinter as ctk
from gui.login_window import LoginWindow
from config.settings import THEME

# default customtkinter settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

if __name__ == "__main__":
    LoginWindow().mainloop()
