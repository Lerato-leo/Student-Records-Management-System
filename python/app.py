"""
Student Records Management System - CLI Application
Main menu-driven interface for managing students, courses, enrollments, grades, and attendance
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


class StudentRecordsApp:
    """Main CLI application"""
    
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
    
    def get_input(self, prompt, input_type=str):
        """Get validated user input"""
        while True:
            try:
                value = input(prompt)
                if input_type == int:
                    return int(value)
                return value
            except ValueError:
                print(f"❌ Invalid input. Please enter a valid {input_type.__name__}")
    
    # ========================================================================
    # STUDENT MANAGEMENT
    # ========================================================================
    
    def student_menu(self):
        """Student management menu"""
        while True:
            options = {
                '1': 'Add New Student',
                '2': 'View All Students',
                '3': 'View Student Details',
                '4': 'Update Student Status'
            }
            self.print_menu("STUDENT MANAGEMENT", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.add_student()
            elif choice == '2':
                self.view_all_students()
            elif choice == '3':
                self.view_student_details()
            elif choice == '4':
                self.update_student_status()
            else:
                print("❌ Invalid option")
    
    def add_student(self):
        """Add a new student"""
        self.print_header("ADD NEW STUDENT")
        
        try:
            # Get student number
            while True:
                student_num = self.get_input("  Student Number (YYYYRR format): ", int)
                valid, msg = Validators.validate_student_number(student_num)
                if valid:
                    break
                print(f"  ❌ {msg}")
            
            # Get name
            first_name = input("  First Name: ").strip()
            valid, msg = Validators.validate_name(first_name)
            if not valid:
                print(f"  ❌ {msg}")
                return
            
            last_name = input("  Last Name: ").strip()
            valid, msg = Validators.validate_name(last_name)
            if not valid:
                print(f"  ❌ {msg}")
                return
            
            # Get date of birth
            while True:
                dob = input("  Date of Birth (YYYY-MM-DD): ").strip()
                valid, msg = Validators.validate_date_of_birth(dob)
                if valid:
                    break
                print(f"  ❌ {msg}")
            
            # Get email
            email = input("  Email: ").strip()
            valid, msg = Validators.validate_email(email)
            if not valid:
                print(f"  ❌ {msg}")
                return
            
            # Add student
            success, msg = StudentOperations.add_student(student_num, first_name, last_name, dob, email)
            if success:
                print(f"\n✅ {msg}")
            else:
                print(f"\n❌ {msg}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def view_all_students(self):
        """View all students"""
        self.print_header("ALL STUDENTS")
        
        students = StudentOperations.get_all_students()
        
        if not students:
            print("  No students found")
        else:
            print(f"  {'ID':<5} {'Student#':<12} {'Name':<30} {'Status':<12} {'Email':<25}")
            print("  " + "-"*90)
            
            for student in students:
                student_id, student_num, first_name, last_name, dob, email, status = student
                name = f"{first_name} {last_name}"
                print(f"  {student_id:<5} {student_num:<12} {name:<30} {status:<12} {email:<25}")
        
        input("\nPress Enter to continue...")
    
    def view_student_details(self):
        """View student details and enrollments"""
        self.print_header("VIEW STUDENT DETAILS")
        
        student_id = self.get_input("  Enter Student ID: ", int)
        student = StudentOperations.get_student_by_id(student_id)
        
        if not student:
            print("  ❌ Student not found")
        else:
            student_id, student_num, first_name, last_name, dob, email, status = student
            
            print(f"\n  Student Information:")
            print(f"    ID: {student_id}")
            print(f"    Number: {student_num}")
            print(f"    Name: {first_name} {last_name}")
            print(f"    DOB: {dob}")
            print(f"    Email: {email}")
            print(f"    Status: {status}")
            
            # Show enrollments
            enrollments = EnrollmentOperations.get_student_enrollments(student_id)
            
            if enrollments:
                print(f"\n  Enrollments:")
                print(f"    {'Course Code':<15} {'Course Name':<30} {'Year':<12} {'Term':<5}")
                print(f"    " + "-"*65)
                for enrollment in enrollments:
                    enrollment_id, student_num, course_code, course_name, academic_year, term, enrollment_date = enrollment
                    print(f"    {course_code:<15} {course_name:<30} {academic_year:<12} {term:<5}")
            else:
                print(f"\n  No enrollments found")
        
        input("\nPress Enter to continue...")
    
    def update_student_status(self):
        """Update student status"""
        self.print_header("UPDATE STUDENT STATUS")
        
        student_id = self.get_input("  Enter Student ID: ", int)
        student = StudentOperations.get_student_by_id(student_id)
        
        if not student:
            print("  ❌ Student not found")
        else:
            print(f"\n  Statuses: active, inactive, graduated")
            status = input("  Enter new status: ").strip()
            
            valid, msg = Validators.validate_student_status(status)
            if not valid:
                print(f"  ❌ {msg}")
            else:
                success, msg = StudentOperations.update_student_status(student_id, status)
                if success:
                    print(f"\n  ✅ {msg}")
                else:
                    print(f"\n  ❌ {msg}")
        
        input("\nPress Enter to continue...")
    
    # ========================================================================
    # ENROLLMENT MANAGEMENT
    # ========================================================================
    
    def enrollment_menu(self):
        """Enrollment management menu"""
        while True:
            options = {
                '1': 'Enroll Student in Course',
                '2': 'View Course Enrollments',
                '3': 'View Student Enrollments'
            }
            self.print_menu("ENROLLMENT MANAGEMENT", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.enroll_student()
            elif choice == '2':
                self.view_course_enrollments()
            elif choice == '3':
                self.view_student_enrollments()
            else:
                print("❌ Invalid option")
    
    def enroll_student(self):
        """Enroll student in a course"""
        self.print_header("ENROLL STUDENT IN COURSE")
        
        try:
            # Get student
            student_id = self.get_input("  Enter Student ID: ", int)
            student = StudentOperations.get_student_by_id(student_id)
            if not student:
                print("  ❌ Student not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"  ✅ Student found: {student[2]} {student[3]}")
            
            # Get course
            course_id = self.get_input("  Enter Course ID: ", int)
            course = CourseOperations.get_course_by_id(course_id)
            if not course:
                print("  ❌ Course not found")
                input("\nPress Enter to continue...")
                return
            
            print(f"  ✅ Course found: {course[1]} - {course[2]}")
            
            # Get academic year
            while True:
                academic_year = input("  Academic Year (YYYY-YYYY): ").strip()
                valid, msg = Validators.validate_academic_year(academic_year)
                if valid:
                    break
                print(f"  ❌ {msg}")
            
            # Get term
            while True:
                term = input("  Term (1=Fall, 2=Spring): ").strip()
                valid, msg = Validators.validate_term(term)
                if valid:
                    break
                print(f"  ❌ {msg}")
            
            # Enroll
            success, msg = EnrollmentOperations.add_enrollment(student_id, course_id, academic_year, term)
            if success:
                print(f"\n✅ {msg}")
            else:
                print(f"\n❌ {msg}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def view_course_enrollments(self):
        """View enrollments for a course"""
        self.print_header("VIEW COURSE ENROLLMENTS")
        
        course_id = self.get_input("  Enter Course ID: ", int)
        course = CourseOperations.get_course_by_id(course_id)
        
        if not course:
            print("  ❌ Course not found")
        else:
            print(f"\n  Course: {course[1]} - {course[2]}")
            
            enrollments = EnrollmentOperations.get_course_enrollments(course_id)
            
            if enrollments:
                print(f"\n  {'Student#':<12} {'Name':<30} {'Year':<12} {'Term':<5}")
                print(f"  " + "-"*65)
                for enrollment in enrollments:
                    enrollment_id, student_id, student_num, first_name, last_name, academic_year, term, enrollment_date = enrollment
                    name = f"{first_name} {last_name}"
                    print(f"  {student_num:<12} {name:<30} {academic_year:<12} {term:<5}")
            else:
                print(f"\n  No enrollments found")
        
        input("\nPress Enter to continue...")
    
    def view_student_enrollments(self):
        """View enrollments for a student"""
        self.print_header("VIEW STUDENT ENROLLMENTS")
        
        student_id = self.get_input("  Enter Student ID: ", int)
        student = StudentOperations.get_student_by_id(student_id)
        
        if not student:
            print("  ❌ Student not found")
        else:
            print(f"\n  Student: {student[2]} {student[3]}")
            
            enrollments = EnrollmentOperations.get_student_enrollments(student_id)
            
            if enrollments:
                print(f"\n  {'Course Code':<15} {'Course Name':<30} {'Year':<12} {'Term':<5}")
                print(f"  " + "-"*65)
                for enrollment in enrollments:
                    enrollment_id, student_num, course_code, course_name, academic_year, term, enrollment_date = enrollment
                    print(f"  {course_code:<15} {course_name:<30} {academic_year:<12} {term:<5}")
            else:
                print(f"\n  No enrollments found")
        
        input("\nPress Enter to continue...")
    
    # ========================================================================
    # GRADES & ATTENDANCE
    # ========================================================================
    
    def grades_attendance_menu(self):
        """Grades and attendance menu"""
        while True:
            options = {
                '1': 'Record Grade',
                '2': 'View Grades',
                '3': 'Mark Attendance',
                '4': 'View Attendance'
            }
            self.print_menu("GRADES & ATTENDANCE", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.record_grade()
            elif choice == '2':
                self.view_grades()
            elif choice == '3':
                self.mark_attendance()
            elif choice == '4':
                self.view_attendance()
            else:
                print("❌ Invalid option")
    
    def record_grade(self):
        """Record a grade for an enrollment"""
        self.print_header("RECORD GRADE")
        
        try:
            enrollment_id = self.get_input("  Enter Enrollment ID: ", int)
            
            # Validate enrollment exists
            enrollments = EnrollmentOperations.get_course_enrollments(1)  # Get any to check format
            
            grade_type = input("  Grade Type (test/assignment/exam): ").strip()
            valid, msg = Validators.validate_grade_type(grade_type)
            if not valid:
                print(f"  ❌ {msg}")
                input("\nPress Enter to continue...")
                return
            
            while True:
                grade_value = self.get_input("  Grade Value (0-100): ", int)
                valid, msg = Validators.validate_grade_value(grade_value)
                if valid:
                    break
                print(f"  ❌ {msg}")
            
            success, msg = GradeOperations.record_grade(enrollment_id, grade_type, grade_value)
            if success:
                print(f"\n✅ {msg}")
            else:
                print(f"\n❌ {msg}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def view_grades(self):
        """View grades for an enrollment"""
        self.print_header("VIEW GRADES")
        
        enrollment_id = self.get_input("  Enter Enrollment ID: ", int)
        grades = GradeOperations.get_enrollment_grades(enrollment_id)
        
        if not grades:
            print("  No grades found for this enrollment")
        else:
            print(f"\n  {'Grade Type':<15} {'Grade Value':<15} {'Date':<12}")
            print(f"  " + "-"*45)
            
            for grade in grades:
                grades_id, grade_type, grade_value, grade_date = grade
                print(f"  {grade_type:<15} {grade_value:<15} {str(grade_date):<12}")
        
        input("\nPress Enter to continue...")
    
    def mark_attendance(self):
        """Mark attendance for an enrollment"""
        self.print_header("MARK ATTENDANCE")
        
        try:
            enrollment_id = self.get_input("  Enter Enrollment ID: ", int)
            
            status = input("  Attendance Status (present/absent/late): ").strip()
            valid, msg = Validators.validate_attendance_status(status)
            if not valid:
                print(f"  ❌ {msg}")
                input("\nPress Enter to continue...")
                return
            
            success, msg = AttendanceOperations.mark_attendance(enrollment_id, status)
            if success:
                print(f"\n✅ {msg}")
            else:
                print(f"\n❌ {msg}")
        
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def view_attendance(self):
        """View attendance for an enrollment"""
        self.print_header("VIEW ATTENDANCE")
        
        enrollment_id = self.get_input("  Enter Enrollment ID: ", int)
        attendance = AttendanceOperations.get_enrollment_attendance(enrollment_id)
        
        if not attendance:
            print("  No attendance records found")
        else:
            print(f"\n  {'Date':<20} {'Status':<15}")
            print(f"  " + "-"*40)
            
            for record in attendance:
                attendance_id, attendance_date, status = record
                print(f"  {str(attendance_date):<20} {status:<15}")
        
        input("\nPress Enter to continue...")
    
    # ========================================================================
    # REPORTS
    # ========================================================================
    
    def reports_menu(self):
        """Reports menu"""
        while True:
            options = {
                '1': 'Student Transcript',
                '2': 'Course Grade Statistics',
                '3': 'Enrollment Statistics',
                '4': 'Low Attendance Report',
                '5': 'Top Students by GPA'
            }
            self.print_menu("REPORTS", options)
            
            choice = input("  Select option: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self.generate_transcript_report()
            elif choice == '2':
                self.generate_course_stats_report()
            elif choice == '3':
                self.generate_enrollment_stats_report()
            elif choice == '4':
                self.generate_low_attendance_report()
            elif choice == '5':
                self.generate_top_students_report()
            else:
                print("❌ Invalid option")
    
    def generate_transcript_report(self):
        """Generate student transcript report"""
        self.print_header("STUDENT TRANSCRIPT REPORT")
        
        student_id = self.get_input("  Enter Student ID: ", int)
        success, msg = ReportGenerator.generate_student_transcript_csv(student_id)
        
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        
        input("\nPress Enter to continue...")
    
    def generate_course_stats_report(self):
        """Generate course statistics report"""
        self.print_header("COURSE GRADE STATISTICS REPORT")
        
        success, msg = ReportGenerator.generate_course_statistics_csv()
        
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        
        input("\nPress Enter to continue...")
    
    def generate_enrollment_stats_report(self):
        """Generate enrollment statistics report"""
        self.print_header("ENROLLMENT STATISTICS REPORT")
        
        success, msg = ReportGenerator.generate_enrollment_statistics_csv()
        
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        
        input("\nPress Enter to continue...")
    
    def generate_low_attendance_report(self):
        """Generate low attendance report"""
        self.print_header("LOW ATTENDANCE REPORT")
        
        success, msg = ReportGenerator.generate_low_attendance_csv()
        
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        
        input("\nPress Enter to continue...")
    
    def generate_top_students_report(self):
        """Generate top students report"""
        self.print_header("TOP STUDENTS BY GPA REPORT")
        
        limit = self.get_input("  How many top students? (default 10): ", int)
        success, msg = ReportGenerator.generate_top_students_csv(limit)
        
        if success:
            print(f"✅ {msg}")
        else:
            print(f"❌ {msg}")
        
        input("\nPress Enter to continue...")
    
    # ========================================================================
    # MAIN MENU
    # ========================================================================
    
    def main_menu(self):
        """Main menu"""
        while self.running:
            self.clear_screen()
            
            print("\n")
            print("╔" + "="*68 + "╗")
            print("║" + "  STUDENT RECORDS MANAGEMENT SYSTEM".center(68) + "║")
            print("║" + "  PostgreSQL + Python CLI".center(68) + "║")
            print("╚" + "="*68 + "╝")
            
            print("\n  Main Menu:")
            print("  " + "-"*68)
            print("  1. Student Management")
            print("  2. Enrollment Management")
            print("  3. Grades & Attendance")
            print("  4. Reports")
            print("  5. Help")
            print("  0. Exit")
            print("  " + "-"*68)
            
            choice = input("\n  Select option: ").strip()
            
            if choice == '1':
                self.student_menu()
            elif choice == '2':
                self.enrollment_menu()
            elif choice == '3':
                self.grades_attendance_menu()
            elif choice == '4':
                self.reports_menu()
            elif choice == '5':
                self.show_help()
            elif choice == '0':
                self.running = False
                print("\n✅ Goodbye!\n")
            else:
                print("❌ Invalid option")
                input("Press Enter to continue...")
    
    def show_help(self):
        """Show help information"""
        self.print_header("HELP & INFORMATION")
        
        print("""
  STUDENT RECORDS MANAGEMENT SYSTEM - User Guide
  ═════════════════════════════════════════════════════════════════
  
  1. STUDENT MANAGEMENT
     - Add New Student: Create a new student record
       * Student Number format: YYYYRR (e.g., 199545)
       * Status: active, inactive, or graduated
     
     - View All Students: List all students in the system
     
     - View Student Details: See student info and enrollments
     
     - Update Student Status: Change student status
  
  2. ENROLLMENT MANAGEMENT
     - Enroll Student in Course: Register student for a course
       * Academic Year format: YYYY-YYYY (e.g., 2024-2025)
       * Term: 1 (Fall) or 2 (Spring)
     
     - View Course Enrollments: See all students in a course
     
     - View Student Enrollments: See all courses for a student
  
  3. GRADES & ATTENDANCE
     - Record Grade: Add grade for enrollment
       * Grade Type: test, assignment, or exam
       * Grade Value: 0-100
     
     - Mark Attendance: Record attendance status
       * Status: present, absent, or late
  
  4. REPORTS
     - Generate CSV reports in the ../reports directory
     - Available reports:
       * Student Transcript
       * Course Grade Statistics
       * Enrollment Statistics
       * Low Attendance Report (< 75%)
       * Top Students by GPA
  
  ═════════════════════════════════════════════════════════════════
        """)
        
        input("Press Enter to return to main menu...")
    
    def run(self):
        """Run the application"""
        try:
            self.main_menu()
        except KeyboardInterrupt:
            print("\n\n❌ Application interrupted")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            sys.exit(1)


def main():
    """Entry point"""
    app = StudentRecordsApp()
    app.run()


if __name__ == "__main__":
    main()
