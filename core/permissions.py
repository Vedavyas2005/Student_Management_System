PERMISSIONS = {
    "superadmin": {"manage_users", "view_logs", "all"},
    "admin": {"manage_students", "manage_fees", "export_data"},
    "faculty": {"mark_attendance", "manage_grades", "view_class"},
    "student": {"view_own"},
}

def has_permission(user, permission: str) -> bool:
    if user.role_name == "superadmin":
        return True
    return permission in PERMISSIONS.get(user.role_name, set())
