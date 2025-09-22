# USE THIS ONLY, IF AND ONLY IF, I MEAN REALLY IF NEEDED BY SOMEONE YOU KNOW, MAYBE IDK, ONLY USE THIS THEN
#AND OH, ALSO DONT FORGET TO PUT THIS THEME FOR EVERY BUTTON AND ALL IF U REALLY REALLY WANNA USE THIS

import customtkinter as ctk
from config.settings import THEME

class ThemeManager:
    def __init__(self):
        self.mode = "dark"   # default

    def apply(self, widget):
        theme = THEME[self.mode]
        try:
            widget.configure(fg_color=theme["bg"])
        except Exception:
            pass

        for child in widget.winfo_children():
            try:
                child.configure(
                    fg_color=theme.get("bg", None),
                    text_color=theme.get("fg", None)
                )
            except Exception:
                pass
            self.apply(child)

    def style_button(self, button: ctk.CTkButton):
        theme = THEME[self.mode]
        try:
            button.configure(
                fg_color=theme["button_color"],
                hover_color=theme["button_hover"],
                text_color=theme["fg"]
            )
        except Exception:
            pass

    def toggle(self, root):
        self.mode = "light" if self.mode == "dark" else "dark"
        self.apply(root)

theme_manager = ThemeManager()

