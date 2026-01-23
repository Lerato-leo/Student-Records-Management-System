"""
Report Generator
Generates CSV and PDF reports
"""

import csv
import os
from datetime import datetime
from database import DatabaseConnection
from operations import ReportOperations, StudentOperations, EnrollmentOperations, GradeOperations

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


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

    # ========================================================================
    # PDF EXPORT METHODS (Using ReportLab)
    # ========================================================================
    
    @classmethod
    def generate_student_transcript_pdf(cls, student_id):
        """Generate student transcript as PDF"""
        if not REPORTLAB_AVAILABLE:
            return False, "ReportLab not installed. Install with: pip install reportlab"
        
        try:
            cls.ensure_output_dir()
            
            # Get student info
            student = StudentOperations.get_student_by_id(student_id)
            if not student:
                return False, "Student not found"
            
            student_id, student_num, first_name, last_name, dob, email, status = student
            
            # Get transcript from database view
            query = f"SELECT * FROM vw_student_transcripts WHERE student_id = {student_id};"
            transcript = DatabaseConnection.execute_query(query)
            
            if not transcript:
                return False, "No transcript data found"
            
            # Create PDF filename
            filename = f"transcript_{student_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            # Create PDF
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph('STUDENT TRANSCRIPT', title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # Student Information Section
            student_info_style = ParagraphStyle(
                'StudentInfo',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=6
            )
            
            story.append(Paragraph(f"<b>Student Number:</b> {student_num}", student_info_style))
            story.append(Paragraph(f"<b>Name:</b> {first_name} {last_name}", student_info_style))
            story.append(Paragraph(f"<b>Email:</b> {email}", student_info_style))
            story.append(Paragraph(f"<b>Status:</b> {status}", student_info_style))
            story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", student_info_style))
            story.append(Spacer(1, 0.3*inch))
            
            # Transcript Table
            table_data = [['Course Code', 'Course Name', 'Academic Year', 'Term', 'Average Grade']]
            
            for row in transcript:
                # row format: student_id, student_num, first_name, last_name, course_code, course_name, academic_year, term, avg_grade
                course_code = row[4]
                course_name = row[5]
                academic_year = row[6]
                term = row[7]
                avg_grade = str(row[8]) if row[8] else 'N/A'
                
                table_data.append([course_code, course_name, academic_year, term, avg_grade])
            
            # Create table with styling
            table = Table(table_data, colWidths=[1.2*inch, 2*inch, 1.2*inch, 0.6*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.3*inch))
            
            # Summary
            total_courses = len(transcript)
            avg_grades = [float(row[8]) for row in transcript if row[8]]
            overall_avg = sum(avg_grades) / len(avg_grades) if avg_grades else 0
            
            summary_style = ParagraphStyle(
                'Summary',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#1f4788'),
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph(f"<b>Summary:</b> Total Courses: {total_courses} | Overall Average: {overall_avg:.2f}", summary_style))
            
            # Build PDF
            doc.build(story)
            
            return True, f"Transcript PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
    
    @classmethod
    def generate_course_statistics_pdf(cls):
        """Generate course grade statistics as PDF"""
        if not REPORTLAB_AVAILABLE:
            return False, "ReportLab not installed"
        
        try:
            cls.ensure_output_dir()
            
            # Get course statistics
            query = """
                SELECT 
                    c.course_code,
                    c.course_name,
                    COUNT(DISTINCT e.student_id) AS total_students,
                    COUNT(g.grades_id) AS total_grades,
                    ROUND(AVG(g.grade_value)::NUMERIC, 2) AS avg_grade,
                    MAX(g.grade_value) AS highest_grade,
                    MIN(g.grade_value) AS lowest_grade
                FROM courses c
                LEFT JOIN enrollments e ON c.course_id = e.course_id
                LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
                WHERE c.status = 'active'
                GROUP BY c.course_id, c.course_code, c.course_name
                ORDER BY c.course_code;
            """
            stats = DatabaseConnection.execute_query(query)
            
            if not stats:
                return False, "No statistics data found"
            
            filename = f"course_statistics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph('COURSE GRADE STATISTICS', title_style))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Statistics Table
            table_data = [['Course Code', 'Course Name', 'Students', 'Grades', 'Avg Grade', 'High', 'Low']]
            
            for row in stats:
                table_data.append([
                    str(row[0]),
                    str(row[1])[:20],
                    str(row[2]),
                    str(row[3]),
                    str(row[4]),
                    str(row[5]) if row[5] else 'N/A',
                    str(row[6]) if row[6] else 'N/A'
                ])
            
            table = Table(table_data, colWidths=[1*inch, 1.8*inch, 0.8*inch, 0.8*inch, 0.9*inch, 0.7*inch, 0.7*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
            ]))
            
            story.append(table)
            doc.build(story)
            
            return True, f"Course statistics PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
    
    @classmethod
    def generate_top_students_pdf(cls, limit=10):
        """Generate top students by GPA as PDF"""
        if not REPORTLAB_AVAILABLE:
            return False, "ReportLab not installed"
        
        try:
            cls.ensure_output_dir()
            
            # Get top students
            query = f"""
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
                LIMIT {limit};
            """
            students = DatabaseConnection.execute_query(query)
            
            if not students:
                return False, "No student data found"
            
            filename = f"top_students_{limit}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            story = []
            styles = getSampleStyleSheet()
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=30,
                alignment=1
            )
            story.append(Paragraph(f'TOP {limit} STUDENTS BY GPA', title_style))
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            story.append(Spacer(1, 0.2*inch))
            
            # Students Table
            table_data = [['Rank', 'Student #', 'First Name', 'Last Name', 'GPA', 'Total Grades']]
            
            for row in students:
                table_data.append([
                    str(row[0]),
                    str(row[1]),
                    str(row[2]),
                    str(row[3]),
                    str(row[4]),
                    str(row[5])
                ])
            
            table = Table(table_data, colWidths=[0.6*inch, 1*inch, 1.2*inch, 1.2*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')])
            ]))
            
            story.append(table)
            doc.build(story)
            
            return True, f"Top students PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"

