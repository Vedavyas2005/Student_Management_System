import sqlite3
from pathlib import Path
from typing import Any, List, Tuple, Optional
from config.settings import DB_PATH, MIGRATIONS_SQL
import os

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

class Database:
    def __init__(self, path: Path = DB_PATH):
        self.path = str(path)
        self.conn: Optional[sqlite3.Connection] = None
        self._connect()
        self._migrate()

    def _connect(self):
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        # enable foreign keys
        self.conn.execute("PRAGMA foreign_keys = ON;")

    def _migrate(self):
        if MIGRATIONS_SQL.exists():
            with open(MIGRATIONS_SQL, "r", encoding="utf-8") as f:
                sql = f.read()
            cur = self.conn.cursor()
            cur.executescript(sql)
            self.conn.commit()
            # Ensure base roles exist
            self._ensure_roles()

    def _ensure_roles(self):
        cur = self.conn.cursor()
        roles = ["superadmin", "admin", "faculty", "student"]
        for r in roles:
            cur.execute("INSERT OR IGNORE INTO roles (name) VALUES (?)", (r,))
        self.conn.commit()

    def execute(self, query: str, params: Tuple = ()):
        cur = self.conn.cursor()
        cur.execute(query, params)
        self.conn.commit()
        return cur

    def fetchall(self, query: str, params: Tuple = ()) -> List[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()

    def fetchone(self, query: str, params: Tuple = ()) -> Optional[sqlite3.Row]:
        cur = self.conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()

    def close(self):
        if self.conn:
            self.conn.close()

# single db instance for app
_db = Database()
def get_db() -> Database:
    return _db
