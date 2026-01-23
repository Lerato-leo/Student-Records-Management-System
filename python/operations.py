"""
Database Operations
CRUD operations and stored procedure calls
"""

from database import DatabaseConnection
from validators import Validators


class StudentOperations:
    """Student management operations"""
    
    @staticmethod
    def add_student(student_number, first_name, last_name, date_of_birth, email, status='active'):
        """Add a new student to the database"""
        try:
            query = f"""
                INSERT INTO students (student_number, first_name, last_name, date_of_birth, email, status)
                VALUES ({student_number}, '{first_name}', '{last_name}', '{date_of_birth}', '{email}', '{status.lower()}')
                RETURNING student_id, student_number, first_name, last_name;
            """
            result = DatabaseConnection.execute_query(query)
            if result:
                student_id, student_num, fname, lname = result[0]
                return True, f"Student {fname} {lname} (ID: {student_id}) added successfully"
            return False, "Failed to add student"
        except Exception as e:
            return False, f"Error adding student: {str(e)}"
    
    @staticmethod
    def get_all_students():
        """Get all students (newest first)"""
        try:
            query = """
                SELECT student_id, student_number, first_name, last_name, date_of_birth, email, status
                FROM students
                ORDER BY student_id DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_student_by_id(student_id):
        """Get student by ID"""
        try:
            query = f"""
                SELECT student_id, student_number, first_name, last_name, date_of_birth, email, status
                FROM students
                WHERE student_id = {student_id}
            """
            result = DatabaseConnection.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            return None
    
    @staticmethod
    def get_student_by_number(student_number):
        """Get student by student number"""
        try:
            query = f"""
                SELECT student_id, student_number, first_name, last_name, date_of_birth, email, status
                FROM students
                WHERE student_number = {student_number}
            """
            result = DatabaseConnection.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            return None
    
    @staticmethod
    def update_student_status(student_id, status):
        """Update student status"""
        try:
            query = f"""
                UPDATE students
                SET status = '{status.lower()}'
                WHERE student_id = {student_id}
            """
            DatabaseConnection.execute_procedure(query)
            return True, f"Student status updated to '{status}'"
        except Exception as e:
            return False, f"Error updating status: {str(e)}"


class CourseOperations:
    """Course management operations"""
    
    @staticmethod
    def get_all_courses():
        """Get all courses"""
        try:
            query = """
                SELECT course_id, course_code, course_name, credits, status
                FROM courses
                WHERE status = 'active'
                ORDER BY course_code
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_course_by_id(course_id):
        """Get course by ID"""
        try:
            query = f"""
                SELECT course_id, course_code, course_name, credits, status
                FROM courses
                WHERE course_id = {course_id}
            """
            result = DatabaseConnection.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            return None


class EnrollmentOperations:
    """Enrollment management operations"""
    
    @staticmethod
    def add_enrollment(student_id, course_id, academic_year, term):
        """Add student enrollment using stored procedure"""
        try:
            procedure_call = f"""
                CALL add_student_enrollment(NULL, {student_id}, {course_id}, '{academic_year}', '{term}')
            """
            DatabaseConnection.execute_procedure(procedure_call)
            return True, f"Student enrolled successfully in course (Academic Year: {academic_year}, Term: {term})"
        except Exception as e:
            error_msg = str(e)
            if "duplicate" in error_msg.lower() or "unique" in error_msg.lower():
                return False, "Student is already enrolled in this course for this term"
            elif "not found" in error_msg.lower():
                return False, "Student or course not found"
            else:
                return False, f"Error enrolling student: {error_msg[:100]}"
    
    @staticmethod
    def get_student_enrollments(student_id):
        """Get all enrollments for a student"""
        try:
            query = f"""
                SELECT e.enrollment_id, s.student_number, c.course_code, c.course_name, 
                       e.academic_year, e.term, e.enrollment_date
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                JOIN courses c ON e.course_id = c.course_id
                WHERE e.student_id = {student_id}
                ORDER BY e.academic_year DESC, e.term
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_course_enrollments(course_id):
        """Get all enrollments for a course"""
        try:
            query = f"""
                SELECT e.enrollment_id, s.student_id, s.student_number, s.first_name, s.last_name,
                       e.academic_year, e.term, e.enrollment_date
                FROM enrollments e
                JOIN students s ON e.student_id = s.student_id
                WHERE e.course_id = {course_id}
                ORDER BY s.student_number
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None


class GradeOperations:
    """Grade management operations"""
    
    @staticmethod
    def record_grade(enrollment_id, grade_type, grade_value):
        """Record grade using stored procedure"""
        try:
            procedure_call = f"""
                CALL record_grade(NULL, {enrollment_id}, '{grade_type.lower()}', {grade_value})
            """
            DatabaseConnection.execute_procedure(procedure_call)
            return True, f"Grade recorded: {grade_type} = {grade_value}"
        except Exception as e:
            error_msg = str(e)
            if "between 0 and 100" in error_msg.lower():
                return False, "Grade must be between 0 and 100"
            elif "not found" in error_msg.lower():
                return False, "Enrollment not found"
            else:
                return False, f"Error recording grade: {error_msg[:100]}"
    
    @staticmethod
    def get_enrollment_grades(enrollment_id):
        """Get all grades for an enrollment"""
        try:
            query = f"""
                SELECT grades_id, grade_type, grade_value, grade_date
                FROM grades
                WHERE enrollment_id = {enrollment_id}
                ORDER BY grade_date DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_student_transcript(student_id):
        """Get student transcript (all grades from all courses)"""
        try:
            query = f"""
                SELECT * FROM vw_student_transcripts
                WHERE student_id = {student_id}
                ORDER BY academic_year DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None


