"""
Student Records Management System - Enhanced CLI Application
Features: CRUD with Delete, Search, Pagination, Sorting, and More
"""

import sys
import os
from datetime import datetime
from database import DatabaseConnection
from validators import Validators
from operations import (
    StudentOperations, CourseOperations, EnrollmentOperations,
    GradeOperations, AttendanceOperations, ReportOperations
)
from report_generator import ReportGenerator


class PaginationManager:
    """Handle pagination for large datasets"""
    
    def __init__(self, items, page_size=5):
        self.items = items
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = (len(items) + page_size - 1) // page_size if items else 0
    
    def get_current_page(self):
        """Get current page items"""
        if not self.items:
            return []
        start = self.current_page * self.page_size
        end = start + self.page_size
        return self.items[start:end]
    
    def has_next(self):
        """Check if next page exists"""
        return self.current_page < self.total_pages - 1
    
    def has_prev(self):
        """Check if previous page exists"""
        return self.current_page > 0
    
    def next_page(self):
        """Go to next page"""
        if self.has_next():
            self.current_page += 1
            return True
        return False
    
    def prev_page(self):
        """Go to previous page"""
        if self.has_prev():
            self.current_page -= 1
            return True
        return False
    
    def get_page_info(self):
        """Get page information"""
        if not self.items:
            return "No items"
        return f"Page {self.current_page + 1}/{self.total_pages} ({len(self.items)} total items)"


