import re
from typing import Tuple

EMAIL_RE = re.compile(r"[^@]+@[^@]+\.[^@]+")

def validate_email(email: str) -> bool:
    if not email:
        return False
    return bool(EMAIL_RE.match(email))

def validate_gpa(value) -> Tuple[bool, float]:
    try:
        gpa = float(value)
        if 0.0 <= gpa <= 10.0:
            return True, gpa
        return False, 0.0
    except Exception:
        return False, 0.0