class AttendanceOperations:
    """Attendance management operations"""
    
    @staticmethod
    def mark_attendance(enrollment_id, status, attendance_date='CURRENT_DATE'):
        """Mark attendance using stored procedure"""
        try:
            procedure_call = f"""
                CALL mark_attendance(NULL, {enrollment_id}, '{status.lower()}', {attendance_date})
            """
            DatabaseConnection.execute_procedure(procedure_call)
            return True, f"Attendance recorded: {status}"
        except Exception as e:
            error_msg = str(e)
            if "not found" in error_msg.lower():
                return False, "Enrollment not found"
            else:
                return False, f"Error marking attendance: {error_msg[:100]}"
    
    @staticmethod
    def get_enrollment_attendance(enrollment_id):
        """Get attendance records for an enrollment"""
        try:
            query = f"""
                SELECT attendance_id, attendance_date, status
                FROM attendance
                WHERE enrollment_id = {enrollment_id}
                ORDER BY attendance_date DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None


class ReportOperations:
    """Report and statistics operations"""
    
    @staticmethod
    def get_course_grade_statistics():
        """Get grade statistics for all courses"""
        try:
            query = """SELECT * FROM get_course_grade_statistics()"""
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_low_attendance_students():
        """Get students with <75% attendance"""
        try:
            query = """SELECT * FROM get_low_attendance_students()"""
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_top_students_by_gpa(limit=10):
        """Get top students by GPA"""
        try:
            query = f"""SELECT * FROM get_top_students_by_gpa({limit})"""
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None
    
    @staticmethod
    def get_enrollment_statistics():
        """Get enrollment statistics for all courses"""
        try:
            query = """SELECT * FROM get_enrollment_statistics()"""
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return None


class EnrollmentOperations:
    """Enrollment management operations"""
    
    @staticmethod
    def add_enrollment(student_id, course_id, academic_year, term):
        """Add new enrollment"""
        try:
            query = f"""
                INSERT INTO enrollments (student_id, course_id, academic_year, term, enrollment_date)
                VALUES ({student_id}, {course_id}, '{academic_year}', '{term}', CURRENT_DATE)
                RETURNING enrollment_id;
            """
            result = DatabaseConnection.execute_query(query)
            if result:
                return True, f"Enrollment added successfully (ID: {result[0][0]})"
            return False, "Failed to add enrollment"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_all_enrollments():
        """Get all enrollments (newest first)"""
        try:
            query = """
                SELECT enrollment_id, student_id, course_id, academic_year, term, enrollment_date
                FROM enrollments
                ORDER BY enrollment_id DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return []
    
    @staticmethod
    def get_enrollment_by_id(enrollment_id):
        """Get enrollment by ID"""
        try:
            query = f"""
                SELECT enrollment_id, student_id, course_id, academic_year, term, enrollment_date
                FROM enrollments
                WHERE enrollment_id = {enrollment_id}
            """
            result = DatabaseConnection.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            return None


class GradeOperations:
    """Grade management operations"""
    
    @staticmethod
    def add_grade(enrollment_id, grade_type, grade_value):
        """Add grade"""
        try:
            query = f"""
                INSERT INTO grades (enrollment_id, grade_type, grade_value, grade_date)
                VALUES ({enrollment_id}, '{grade_type}', {grade_value}, CURRENT_DATE)
                RETURNING grades_id;
            """
            result = DatabaseConnection.execute_query(query)
            if result:
                return True, f"Grade added successfully"
            return False, "Failed to add grade"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_all_grades():
        """Get all grades (newest first)"""
        try:
            query = """
                SELECT grades_id, enrollment_id, grade_type, grade_value, grade_date
                FROM grades
                ORDER BY grades_id DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return []
    
    @staticmethod
    def get_grade_by_id(grade_id):
        """Get grade by ID"""
        try:
            query = f"""
                SELECT grades_id, enrollment_id, grade_type, grade_value, grade_date
                FROM grades
                WHERE grades_id = {grade_id}
            """
            result = DatabaseConnection.execute_query(query)
            return result[0] if result else None
        except Exception as e:
            return None


class AttendanceOperations:
    """Attendance management operations"""
    
    @staticmethod
    def mark_attendance(enrollment_id, status):
        """Mark attendance"""
        try:
            query = f"""
                INSERT INTO attendance (enrollment_id, attendance_date, status)
                VALUES ({enrollment_id}, CURRENT_DATE, '{status}')
                RETURNING attendance_id;
            """
            result = DatabaseConnection.execute_query(query)
            if result:
                return True, f"Attendance marked as '{status}'"
            return False, "Failed to mark attendance"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_all_attendance():
        """Get all attendance records (newest first)"""
        try:
            query = """
                SELECT attendance_id, enrollment_id, attendance_date, status
                FROM attendance
                ORDER BY attendance_id DESC
            """
            return DatabaseConnection.execute_query(query)
        except Exception as e:
            return []
