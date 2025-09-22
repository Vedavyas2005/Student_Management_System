from core import auth
from data.database import get_db

def test_create_and_login_user():
    db = get_db()
    # create test user
    username = "test_user_001"
    try:
        uid = auth.create_user(username, "password123", "Test User", "test@example.com", "admin")
    except Exception:
        # if exists, fetch
        user = auth.get_user_by_username(username)
        assert user is not None
        return
    user = auth.get_user_by_username(username)
    assert user.username == username
    logged = auth.login(username, "password123")
    assert logged is not None
