from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "data" / "app.db"
MIGRATIONS_SQL = BASE_DIR / "data" / "migrations.sql"

APP_TITLE = "Student Management System"
WINDOW_SIZE = "1100x700"


THEME = {
    "dark": {
        "bg": "#121212",
        "fg": "#FFFFFF",
        "button_color": "#C2185B",   # cherry red
        "button_hover": "#E91E63",   # pink
    },
    "light": {
        "bg": "#F5F9FF",
        "fg": "#000000",
        "button_color": "#2196F3",   # neon light blue
        "button_hover": "#0D47A1",   # dark blue
    }
}


# Default placement criteria
PLACEMENT_RULES = {
    "min_gpa": 6.0,
    "min_attendance_percent": 55.0
}
