from passlib.hash import pbkdf2_sha256
from data.database import get_db
from typing import Optional
from core.user import User
import datetime

db = get_db()

def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pbkdf2_sha256.verify(password, hashed)
    except Exception:
        return False

def create_user(username: str, password: str, full_name: str, email: str, role_name: str) -> int:
    # find role id
    role_row = db.fetchone("SELECT id FROM roles WHERE name = ?", (role_name,))
    if not role_row:
        raise ValueError("Role not found")
    role_id = role_row["id"]
    password_hash = hash_password(password)
    cur = db.execute(
        "INSERT INTO users (username, password_hash, full_name, email, role_id) VALUES (?, ?, ?, ?, ?)",
        (username, password_hash, full_name, email, role_id)
    )
    user_id = cur.lastrowid
    _log(user_id, "create_user", "users", user_id, f"Created user {username} role {role_name}")
    return user_id

def get_user_by_username(username: str) -> Optional[User]:
    row = db.fetchone("SELECT u.*, r.name as role_name FROM users u JOIN roles r ON u.role_id=r.id WHERE username = ?", (username,))
    if not row:
        return None
    return User.from_row(row)

def login(username: str, password: str) -> Optional[User]:
    row = db.fetchone("SELECT u.*, r.name as role_name FROM users u JOIN roles r ON u.role_id=r.id WHERE username = ?", (username,))
    if not row:
        return None
    if verify_password(password, row["password_hash"]):
        # update last_login
        db.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.datetime.utcnow().isoformat(), row["id"]))
        user = User.from_row(row)
        _log(row["id"], "login", "users", row["id"], f"User logged in")
        return user
    return None

def change_password(user_id: int, new_password: str):
    ph = hash_password(new_password)
    db.execute("UPDATE users SET password_hash = ? WHERE id = ?", (ph, user_id))
    _log(user_id, "change_password", "users", user_id, "Password changed")

def _log(user_id, action, table, target_id, details):
    db.execute("INSERT INTO audit_logs (user_id, action, target_table, target_id, details) VALUES (?, ?, ?, ?, ?)",
               (user_id, action, table, target_id, details))
