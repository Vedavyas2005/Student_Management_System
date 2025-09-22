from core.student import add_student, get_all_students

def test_add_student_minimal():
    cur = add_student({
        "roll_no": "T-001",
        "first_name": "Tester",
        "last_name": "One",
        "email": "t1@example.com",
        "department": "CSE",
        "batch": 2025,
        "gpa": 8.2
    })
    assert cur is not None
    students = get_all_students()
    assert any(s.roll_no == "T-001" for s in students)
