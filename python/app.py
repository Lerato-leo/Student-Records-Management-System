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
from logger import log_info, log_error, log_operation, log_debug


class PaginationManager:
    """Handle pagination for large datasets with enhanced feedback"""
    
    def __init__(self, items, page_size=5):
        self.items = items if items else []
        self.page_size = max(1, page_size)  # Ensure page_size is at least 1
        self.current_page = 0
        self.total_pages = (len(self.items) + self.page_size - 1) // self.page_size if self.items else 1
    
    def get_current_page(self):
        """Get current page items"""
        if not self.items:
            return []
        start = self.current_page * self.page_size
        end = start + self.page_size
        return self.items[start:end]
    
    def has_next(self):
        """Check if next page exists"""
        return self.current_page < self.total_pages - 1 if self.total_pages > 0 else False
    
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
    
    def jump_to_page(self, page_number):
        """Jump to specific page (1-indexed)"""
        if 1 <= page_number <= self.total_pages:
            self.current_page = page_number - 1
            return True
        return False
    
    def get_page_info(self):
        """Get detailed page information"""
        if not self.items:
            return "No items available"
        
        current_items_start = self.current_page * self.page_size + 1
        current_items_end = min((self.current_page + 1) * self.page_size, len(self.items))
        
        return (f"Page {self.current_page + 1}/{self.total_pages} | "
                f"Showing items {current_items_start}-{current_items_end} of {len(self.items)}")


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
    
    def get_input(self, prompt, input_type=str, allow_empty=False, min_val=None, max_val=None):
        """Get validated user input with enhanced error handling"""
        while True:
            try:
                value = input(prompt).strip()
                
                # Check empty input
                if not value:
                    if allow_empty:
                        return value if input_type == str else None
                    print("  ❌ Input cannot be empty. Please try again.")
                    continue
                
                # Handle different input types
                if input_type == int:
                    try:
                        num = int(value)
                        if min_val is not None and num < min_val:
                            print(f"  ❌ Value must be at least {min_val}")
                            continue
                        if max_val is not None and num > max_val:
                            print(f"  ❌ Value must be at most {max_val}")
                            continue
                        return num
                    except ValueError:
                        print("  ❌ Invalid input. Please enter a valid integer.")
                        continue
                
                elif input_type == float:
                    try:
                        num = float(value)
                        if min_val is not None and num < min_val:
                            print(f"  ❌ Value must be at least {min_val}")
                            continue
                        if max_val is not None and num > max_val:
                            print(f"  ❌ Value must be at most {max_val}")
                            continue
                        return num
                    except ValueError:
                        print("  ❌ Invalid input. Please enter a valid decimal number.")
                        continue
                
                # Return string (already stripped)
                return value
                
            except KeyboardInterrupt:
                print("\n\n  ⚠️  Operation cancelled by user")
                return None
            except Exception as e:
                log_error("Error in get_input", exception=e)
                print(f"  ❌ An unexpected error occurred: {str(e)}")
                continue
    
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
        """Add new student with comprehensive validation and logging"""
        self.print_header("ADD NEW STUDENT")
        
        try:
            # Get and validate student number
            while True:
                student_number = self.get_input("  Student Number (YYYYRR): ", int)
                if student_number is None:
                    return
                valid, msg = Validators.validate_student_number(student_number)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Get and validate first name
            while True:
                first_name = self.get_input("  First Name: ")
                if first_name is None:
                    return
                valid, msg = Validators.validate_name(first_name)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Get and validate last name
            while True:
                last_name = self.get_input("  Last Name: ")
                if last_name is None:
                    return
                valid, msg = Validators.validate_name(last_name)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Get and validate date of birth
            while True:
                dob = self.get_input("  Date of Birth (YYYY-MM-DD): ")
                if dob is None:
                    return
                valid, msg = Validators.validate_date_of_birth(dob)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Get and validate email
            while True:
                email = self.get_input("  Email: ")
                if email is None:
                    return
                valid, msg = Validators.validate_email(email)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Add student
            result = StudentOperations.add_student(
                student_number, first_name, last_name, dob, email
            )
            
            # Handle both old (2-tuple) and new (3-tuple) return formats
            if len(result) == 3:
                success, message, student_id = result
                print(f"\n{'✅' if success else '❌'} {message}")
                if success:
                    log_info(f"Student added: {first_name} {last_name} (ID: {student_id})")
            else:
                success, message = result
                print(f"\n{'✅' if success else '❌'} {message}")
                if success:
                    log_info(f"Student added: {first_name} {last_name}")
        
        except Exception as e:
            log_error("Error in add_student", exception=e)
            print(f"\n  ❌ An unexpected error occurred: {str(e)}")
    
    
    def search_students(self):
        """Search students by name or number (case-insensitive, partial match)"""
        self.print_header("SEARCH STUDENTS")
        
        try:
            search_term = self.get_input("  Search (name or student number): ")
            if search_term is None:
                return
            
            if not search_term.strip():
                print("  ❌ Search term cannot be empty\n")
                return
            
            all_students = StudentOperations.get_all_students()
            if not all_students:
                print("  ❌ No students found in database\n")
                return
            
            # Case-insensitive partial match search
            search_lower = search_term.lower()
            students = []
            
            for student in all_students:
                # Search by ID, student number, or name (case-insensitive, partial match)
                student_id, student_num, first_name, last_name, dob, email, status = student
                
                if (str(student_id).startswith(search_lower) or
                    str(student_num).startswith(search_lower) or
                    first_name.lower().startswith(search_lower) or
                    last_name.lower().startswith(search_lower) or
                    f"{first_name} {last_name}".lower().find(search_lower) != -1):
                    students.append(student)
            
            if students:
                headers = ["ID", "Num", "First Name", "Last Name", "DOB", "Email", "Status"]
                print(f"  Found {len(students)} student(s):\n")
                self.print_table(headers, students)
                log_info(f"Search completed: '{search_term}' found {len(students)} results")
            else:
                print(f"  ❌ No students found matching '{search_term}'\n")
                log_info(f"Search completed: '{search_term}' found 0 results")
        
        except Exception as e:
            log_error("Error in search_students", exception=e, context=f"search_term={search_term}")
            print(f"  ❌ Error during search: {str(e)}\n")
    
    def view_all_students_paginated(self):
        """View students with pagination and comprehensive navigation"""
        self.print_header("VIEW ALL STUDENTS (PAGINATED - NEWEST FIRST)")
        
        try:
            students = StudentOperations.get_all_students()
            if not students:
                print("  ℹ️  No students found in database\n")
                return
            
            paginator = PaginationManager(students, page_size=5)
            
            while True:
                try:
                    print(f"  📄 {paginator.get_page_info()}\n")
                    
                    headers = ["ID", "Num", "First Name", "Last Name", "DOB", "Email", "Status"]
                    current = paginator.get_current_page()
                    self.print_table(headers, current)
                    
                    # Build navigation options
                    nav_options = []
                    if paginator.has_prev():
                        nav_options.append("p=Previous")
                    if paginator.has_next():
                        nav_options.append("n=Next")
                    nav_options.append("q=Quit")
                    
                    print("  Navigation: " + " | ".join(nav_options))
                    choice = input("  Enter choice: ").strip().lower()
                    
                    if choice == 'n':
                        if paginator.has_next():
                            paginator.next_page()
                            print()
                        else:
                            print("  ⚠️  Already on last page\n")
                    elif choice == 'p':
                        if paginator.has_prev():
                            paginator.prev_page()
                            print()
                        else:
                            print("  ⚠️  Already on first page\n")
                    elif choice == 'q':
                        break
                    else:
                        print("  ❌ Invalid option. Please use p, n, or q\n")
                
                except KeyboardInterrupt:
                    print("\n\n  ⚠️  Navigation cancelled\n")
                    break
                except Exception as e:
                    log_error("Error in pagination loop", exception=e)
                    print(f"  ❌ Error: {str(e)}\n")
                    break
        
        except Exception as e:
            log_error("Error in view_all_students_paginated", exception=e)
            print(f"  ❌ Error retrieving students: {str(e)}\n")
    
    def view_student_details(self):
        """View detailed student information with error handling"""
        self.print_header("VIEW STUDENT DETAILS")
        
        try:
            student_id = self.get_input("  Enter Student ID: ", int, min_val=1)
            if student_id is None:
                return
            
            student = StudentOperations.get_student_by_id(student_id)
            
            if not student:
                print(f"  ❌ Student with ID {student_id} not found\n")
                log_info(f"Student search: ID {student_id} not found")
                return
            
            print("\n  " + "="*64)
            print(f"  Student ID:         {student[0]}")
            print(f"  Student Number:     {student[1]}")
            print(f"  Full Name:          {student[2]} {student[3]}")
            print(f"  Date of Birth:      {student[4]}")
            print(f"  Email:              {student[5]}")
            print(f"  Status:             {student[6]}")
            print("  " + "="*64 + "\n")
            log_info(f"Student details viewed: ID {student_id}")
        
        except Exception as e:
            log_error("Error in view_student_details", exception=e)
            print(f"  ❌ Error retrieving student details: {str(e)}\n")
    
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
        """Add enrollment with comprehensive validation"""
        self.print_header("ADD ENROLLMENT")
        
        try:
            # Get and validate student ID
            student_id = self.get_input("  Enter Student ID: ", int, min_val=1)
            if student_id is None:
                return
            
            student = StudentOperations.get_student_by_id(student_id)
            if not student:
                print(f"  ❌ Student with ID {student_id} not found\n")
                log_info(f"Enrollment: Student {student_id} not found")
                return
            print(f"  ✅ Student found: {student[2]} {student[3]}")
            
            # Get and validate course ID
            course_id = self.get_input("  Enter Course ID: ", int, min_val=1)
            if course_id is None:
                return
            
            course = CourseOperations.get_course_by_id(course_id)
            if not course:
                print(f"  ❌ Course with ID {course_id} not found\n")
                log_info(f"Enrollment: Course {course_id} not found")
                return
            print(f"  ✅ Course found: {course[1]}")
            
            # Get and validate academic year
            while True:
                academic_year = self.get_input("  Academic Year (YYYY-YYYY, e.g., 2024-2025): ")
                if academic_year is None:
                    return
                valid, msg = Validators.validate_academic_year(academic_year)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Get and validate term
            while True:
                term = self.get_input("  Term (1=Fall, 2=Spring): ")
                if term is None:
                    return
                valid, msg = Validators.validate_term(term)
                if valid:
                    break
                print(f"  ❌ {msg}. Please try again.")
            
            # Add enrollment
            success, message = EnrollmentOperations.add_enrollment(
                student_id, course_id, academic_year, term
            )
            print(f"\n  {'✅' if success else '❌'} {message}\n")
            if success:
                log_operation("add_enrollment", "success", f"Student {student_id}, Course {course_id}")
        
        except Exception as e:
            log_error("Error in add_enrollment", exception=e)
            print(f"\n  ❌ Error: {str(e)}\n")
    
    def view_all_enrollments_paginated(self):
        """View enrollments with pagination and navigation (newest first)"""
        self.print_header("VIEW ALL ENROLLMENTS (PAGINATED - NEWEST FIRST)")
        
        try:
            enrollments = EnrollmentOperations.get_all_enrollments()
            if not enrollments:
                print("  ℹ️  No enrollments found in database\n")
                return
            
            paginator = PaginationManager(enrollments, page_size=5)
            
            while True:
                try:
                    print(f"  📄 {paginator.get_page_info()}\n")
                    
                    headers = ["Enroll ID", "Student ID", "Course ID", "Year", "Term", "Date"]
                    current = paginator.get_current_page()
                    self.print_table(headers, current)
                    
                    # Build navigation options
                    nav_options = []
                    if paginator.has_prev():
                        nav_options.append("p=Previous")
                    if paginator.has_next():
                        nav_options.append("n=Next")
                    nav_options.append("q=Quit")
                    
                    print("  Navigation: " + " | ".join(nav_options))
                    choice = input("  Enter choice: ").strip().lower()
                    
                    if choice == 'n':
                        if paginator.has_next():
                            paginator.next_page()
                            print()
                        else:
                            print("  ⚠️  Already on last page\n")
                    elif choice == 'p':
                        if paginator.has_prev():
                            paginator.prev_page()
                            print()
                        else:
                            print("  ⚠️  Already on first page\n")
                    elif choice == 'q':
                        break
                    else:
                        print("  ❌ Invalid option. Please use p, n, or q\n")
                
                except KeyboardInterrupt:
                    print("\n\n  ⚠️  Navigation cancelled\n")
                    break
                except Exception as e:
                    log_error("Error in enrollment pagination loop", exception=e)
                    print(f"  ❌ Error: {str(e)}\n")
                    break
        
        except Exception as e:
            log_error("Error in view_all_enrollments_paginated", exception=e)
            print(f"  ❌ Error retrieving enrollments: {str(e)}\n")
    
    def search_enrollments(self):
        """Search enrollments by student or course with error handling"""
        self.print_header("SEARCH ENROLLMENTS")
        
        try:
            print("  Search by:")
            print("  1. Student ID")
            print("  2. Course ID")
            
            search_type = self.get_input("\n  Select (1 or 2): ")
            if search_type is None:
                return
            
            if search_type not in ['1', '2']:
                print("  ❌ Invalid search type. Please select 1 or 2\n")
                return
            
            search_value = self.get_input("  Enter search value: ", int, min_val=1)
            if search_value is None:
                return
            
            enrollments = EnrollmentOperations.get_all_enrollments()
            if not enrollments:
                print("  ℹ️  No enrollments found in database\n")
                return
            
            if search_type == '1':
                results = [e for e in enrollments if e[1] == search_value]
                search_label = f"Student ID {search_value}"
            else:  # search_type == '2'
                results = [e for e in enrollments if e[2] == search_value]
                search_label = f"Course ID {search_value}"
            
            if results:
                headers = ["Enroll ID", "Student ID", "Course ID", "Year", "Term", "Date"]
                print(f"\n  Found {len(results)} enrollment(s) for {search_label}:\n")
                self.print_table(headers, results)
                log_info(f"Enrollment search: {search_label} found {len(results)} results")
            else:
                print(f"  ❌ No enrollments found for {search_label}\n")
                log_info(f"Enrollment search: {search_label} found 0 results")
        
        except Exception as e:
            log_error("Error in search_enrollments", exception=e)
            print(f"  ❌ Error during search: {str(e)}\n")
    
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
                '6': 'View All Attendance (Paginated)',
                '7': 'View Attendance Report'
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
                self.view_all_attendance_paginated()
            elif choice == '7':
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
    
    def view_all_attendance_paginated(self):
        """View all attendance records with pagination (newest first)"""
        self.print_header("VIEW ALL ATTENDANCE RECORDS (PAGINATED)")
        
        attendance_records = AttendanceOperations.get_all_attendance()
        if not attendance_records:
            print("  No attendance records found\n")
            return
        
        paginator = PaginationManager(attendance_records, page_size=5)
        
        while True:
            print(f"  {paginator.get_page_info()}\n")
            
            headers = ["Attend ID", "Enroll ID", "Date", "Status"]
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
                '4': 'Top Students by Weighted GPA',
                '5': 'Student Course Results (Weighted)',
                '6': 'Student GPA Breakdown',
                '7': 'Low Attendance Report',
                '8': 'Export All Reports to CSV',
                '9': 'Student Transcript as PDF ⭐',
                '10': 'Course Statistics as PDF ⭐',
                '11': 'Top Students as PDF ⭐'
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
                self.report_top_students_weighted_gpa()
            elif choice == '5':
                self.report_course_results_weighted()
            elif choice == '6':
                self.report_student_gpa_breakdown()
            elif choice == '7':
                self.report_low_attendance()
            elif choice == '8':
                self.export_all_reports()
            elif choice == '9':
                self.export_transcript_pdf()
            elif choice == '10':
                self.export_course_stats_pdf()
            elif choice == '11':
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
    
    def report_top_students_weighted_gpa(self):
        """Top students by weighted GPA"""
        self.print_header("TOP STUDENTS BY WEIGHTED GPA")
        print("  Weights: Assignment 30% | Test 30% | Exam 40%\n")
        
        try:
            query = """
                SELECT
                    ROW_NUMBER() OVER (ORDER BY gpa DESC) AS rank,
                    student_number,
                    first_name,
                    last_name,
                    gpa
                FROM vw_student_gpa
                ORDER BY gpa DESC
                LIMIT 10;
            """
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Rank", "Student #", "First Name", "Last Name", "Weighted GPA"]
                self.print_table(headers, result)
            else:
                print("  ❌ No data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_course_results_weighted(self):
        """View course results with weighted averages"""
        self.print_header("STUDENT COURSE RESULTS (WEIGHTED)")
        print("  Weights: Assignment 30% | Test 30% | Exam 40%\n")
        
        try:
            query = """
                SELECT 
                    student_number,
                    first_name,
                    last_name,
                    course_code,
                    course_name,
                    academic_year,
                    term,
                    final_average
                FROM vw_student_course_results
                ORDER BY student_number, course_code;
            """
            result = DatabaseConnection.execute_query(query)
            
            if result:
                headers = ["Num", "First", "Last", "Code", "Course", "Year", "Term", "Final Avg"]
                self.print_table(headers, result)
            else:
                print("  ❌ No data found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_student_gpa_breakdown(self):
        """View student GPA with course breakdown"""
        self.print_header("STUDENT GPA BREAKDOWN")
        print("  Weights: Assignment 30% | Test 30% | Exam 40%\n")
        
        student_id = self.get_input("  Enter Student ID: ", int)
        
        try:
            # Get student GPA
            gpa_query = f"SELECT * FROM vw_student_gpa WHERE student_id = {student_id};"
            gpa_result = DatabaseConnection.execute_query(gpa_query)
            
            if gpa_result:
                print(f"\n  Student: {gpa_result[0][1]} ({gpa_result[0][2]} {gpa_result[0][3]})")
                print(f"  Overall GPA: {gpa_result[0][4]}\n")
                
                # Get course breakdown
                course_query = f"""
                    SELECT 
                        course_code,
                        course_name,
                        final_average
                    FROM vw_student_course_results
                    WHERE student_id = {student_id}
                    ORDER BY course_code;
                """
                course_result = DatabaseConnection.execute_query(course_query)
                
                if course_result:
                    headers = ["Code", "Course Name", "Final Average"]
                    self.print_table(headers, course_result)
                else:
                    print("  No course data found\n")
            else:
                print("  ❌ Student not found\n")
        except Exception as e:
            print(f"  ❌ Error: {e}\n")
    
    def report_top_students(self):
        """Top students by GPA (Legacy - calls weighted version)"""
        self.report_top_students_weighted_gpa()
    
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
     • Weighted GPA System: Assignment 30% | Test 30% | Exam 40%
     
  ✅ REPORTS (NEW WEIGHTED GPA FEATURES)
     • Student Transcripts (from vw_student_transcripts view)
     • Course Grade Statistics (aggregated data)
     • Enrollment Statistics
     • ⭐ Top Students by Weighted GPA (ranked by weighted average)
     • ⭐ Student Course Results (showing weighted final average)
     • ⭐ Student GPA Breakdown (per-course breakdown)
     • Low Attendance Report (< 75%)
     • Export all reports to CSV
  
  📊 WEIGHTED GPA CALCULATION
     • Formula: (Assignment × 0.30) + (Test × 0.30) + (Exam × 0.40)
     • Ensures comprehensive assessment of student performance
     • Views: vw_student_gpa, vw_student_course_results
  
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