class StudentRecordsApp:
    """Enhanced CLI application with CRUD, Search, Pagination"""
    
    def __init__(self):
        """Initialize application"""
        self.running = True
        self.validate_database_connection()
    
    def validate_database_connection(self):
        """Check database connection on startup"""
        if not DatabaseConnection.test_connection():
            print("\n❌ ERROR: Cannot connect to PostgreSQL database")
            print("   Make sure PostgreSQL is running and student_records_db exists")
            sys.exit(1)
        print("\n✅ Database connection successful\n")
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print formatted header"""
        print("\n" + "="*70)
        print(f"  {title}".center(70))
        print("="*70 + "\n")
    
    def print_menu(self, title, options):
        """Print formatted menu"""
        self.print_header(title)
        for key, label in options.items():
            print(f"  {key}. {label}")
        print("\n  0. Back to Main Menu")
        print("\n" + "="*70)
    
    def get_input(self, prompt, input_type=str, allow_empty=False):
        """Get validated user input"""
        while True:
            try:
                value = input(prompt).strip()
                if not value and not allow_empty:
                    print("❌ Input cannot be empty")
                    continue
                if input_type == int:
                    return int(value) if value else None
                return value
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid {input_type.__name__}")
    
    def confirm(self, prompt):
        """Get yes/no confirmation"""
        while True:
            response = input(f"\n{prompt} (yes/no): ").strip().lower()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            print("❌ Please enter 'yes' or 'no'")
    
    def print_table(self, headers, rows, max_width=70):
        """Print formatted table"""
        if not rows:
            print("  No data to display\n")
            return
        
        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Print header
        header_row = " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print("  " + header_row)
        print("  " + "-" * (len(header_row)))
        
        # Print rows
        for row in rows:
            data_row = " | ".join(str(cell).ljust(col_widths[i]) for i, cell in enumerate(row))
            print("  " + data_row)
        print()
    
    # ========================================================================
    # STUDENT MANAGEMENT
    # ========================================================================
    
    def student_menu(self):
        """Student management menu"""
        while True:
            options = {
                '1': 'Add New Student',
                '2': 'Search Students',
                '3': 'View All Students (Paginated)',
                '4': 'View Student Details',
                '5': 'Update Student Status',
                '6': 'Delete Student',
                '7': 'Sort Students By'
            }
            self.print_menu("STUDENT MANAGEMENT", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.add_student()
            elif choice == '2':
                self.search_students()
            elif choice == '3':
                self.view_all_students_paginated()
            elif choice == '4':
                self.view_student_details()
            elif choice == '5':
                self.update_student_status()
            elif choice == '6':
                self.delete_student()
            elif choice == '7':
                self.sort_students()
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")
    
    def add_student(self):
        """Add new student"""
        self.print_header("ADD NEW STUDENT")
        
        student_number = self.get_input("  Student Number: ", int)
        if not Validators.validate_student_number(student_number):
            print("❌ Invalid student number")
            return
        
        first_name = self.get_input("  First Name: ")
        last_name = self.get_input("  Last Name: ")
        
        dob = self.get_input("  Date of Birth (YYYY-MM-DD): ")
        if not Validators.validate_date(dob):
            print("❌ Invalid date format")
            return
        
        email = self.get_input("  Email: ")
        if not Validators.validate_email(email):
            print("❌ Invalid email format")
            return
        
        success, message = StudentOperations.add_student(
            student_number, first_name, last_name, dob, email
        )
        print(f"\n{'✅' if success else '❌'} {message}")
    
    def search_students(self):
        """Search students by name or number"""
        self.print_header("SEARCH STUDENTS")
        
        search_term = self.get_input("  Search (name or student number): ")
        
        try:
            # Try as number first
            if search_term.isdigit():
                students = [StudentOperations.get_student_by_number(int(search_term))]
                students = [s for s in students if s]
            else:
                # Search by name
                all_students = StudentOperations.get_all_students()
                students = [s for s in all_students if search_term.lower() in 
                           f"{s[2]} {s[3]}".lower()]
            
            if students:
                headers = ["ID", "Num", "First Name", "Last Name", "DOB", "Email", "Status"]
                self.print_table(headers, students)
            else:
                print("  ❌ No students found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def view_all_students_paginated(self):
        """View students with pagination"""
        self.print_header("VIEW ALL STUDENTS (PAGINATED)")
        
        students = StudentOperations.get_all_students()
        if not students:
            print("  No students found\n")
            return
        
        paginator = PaginationManager(students, page_size=5)
        
        while True:
            print(f"  {paginator.get_page_info()}\n")
            
            headers = ["ID", "Num", "First Name", "Last Name", "DOB", "Email", "Status"]
            current = paginator.get_current_page()
            self.print_table(headers, current)
            
            nav_options = []
            if paginator.has_prev():
                nav_options.append("p=Previous Page")
            if paginator.has_next():
                nav_options.append("n=Next Page")
            nav_options.append("q=Quit")
            
            print("  Navigation: " + " | ".join(nav_options))
            choice = input("  Select: ").strip().lower()
            
            if choice == 'n' and paginator.has_next():
                paginator.next_page()
            elif choice == 'p' and paginator.has_prev():
                paginator.prev_page()
            elif choice == 'q':
                break
            else:
                print("  ❌ Invalid option")
            
            print()
    
    def view_student_details(self):
        """View detailed student information"""
        self.print_header("VIEW STUDENT DETAILS")
        
        student_id = self.get_input("  Student ID: ", int)
        student = StudentOperations.get_student_by_id(student_id)
        
        if not student:
            print("  ❌ Student not found\n")
            return
        
        print("  " + "-"*66)
        print(f"  Student ID:      {student[0]}")
        print(f"  Student Number:  {student[1]}")
        print(f"  Name:            {student[2]} {student[3]}")
        print(f"  Date of Birth:   {student[4]}")
        print(f"  Email:           {student[5]}")
        print(f"  Status:          {student[6]}")
        print("  " + "-"*66 + "\n")
    
    def update_student_status(self):
        """Update student status"""
        self.print_header("UPDATE STUDENT STATUS")
        
        student_id = self.get_input("  Student ID: ", int)
        student = StudentOperations.get_student_by_id(student_id)
        
        if not student:
            print("  ❌ Student not found\n")
            return
        
        print(f"\n  Current Status: {student[6]}")
        print("  New Status Options: active, inactive, graduated")
        status = self.get_input("  New Status: ").lower()
        
        if status not in ['active', 'inactive', 'graduated']:
            print("  ❌ Invalid status\n")
            return
        
        success, message = StudentOperations.update_student_status(student_id, status)
        print(f"  {'✅' if success else '❌'} {message}\n")
    
    def delete_student(self):
        """Delete a student (soft delete via status)"""
        self.print_header("DELETE STUDENT")
        
        student_id = self.get_input("  Student ID: ", int)
        student = StudentOperations.get_student_by_id(student_id)
        
        if not student:
            print("  ❌ Student not found\n")
            return
        
        print(f"\n  Student: {student[2]} {student[3]} (ID: {student[0]})")
        print("  ⚠️  WARNING: This action will mark the student as deleted")
        
        if self.confirm("  Are you absolutely sure you want to delete this student?"):
            try:
                query = f"""
                    UPDATE students
                    SET status = 'inactive'
                    WHERE student_id = {student_id}
                """
                DatabaseConnection.execute_procedure(query)
                print("\n  ✅ Student marked as deleted (status set to inactive)\n")
            except Exception as e:
                print(f"\n  ❌ Error: {e}\n")
        else:
            print("\n  ❌ Deletion cancelled\n")
    
    def sort_students(self):
        """Sort students by different criteria"""
        self.print_header("SORT STUDENTS")
        
        print("  Sort by:")
        print("  1. Student Number (Ascending)")
        print("  2. Student Number (Descending)")
        print("  3. First Name (A-Z)")
        print("  4. Last Name (A-Z)")
        
        choice = self.get_input("\n  Select sort option: ")
        
        students = StudentOperations.get_all_students()
        if not students:
            print("  No students found\n")
            return
        
        if choice == '1':
            students.sort(key=lambda x: x[1])
            title = "Students Sorted by Number (Ascending)"
        elif choice == '2':
            students.sort(key=lambda x: x[1], reverse=True)
            title = "Students Sorted by Number (Descending)"
        elif choice == '3':
            students.sort(key=lambda x: x[2])
            title = "Students Sorted by First Name"
        elif choice == '4':
            students.sort(key=lambda x: x[3])
            title = "Students Sorted by Last Name"
        else:
            print("  ❌ Invalid option\n")
            return
        
        print(f"\n  {title}\n")
        headers = ["ID", "Num", "First Name", "Last Name", "DOB", "Email", "Status"]
        self.print_table(headers, students)
    
    # ========================================================================
    # ENROLLMENT MANAGEMENT
    # ========================================================================
    
    def enrollment_menu(self):
        """Enrollment management menu"""
        while True:
            options = {
                '1': 'Add Student to Course',
                '2': 'View All Enrollments (Paginated)',
                '3': 'Search Enrollments',
                '4': 'Delete Enrollment',
                '5': 'View Course Roster'
            }
            self.print_menu("ENROLLMENT MANAGEMENT", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.add_enrollment()
            elif choice == '2':
                self.view_all_enrollments_paginated()
            elif choice == '3':
                self.search_enrollments()
            elif choice == '4':
                self.delete_enrollment()
            elif choice == '5':
                self.view_course_roster()
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")
    
    def add_enrollment(self):
        """Add enrollment"""
        self.print_header("ADD ENROLLMENT")
        
        student_id = self.get_input("  Student ID: ", int)
        if not StudentOperations.get_student_by_id(student_id):
            print("  ❌ Student not found\n")
            return
        
        course_id = self.get_input("  Course ID: ", int)
        if not CourseOperations.get_course_by_id(course_id):
            print("  ❌ Course not found\n")
            return
        
        academic_year = self.get_input("  Academic Year (e.g., 2024-2025): ")
        term = self.get_input("  Term (1 or 2): ")
        
        if term not in ['1', '2']:
            print("  ❌ Term must be 1 or 2\n")
            return
        
        success, message = EnrollmentOperations.add_enrollment(
            student_id, course_id, academic_year, term
        )
        print(f"  {'✅' if success else '❌'} {message}\n")
    
    def view_all_enrollments_paginated(self):
        """View enrollments with pagination"""
        self.print_header("VIEW ALL ENROLLMENTS (PAGINATED)")
        
        enrollments = EnrollmentOperations.get_all_enrollments()
        if not enrollments:
            print("  No enrollments found\n")
            return
        
        paginator = PaginationManager(enrollments, page_size=5)
        
        while True:
            print(f"  {paginator.get_page_info()}\n")
            
            headers = ["Enroll ID", "Student ID", "Course ID", "Year", "Term", "Date"]
            current = paginator.get_current_page()
            self.print_table(headers, current)
            
            nav_options = []
            if paginator.has_prev():
                nav_options.append("p=Previous")
            if paginator.has_next():
                nav_options.append("n=Next")
            nav_options.append("q=Quit")
            
            print("  Navigation: " + " | ".join(nav_options))
            choice = input("  Select: ").strip().lower()
            
            if choice == 'n' and paginator.has_next():
                paginator.next_page()
            elif choice == 'p' and paginator.has_prev():
                paginator.prev_page()
            elif choice == 'q':
                break
            else:
                print("  ❌ Invalid option")
            
            print()
    
    def search_enrollments(self):
        """Search enrollments by student or course"""
        self.print_header("SEARCH ENROLLMENTS")
        
        search_type = self.get_input("  Search by (1=Student ID, 2=Course ID): ")
        search_value = self.get_input("  Search value: ", int)
        
        enrollments = EnrollmentOperations.get_all_enrollments()
        if search_type == '1':
            results = [e for e in enrollments if e[1] == search_value]
        elif search_type == '2':
            results = [e for e in enrollments if e[2] == search_value]
        else:
            print("  ❌ Invalid search type\n")
            return
        
        if results:
            headers = ["Enroll ID", "Student ID", "Course ID", "Year", "Term", "Date"]
            self.print_table(headers, results)
        else:
            print("  ❌ No enrollments found\n")
    
    def delete_enrollment(self):
        """Delete enrollment"""
        self.print_header("DELETE ENROLLMENT")
        
        enrollment_id = self.get_input("  Enrollment ID: ", int)
        enrollment = EnrollmentOperations.get_enrollment_by_id(enrollment_id)
        
        if not enrollment:
            print("  ❌ Enrollment not found\n")
            return
        
        print(f"\n  Enrollment: Student {enrollment[1]} in Course {enrollment[2]}")
        
        if self.confirm("  Are you sure you want to delete this enrollment?"):
            try:
                query = f"DELETE FROM enrollments WHERE enrollment_id = {enrollment_id}"
                DatabaseConnection.execute_procedure(query)
                print("\n  ✅ Enrollment deleted\n")
            except Exception as e:
                print(f"\n  ❌ Error: {e}\n")
        else:
            print("\n  ❌ Deletion cancelled\n")
    
    def view_course_roster(self):
        """View course roster from view"""
        self.print_header("VIEW COURSE ROSTER")
        
        try:
            roster = DatabaseConnection.execute_query("SELECT * FROM vw_course_rosters LIMIT 10;")
            if roster:
                headers = ["Course Code", "Course Name", "Student Num", "First Name", "Last Name", 
                          "Year", "Term", "Total Classes", "Attended"]
                self.print_table(headers, roster)
            else:
                print("  No roster data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    # ========================================================================
    # GRADES & ATTENDANCE
    # ========================================================================
    
    def grades_attendance_menu(self):
        """Grades and attendance menu"""
        while True:
            options = {
                '1': 'Add Grade',
                '2': 'View Grades (Paginated)',
                '3': 'Search Grades',
                '4': 'Delete Grade',
                '5': 'Mark Attendance',
                '6': 'View Attendance Report'
            }
            self.print_menu("GRADES & ATTENDANCE", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.add_grade()
            elif choice == '2':
                self.view_grades_paginated()
            elif choice == '3':
                self.search_grades()
            elif choice == '4':
                self.delete_grade()
            elif choice == '5':
                self.mark_attendance()
            elif choice == '6':
                self.view_attendance_report()
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")
    
    def add_grade(self):
        """Add grade"""
        self.print_header("ADD GRADE")
        
        enrollment_id = self.get_input("  Enrollment ID: ", int)
        if not EnrollmentOperations.get_enrollment_by_id(enrollment_id):
            print("  ❌ Enrollment not found\n")
            return
        
        print("  Grade Type: test, assignment, exam")
        grade_type = self.get_input("  Grade Type: ").lower()
        grade_value = self.get_input("  Grade Value (0-100): ", int)
        
        if not Validators.validate_grade(grade_value):
            print("  ❌ Grade must be between 0 and 100\n")
            return
        
        success, message = GradeOperations.add_grade(
            enrollment_id, grade_type, grade_value
        )
        print(f"  {'✅' if success else '❌'} {message}\n")
    
    def view_grades_paginated(self):
        """View grades with pagination"""
        self.print_header("VIEW ALL GRADES (PAGINATED)")
        
        grades = GradeOperations.get_all_grades()
        if not grades:
            print("  No grades found\n")
            return
        
        paginator = PaginationManager(grades, page_size=5)
        
        while True:
            print(f"  {paginator.get_page_info()}\n")
            
            headers = ["Grade ID", "Enroll ID", "Type", "Value", "Date"]
            current = paginator.get_current_page()
            self.print_table(headers, current)
            
            nav_options = []
            if paginator.has_prev():
                nav_options.append("p=Previous")
            if paginator.has_next():
                nav_options.append("n=Next")
            nav_options.append("q=Quit")
            
            print("  Navigation: " + " | ".join(nav_options))
            choice = input("  Select: ").strip().lower()
            
            if choice == 'n' and paginator.has_next():
                paginator.next_page()
            elif choice == 'p' and paginator.has_prev():
                paginator.prev_page()
            elif choice == 'q':
                break
            else:
                print("  ❌ Invalid option")
            
            print()
    
    def search_grades(self):
        """Search grades"""
        self.print_header("SEARCH GRADES")
        
        enrollment_id = self.get_input("  Enrollment ID: ", int)
        grades = [g for g in GradeOperations.get_all_grades() if g[1] == enrollment_id]
        
        if grades:
            headers = ["Grade ID", "Enroll ID", "Type", "Value", "Date"]
            self.print_table(headers, grades)
        else:
            print("  ❌ No grades found\n")
    
    def delete_grade(self):
        """Delete grade"""
        self.print_header("DELETE GRADE")
        
        grade_id = self.get_input("  Grade ID: ", int)
        grade = GradeOperations.get_grade_by_id(grade_id)
        
        if not grade:
            print("  ❌ Grade not found\n")
            return
        
        print(f"\n  Grade: Type '{grade[2]}' with value {grade[3]}")
        
        if self.confirm("  Are you sure you want to delete this grade?"):
            try:
                query = f"DELETE FROM grades WHERE grades_id = {grade_id}"
                DatabaseConnection.execute_procedure(query)
                print("\n  ✅ Grade deleted\n")
            except Exception as e:
                print(f"\n  ❌ Error: {e}\n")
        else:
            print("\n  ❌ Deletion cancelled\n")
    
    def mark_attendance(self):
        """Mark attendance"""
        self.print_header("MARK ATTENDANCE")
        
        enrollment_id = self.get_input("  Enrollment ID: ", int)
        if not EnrollmentOperations.get_enrollment_by_id(enrollment_id):
            print("  ❌ Enrollment not found\n")
            return
        
        print("  Status: present, absent, late")
        status = self.get_input("  Attendance Status: ").lower()
        
        success, message = AttendanceOperations.mark_attendance(
            enrollment_id, status
        )
        print(f"  {'✅' if success else '❌'} {message}\n")
    
    def view_attendance_report(self):
        """View attendance report from view"""
        self.print_header("VIEW ATTENDANCE REPORT")
        
        try:
            report = DatabaseConnection.execute_query("SELECT * FROM vw_attendance_reports LIMIT 10;")
            if report:
                headers = ["Student Num", "First Name", "Last Name", "Course Code", "Course Name", 
                          "Year", "Total", "Present", "Absent"]
                self.print_table(headers, report)
            else:
                print("  No attendance data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    # ========================================================================
    # REPORTS
    # ========================================================================
    
    def reports_menu(self):
        """Reports menu"""
        while True:
            options = {
                '1': 'Student Transcript (View)',
                '2': 'Course Grade Statistics',
                '3': 'Enrollment Statistics',
                '4': 'Top Students by GPA',
                '5': 'Low Attendance Report',
                '6': 'Export All Reports to CSV',
                '7': 'Student Transcript as PDF ⭐',
                '8': 'Course Statistics as PDF ⭐',
                '9': 'Top Students as PDF ⭐'
            }
            self.print_menu("REPORTS", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.report_transcript()
            elif choice == '2':
                self.report_course_stats()
            elif choice == '3':
                self.report_enrollment_stats()
            elif choice == '4':
                self.report_top_students()
            elif choice == '5':
                self.report_low_attendance()
            elif choice == '6':
                self.export_all_reports()
            elif choice == '7':
                self.export_transcript_pdf()
            elif choice == '8':
                self.export_course_stats_pdf()
            elif choice == '9':
                self.export_top_students_pdf()
            else:
                print("❌ Invalid option")
            
            input("\nPress Enter to continue...")
    
    def report_transcript(self):
        """Student transcript report"""
        self.print_header("STUDENT TRANSCRIPT REPORT")
        
        student_id = self.get_input("  Student ID: ", int)
        
        try:
            query = f"SELECT * FROM vw_student_transcripts WHERE student_id = {student_id};"
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Student ID", "Num", "First", "Last", "Course", "Name", "Year", "Term", "Avg Grade"]
                self.print_table(headers, result)
            else:
                print("  ❌ No transcript data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_course_stats(self):
        """Course grade statistics"""
        self.print_header("COURSE GRADE STATISTICS")
        
        try:
            # Simplified query since procedures might not be available
            query = """
                SELECT 
                    c.course_code,
                    c.course_name,
                    COUNT(DISTINCT e.student_id) AS total_students,
                    COUNT(g.grades_id) AS total_grades,
                    ROUND(AVG(g.grade_value)::NUMERIC, 2) AS avg_grade
                FROM courses c
                LEFT JOIN enrollments e ON c.course_id = e.course_id
                LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
                WHERE c.status = 'active'
                GROUP BY c.course_id, c.course_code, c.course_name
                ORDER BY c.course_code;
            """
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Code", "Name", "Students", "Grades", "Avg Grade"]
                self.print_table(headers, result)
            else:
                print("  ❌ No data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_enrollment_stats(self):
        """Enrollment statistics"""
        self.print_header("ENROLLMENT STATISTICS")
        
        try:
            query = """
                SELECT 
                    c.course_code,
                    c.course_name,
                    COUNT(e.enrollment_id) AS total_enrollments,
                    COUNT(DISTINCT e.student_id) AS unique_students
                FROM courses c
                LEFT JOIN enrollments e ON c.course_id = e.course_id
                WHERE c.status = 'active'
                GROUP BY c.course_id, c.course_code, c.course_name
                ORDER BY c.course_code;
            """
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Code", "Name", "Total Enrollments", "Unique Students"]
                self.print_table(headers, result)
            else:
                print("  ❌ No data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_top_students(self):
        """Top students by GPA"""
        self.print_header("TOP STUDENTS BY GPA")
        
        try:
            query = """
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY AVG(g.grade_value) DESC) AS rank,
                    s.student_number,
                    s.first_name,
                    s.last_name,
                    ROUND(AVG(g.grade_value)::NUMERIC, 2) AS gpa,
                    COUNT(g.grades_id) AS total_grades
                FROM students s
                LEFT JOIN enrollments e ON s.student_id = e.student_id
                LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
                WHERE s.status = 'active' AND g.grades_id IS NOT NULL
                GROUP BY s.student_id, s.student_number, s.first_name, s.last_name
                ORDER BY gpa DESC
                LIMIT 10;
            """
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Rank", "Num", "First", "Last", "GPA", "Total Grades"]
                self.print_table(headers, result)
            else:
                print("  ❌ No data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_low_attendance(self):
        """Low attendance report"""
        self.print_header("LOW ATTENDANCE REPORT (<75%)")
        
        try:
            query = """
                SELECT 
                    s.student_number,
                    s.first_name,
                    s.last_name,
                    c.course_code,
                    COUNT(a.attendance_id) AS total_classes,
                    SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS classes_present,
                    ROUND((SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END)::NUMERIC / 
                           COUNT(a.attendance_id) * 100), 2) AS attendance_pct
                FROM students s
                JOIN enrollments e ON s.student_id = e.student_id
                JOIN courses c ON e.course_id = c.course_id
                LEFT JOIN attendance a ON e.enrollment_id = a.enrollment_id
                WHERE s.status = 'active'
                GROUP BY s.student_id, s.student_number, s.first_name, s.last_name, c.course_code
                HAVING COUNT(a.attendance_id) > 0 AND 
                       (SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END)::NUMERIC / 
                        COUNT(a.attendance_id) * 100) < 75
                ORDER BY attendance_pct ASC;
            """
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Num", "First", "Last", "Course", "Total", "Present", "% Attendance"]
                self.print_table(headers, result)
            else:
                print("  No low attendance students found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def export_all_reports(self):
        """Export all reports to CSV"""
        self.print_header("EXPORT ALL REPORTS")
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ReportGenerator.generate_all_reports(timestamp)
            print(f"  ✅ Reports exported to reports/ directory\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def export_transcript_pdf(self):
        """Export student transcript as PDF"""
        self.print_header("EXPORT STUDENT TRANSCRIPT AS PDF")
        
        student_id = self.get_input("  Student ID: ", int)
        
        try:
            success, message = ReportGenerator.generate_student_transcript_pdf(student_id)
            print(f"  {'✅' if success else '❌'} {message}\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def export_course_stats_pdf(self):
        """Export course statistics as PDF"""
        self.print_header("EXPORT COURSE STATISTICS AS PDF")
        
        try:
            success, message = ReportGenerator.generate_course_statistics_pdf()
            print(f"  {'✅' if success else '❌'} {message}\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def export_top_students_pdf(self):
        """Export top students as PDF"""
        self.print_header("EXPORT TOP STUDENTS AS PDF")
        
        limit = self.get_input("  Number of top students (default 10): ", int) or 10
        
        try:
            success, message = ReportGenerator.generate_top_students_pdf(limit)
            print(f"  {'✅' if success else '❌'} {message}\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    # ========================================================================
    # MAIN MENU
    # ========================================================================
    
    def main_menu(self):
        """Main menu"""
        while self.running:
            self.print_header("STUDENT RECORDS MANAGEMENT SYSTEM (Enhanced)")
            print("  1. Student Management")
            print("  2. Enrollment Management")
            print("  3. Grades & Attendance")
            print("  4. Reports")
            print("  5. Help")
            print("  0. Exit")
            print("\n" + "="*70)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                print("\n  👋 Thank you for using Student Records System. Goodbye!\n")
                self.running = False
            elif choice == '1':
                self.student_menu()
            elif choice == '2':
                self.enrollment_menu()
            elif choice == '3':
                self.grades_attendance_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                self.show_help()
            else:
                print("  ❌ Invalid option")
            
            input("\nPress Enter to continue...")
    
    def show_help(self):
        """Show help information"""
        self.print_header("HELP & FEATURES")
        
        help_text = """
  🎯 FEATURES:
  
  ✅ STUDENT MANAGEMENT
     • Add, Search, View (paginated), Sort, Update, Delete
     • Search by name or student number
     • Pagination for large datasets
     
  ✅ ENROLLMENT MANAGEMENT
     • Add, View (paginated), Search, Delete enrollments
     • View course rosters from database views
     
  ✅ GRADES & ATTENDANCE
     • Add, View (paginated), Search, Delete grades
     • Mark attendance with status (present/absent/late)
     • View attendance reports with statistics
     
  ✅ REPORTS
     • Student Transcripts (from vw_student_transcripts view)
     • Course Grade Statistics (aggregated data)
     • Enrollment Statistics
     • Top Students by GPA (ranked)
     • Low Attendance Report (< 75%)
     • Export all reports to CSV
  
  🔒 SAFETY FEATURES
     • Confirmation prompts for all deletions
     • Input validation for all fields
     • Graceful error handling
  
  📄 NAVIGATION
     • Page navigation: [n] Next | [p] Previous | [q] Quit
     • All menus support 0 to go back
     • Press Enter to continue after actions
        """
        print(help_text)


def main():
    """Main entry point"""
    app = StudentRecordsApp()
    app.main_menu()


if __name__ == "__main__":
    main()
