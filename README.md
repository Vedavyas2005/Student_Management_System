# Student_Management_System

A modern Student Management System built entirely in Python using Tkinter — but with a twist. Instead of the classic, old-school Tkinter look, we used CustomTkinter, an extended version of Tkinter that brings in modern UI components, theme toggling (light/dark), and a cleaner design.

This project was designed to be:

Modular & Scalable → follows a clean folder structure with separate modules for students, faculty, admins, and fees.

Role-Based → supports SuperAdmin, Admin, Faculty, and Student logins, each with their own dashboards and permissions.

Feature-Rich → from attendance and grades to fees with live pending-balance calculations.

Database-Driven → backed by SQLite with proper relational design.

User-Friendly → clean UI, theme toggle, CSV exports, and dynamic summaries for fees.

In short: classic Tkinter power with modern CustomTkinter looks 🚀

## ✨ Features

- 🔑 **Role-Based Access**
  - **Super Admin** → manages admins and overall system
  - **Admin** → manages students, faculty, and fees
  - **Faculty** → manages student attendance and grades
  - **Students** → view their attendance, grades, and fees
- 🗂️ **Student & Faculty Management** → add, edit, delete with linked user accounts
- 💸 **Fee Management**
  - Add new fees per student
  - Mark fees as paid
  - Live summary: **Total | Paid | Pending**
- 📊 **Attendance & Grades** → managed by faculty
- 🌓 **Light/Dark Theme Toggle** → modern UI that adapts
- 📤 **CSV Export** → export student records and fee data
- 🛢️ **SQLite Database** → lightweight and portable, included with project

---

## 🛠️ Tech Stack

- **Python 3.10+ (works with Python 3.13)**
- **CustomTkinter** (extension of Tkinter for modern GUI)
- **SQLite** (database)
- Standard libraries: `hashlib`, `datetime`, etc.

---

## 🚀 How to Run

1. **Clone the repo**  
   ```bash
   git clone https://github.com/your-username/student-management-system.git
   cd student-management-system
2. Install dependencies
   ```bash
   pip install -r requirements.txt
3. Run the app/project
   ```bash
   python main.py
4. First-time setup

On first launch, the system will prompt to create a SuperAdmin account.

## Demo Video in Sample Test Video Folder

Use this account to add Admins.

Admins can then add Students and Faculty.
