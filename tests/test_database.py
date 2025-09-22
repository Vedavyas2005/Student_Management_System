from data.database import get_db

def test_db_exists():
    db = get_db()
    assert db is not None
    row = db.fetchone("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert row is not None
