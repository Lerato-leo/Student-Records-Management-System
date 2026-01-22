#!/usr/bin/env python3
"""Debug script to check database views and data"""
import sys
sys.path.insert(0, 'python')
from database import DatabaseConnection

db = DatabaseConnection()

print("=" * 70)
print("CHECKING DATABASE STATE")
print("=" * 70)

# Check if data exists
print("\n[1] Student data:")
try:
    students = db.execute_query("SELECT COUNT(*) as count FROM students;")
    print(f"    Total students: {students}")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n[2] Enrollment data:")
try:
    enrollments = db.execute_query("SELECT COUNT(*) as count FROM enrollments;")
    print(f"    Total enrollments: {enrollments}")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n[3] Grades data:")
try:
    grades = db.execute_query("SELECT COUNT(*) as count FROM grades;")
    print(f"    Total grades: {grades}")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n[4] View vw_student_transcripts:")
try:
    view_data = db.execute_query("SELECT * FROM vw_student_transcripts LIMIT 3;")
    print(f"    Sample rows: {view_data}")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n[5] Raw query for student 1:")
try:
    raw = db.execute_query("""
    SELECT e.student_id, s.name, c.course_name, g.grade 
    FROM enrollments e
    JOIN students s ON e.student_id = s.id
    JOIN courses c ON e.course_id = c.id
    LEFT JOIN grades g ON e.id = g.enrollment_id
    WHERE e.student_id = 1
    LIMIT 5;
    """)
    print(f"    Results: {raw}")
except Exception as e:
    print(f"    ERROR: {e}")

print("\n" + "=" * 70)
