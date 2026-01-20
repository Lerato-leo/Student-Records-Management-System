"""
Report Generator
Generates CSV and PDF reports
"""

import csv
import os
from datetime import datetime
from operations import ReportOperations, StudentOperations, EnrollmentOperations, GradeOperations


class ReportGenerator:
    """Generate reports in CSV and PDF formats"""
    
    OUTPUT_DIR = "../reports"
    
    @classmethod
    def ensure_output_dir(cls):
        """Create output directory if it doesn't exist"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
    
    @classmethod
    def generate_student_transcript_csv(cls, student_id):
        """Generate student transcript as CSV"""
        try:
            cls.ensure_output_dir()
            
            # Get student info
            student = StudentOperations.get_student_by_id(student_id)
            if not student:
                return False, "Student not found"
            
            student_id, student_num, first_name, last_name, dob, email, status = student
            
            # Get transcript
            transcript = GradeOperations.get_student_transcript(student_id)
            if not transcript:
                return False, "No transcript data found"
            
            # Create filename
            filename = f"transcript_{student_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            # Write CSV
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Header with student info
                writer.writerow(['STUDENT TRANSCRIPT'])
                writer.writerow([])
                writer.writerow(['Student Number:', student_num])
                writer.writerow(['Name:', f"{first_name} {last_name}"])
                writer.writerow(['Email:', email])
                writer.writerow(['Status:', status])
                writer.writerow([])
                
                # Transcript data
                writer.writerow(['Student ID', 'Student Number', 'First Name', 'Last Name', 
                                'Course Code', 'Course Name', 'Academic Year', 'Term', 'Average Grade'])
                
                for row in transcript:
                    writer.writerow(row)
            
            return True, f"Transcript saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating transcript: {str(e)}"
    
    @classmethod
    def generate_course_statistics_csv(cls):
        """Generate course grade statistics as CSV"""
        try:
            cls.ensure_output_dir()
            
            stats = ReportOperations.get_course_grade_statistics()
            if not stats:
                return False, "No statistics data found"
            
            filename = f"course_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow(['COURSE GRADE STATISTICS'])
                writer.writerow([])
                writer.writerow(['Course Code', 'Course Name', 'Total Students', 'Total Grades',
                                'Average Grade', 'Highest Grade', 'Lowest Grade'])
                
                for row in stats:
                    writer.writerow(row)
            
            return True, f"Statistics saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating statistics: {str(e)}"
    
    @classmethod
    def generate_enrollment_statistics_csv(cls):
        """Generate enrollment statistics as CSV"""
        try:
            cls.ensure_output_dir()
            
            stats = ReportOperations.get_enrollment_statistics()
            if not stats:
                return False, "No enrollment data found"
            
            filename = f"enrollment_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow(['ENROLLMENT STATISTICS'])
                writer.writerow([])
                writer.writerow(['Course Code', 'Course Name', 'Total Enrollments',
                                'Unique Students', 'Students with Grades'])
                
                for row in stats:
                    writer.writerow(row)
            
            return True, f"Enrollment statistics saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating enrollment statistics: {str(e)}"
    
    @classmethod
    def generate_low_attendance_csv(cls):
        """Generate low attendance report as CSV"""
        try:
            cls.ensure_output_dir()
            
            students = ReportOperations.get_low_attendance_students()
            if not students:
                return True, "No students with low attendance"
            
            filename = f"low_attendance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow(['LOW ATTENDANCE STUDENTS (<75%)'])
                writer.writerow([])
                writer.writerow(['Student Number', 'First Name', 'Last Name', 'Course Code',
                                'Total Classes', 'Classes Attended', 'Attendance Percentage'])
                
                for row in students:
                    writer.writerow(row)
            
            return True, f"Low attendance report saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating low attendance report: {str(e)}"
    
    @classmethod
    def generate_top_students_csv(cls, limit=10):
        """Generate top students by GPA report as CSV"""
        try:
            cls.ensure_output_dir()
            
            students = ReportOperations.get_top_students_by_gpa(limit)
            if not students:
                return False, "No student data found"
            
            filename = f"top_students_{limit}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                writer.writerow([f'TOP {limit} STUDENTS BY GPA'])
                writer.writerow([])
                writer.writerow(['Rank', 'Student Number', 'First Name', 'Last Name', 'GPA', 'Total Grades'])
                
                for row in students:
                    writer.writerow(row)
            
            return True, f"Top students report saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating top students report: {str(e)}"
