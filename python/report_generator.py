"""
Report Generator
Generates CSV and PDF reports with academic audit compliance
"""

import csv
import os
import hashlib
import uuid
from datetime import datetime, timedelta
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

# Institution Information (for audit compliance)
INSTITUTION_INFO = {
    'name': 'Educational Records System',
    'accreditation': 'Certified Academic Institution',
    'email': 'registrar@institution.edu',
    'phone': '+1 (555) 123-4567',
    'address': 'Academic Records Office',
}


class ReportGenerator:
    """Generate reports in CSV and PDF formats with audit compliance"""
    
    OUTPUT_DIR = "../reports"
    
    @classmethod
    def ensure_output_dir(cls):
        """Create output directory if it doesn't exist"""
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
    
    @classmethod
    def generate_document_id(cls):
        """Generate unique audit-compliant document ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique = str(uuid.uuid4())[:8].upper()
        return f"DOC-{timestamp}-{unique}"
    
    @classmethod
    def generate_verification_code(cls, student_id, student_num, timestamp):
        """Generate tamper-evident verification code"""
        data = f"{student_id}{student_num}{timestamp}OFFICIAL".encode()
        return hashlib.sha256(data).hexdigest()[:16].upper()
    
    @classmethod
    def get_validity_period(cls):
        """Return report validity dates"""
        issued = datetime.now()
        expires = issued + timedelta(days=365)
        return issued, expires
    
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
        """Generate audit-compliant student transcript PDF for official academic records"""
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
            
            # Generate audit compliance identifiers
            document_id = cls.generate_document_id()
            issued_date, expires_date = cls.get_validity_period()
            verification_code = cls.generate_verification_code(student_id, student_num, issued_date.strftime('%Y%m%d'))
            
            # Create PDF filename with document ID
            filename = f"transcript_{student_num}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(cls.OUTPUT_DIR, filename)
            
            # Create PDF with audit-compliant margins
            doc = SimpleDocTemplate(filepath, pagesize=letter, 
                                   leftMargin=0.75*inch, rightMargin=0.75*inch,
                                   topMargin=0.5*inch, bottomMargin=1*inch)
            story = []
            styles = getSampleStyleSheet()
            
            # ========== OFFICIAL INSTITUTION HEADER ==========
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor('#1f4788'),
                alignment=1,
                spaceAfter=2,
                fontName='Helvetica-Bold'
            )
            subheader_style = ParagraphStyle(
                'SubHeaderStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#666666'),
                alignment=1,
                spaceAfter=1
            )
            
            story.append(Paragraph(INSTITUTION_INFO['name'], header_style))
            story.append(Paragraph(INSTITUTION_INFO['address'], subheader_style))
            story.append(Paragraph(f"Phone: {INSTITUTION_INFO['phone']} | Email: {INSTITUTION_INFO['email']}", subheader_style))
            story.append(Paragraph(f"Accreditation: {INSTITUTION_INFO['accreditation']}", subheader_style))
            story.append(Spacer(1, 0.2*inch))
            
            # ========== OFFICIAL TITLE ==========
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=26,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=12,
                alignment=1,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph('OFFICIAL ACADEMIC TRANSCRIPT', title_style))
            
            # ========== AUDIT COMPLIANCE SECTION ==========
            compliance_style = ParagraphStyle(
                'ComplianceStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#CC0000'),
                alignment=1,
                spaceAfter=6
            )
            story.append(Paragraph("This is an official academic record. Unauthorized reproduction or alteration is prohibited.", compliance_style))
            
            # ========== DOCUMENT IDENTIFIERS (Audit Trail) ==========
            audit_data = [
                ['Document ID:', document_id, 'Issued:', issued_date.strftime('%B %d, %Y')],
                ['Verification Code:', verification_code, 'Valid Until:', expires_date.strftime('%B %d, %Y')]
            ]
            
            audit_table = Table(audit_data, colWidths=[1.3*inch, 1.7*inch, 1.3*inch, 1.7*inch])
            audit_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#1f4788')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Courier'),
                ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc'))
            ]))
            
            story.append(audit_table)
            story.append(Spacer(1, 0.2*inch))
            
            # ========== STUDENT INFORMATION SECTION ==========
            student_info_data = [
                ['Student Number:', str(student_num), 'Legal Name:', f"{first_name} {last_name}"],
                ['Date of Birth:', str(dob), 'Enrollment Status:', status.upper()],
                ['Email Address:', email, 'Record Last Updated:', datetime.now().strftime('%Y-%m-%d')]
            ]
            
            student_info_table = Table(student_info_data, colWidths=[1.2*inch, 1.8*inch, 1.2*inch, 1.8*inch])
            student_info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTNAME', (3, 0), (3, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f9f9f9')])
            ]))
            
            story.append(student_info_table)
            story.append(Spacer(1, 0.2*inch))
            
            # ========== ACADEMIC RECORD HEADER ==========
            record_header = ParagraphStyle(
                'RecordHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=10,
                fontName='Helvetica-Bold',
                borderPadding=5
            )
            story.append(Paragraph('ACADEMIC RECORD - OFFICIAL COURSES AND GRADES', record_header))
            
            # ========== TRANSCRIPT TABLE ==========
            table_data = [['Course Code', 'Course Name', 'Academic Year', 'Term', 'Grade', 'Status']]
            
            for row in transcript:
                course_code = row[4]
                course_name = row[5][:28]
                academic_year = row[6]
                term = f"Term {row[7]}"
                avg_grade = f"{float(row[8]):.2f}" if row[8] else 'N/A'
                # Status based on grade (audit compliance)
                status_val = "PASSED" if row[8] and float(row[8]) >= 60 else "AUDIT" if row[8] else "PENDING"
                
                table_data.append([course_code, course_name, academic_year, term, avg_grade, status_val])
            
            table = Table(table_data, colWidths=[1*inch, 2.1*inch, 1*inch, 0.75*inch, 0.9*inch, 0.9*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fafafa')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGNMENT', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1.2, colors.HexColor('#1f4788')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f0f7ff')])
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.2*inch))
            
            # ========== ACADEMIC SUMMARY WITH CONSTRAINTS ==========
            total_courses = len(transcript)
            avg_grades = [float(row[8]) for row in transcript if row[8]]
            overall_avg = sum(avg_grades) / len(avg_grades) if avg_grades else 0
            
            summary_header = ParagraphStyle(
                'SummaryHeader',
                parent=styles['Heading2'],
                fontSize=11,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=8,
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph('ACADEMIC SUMMARY AND GRADE STATISTICS', summary_header))
            
            summary_data = [
                ['Total Courses Completed:', str(total_courses), 'Overall GPA:', f'{overall_avg:.2f}'],
                ['Minimum Grade Threshold:', '60', 'Average Grade Range:', '0-100'],
                ['Grade Scale: A (90-100) | B (80-89) | C (70-79) | D (60-69) | F (0-59)', '', '', '']
            ]
            
            summary_table = Table(summary_data, colWidths=[2*inch, 1.2*inch, 1.5*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 1), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 1), colors.whitesmoke),
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f0f0f0')),
                ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),
                ('FONTNAME', (0, 2), (-1, 2), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, 1), 10),
                ('FONTSIZE', (0, 2), (-1, 2), 8),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, 1), 1, colors.whitesmoke),
                ('GRID', (0, 2), (-1, 2), 0.5, colors.HexColor('#cccccc'))
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # ========== OFFICIAL CERTIFICATION & FOOTER ==========
            certification_style = ParagraphStyle(
                'CertificationStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#1f4788'),
                fontName='Helvetica-Bold',
                spaceAfter=4,
                alignment=0
            )
            
            normal_style = ParagraphStyle(
                'NormalStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#333333'),
                alignment=0,
                spaceAfter=2
            )
            
            story.append(Paragraph('CERTIFICATION:', certification_style))
            story.append(Paragraph('This official academic transcript is a complete and accurate record of the academic progress and achievements of the named student. This document is prepared in accordance with institutional policies and federal regulations governing educational records.', normal_style))
            story.append(Spacer(1, 0.15*inch))
            
            story.append(Paragraph('CONFIDENTIALITY NOTICE:', certification_style))
            story.append(Paragraph('This document contains confidential educational records protected under FERPA (Family Educational Rights and Privacy Act). Unauthorized access, use, or distribution is prohibited by federal law.', normal_style))
            story.append(Spacer(1, 0.2*inch))
            
            # ========== OFFICIAL FOOTER ==========
            footer_style = ParagraphStyle(
                'FooterStyle',
                parent=styles['Normal'],
                fontSize=7,
                textColor=colors.HexColor('#999999'),
                alignment=1,
                spaceAfter=1
            )
            
            story.append(Paragraph("═" * 80, footer_style))
            story.append(Paragraph(f"Document ID: {document_id} | Verification Code: {verification_code}", footer_style))
            story.append(Paragraph(f"Generated: {issued_date.strftime('%B %d, %Y at %H:%M:%S %Z')} | Valid Until: {expires_date.strftime('%B %d, %Y')}", footer_style))
            story.append(Paragraph(f"Contact Registrar for verification: {INSTITUTION_INFO['email']} | {INSTITUTION_INFO['phone']}", footer_style))
            story.append(Paragraph("OFFICIAL SEAL - TAMPER EVIDENT", footer_style))
            
            # Build PDF
            doc.build(story)
            
            return True, f"Official transcript PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
            
            # ========== STUDENT INFORMATION SECTION ==========
            story.append(Spacer(1, 0.1*inch))
            
            # Student info in a professional box style
            student_info_data = [
                ['Student Number:', str(student_num), 'Email:', email],
                ['Full Name:', f"{first_name} {last_name}", 'Status:', status.upper()],
                ['Date of Birth:', str(dob), 'Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]
            
            student_info_table = Table(student_info_data, colWidths=[1.2*inch, 1.8*inch, 1*inch, 1.8*inch])
            student_info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f9f9f9')])
            ]))
            
            story.append(student_info_table)
            story.append(Spacer(1, 0.25*inch))
            
            # ========== TRANSCRIPT SECTION HEADER ==========
            transcript_header_style = ParagraphStyle(
                'TranscriptHeader',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=12,
                fontName='Helvetica-Bold',
                borderPadding=5
            )
            story.append(Paragraph('Academic Record', transcript_header_style))
            
            # ========== TRANSCRIPT TABLE ==========
            table_data = [['Course Code', 'Course Name', 'Academic Year', 'Term', 'Average Grade']]
            
            for row in transcript:
                # row format: student_id, student_num, first_name, last_name, course_code, course_name, academic_year, term, avg_grade
                course_code = row[4]
                course_name = row[5][:30]  # Truncate long names
                academic_year = row[6]
                term = f"Term {row[7]}"
                avg_grade = f"{float(row[8]):.2f}" if row[8] else 'N/A'
                
                table_data.append([course_code, course_name, academic_year, term, avg_grade])
            
            # Create table with enhanced styling
            table = Table(table_data, colWidths=[1.1*inch, 2.2*inch, 1*inch, 0.8*inch, 1.2*inch])
            table.setStyle(TableStyle([
                # Header styling
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Data rows styling
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fafafa')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGNMENT', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                # Grid styling
                ('GRID', (0, 0), (-1, -1), 1.2, colors.HexColor('#1f4788')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f0f7ff')])
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.25*inch))
            
            # ========== SUMMARY SECTION ==========
            total_courses = len(transcript)
            avg_grades = [float(row[8]) for row in transcript if row[8]]
            overall_avg = sum(avg_grades) / len(avg_grades) if avg_grades else 0
            
            # Summary box
            summary_style = ParagraphStyle(
                'SummaryStyle',
                parent=styles['Normal'],
                fontSize=10,
                fontName='Helvetica-Bold',
                textColor=colors.HexColor('#1f4788')
            )
            
            summary_data = [
                ['Total Courses:', str(total_courses), 'Overall Average:', f'{overall_avg:.2f}']
            ]
            
            summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.whitesmoke)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # ========== FOOTER ==========
            footer_style = ParagraphStyle(
                'FooterStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=1,
                spaceAfter=0
            )
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("This is an official academic record. For official use only.", footer_style))
            story.append(Paragraph(f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", footer_style))
            
            # Build PDF
            doc.build(story)
            
            return True, f"Transcript PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
    
    @classmethod
    def generate_course_statistics_pdf(cls):
        """Generate course grade statistics as PDF with professional styling"""
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
            
            # Create PDF with margins
            doc = SimpleDocTemplate(filepath, pagesize=letter,
                                   leftMargin=0.5*inch, rightMargin=0.5*inch,
                                   topMargin=0.75*inch, bottomMargin=0.75*inch)
            story = []
            styles = getSampleStyleSheet()
            
            # ========== HEADER ==========
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#666666'),
                alignment=1,
                spaceAfter=3
            )
            story.append(Paragraph("Student Records Management System", header_style))
            story.append(Paragraph("Course Performance & Statistics Report", header_style))
            story.append(Spacer(1, 0.15*inch))
            
            # ========== TITLE ==========
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=26,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=20,
                alignment=1,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph('COURSE STATISTICS REPORT', title_style))
            
            # ========== REPORT INFO ==========
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#666666'),
                alignment=1,
                spaceAfter=12
            )
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", info_style))
            story.append(Paragraph(f"Total Courses: {len(stats)}", info_style))
            story.append(Spacer(1, 0.15*inch))
            
            # ========== STATISTICS TABLE ==========
            table_data = [['Code', 'Course Name', 'Students', 'Grades', 'Avg Grade', 'Highest', 'Lowest']]
            
            for row in stats:
                table_data.append([
                    str(row[0]),
                    str(row[1])[:26],
                    str(int(row[2] or 0)),
                    str(int(row[3] or 0)),
                    f"{float(row[4] or 0):.2f}",
                    f"{float(row[5] or 0):.2f}",
                    f"{float(row[6] or 0):.2f}"
                ])
            
            table = Table(table_data, colWidths=[0.9*inch, 2.2*inch, 0.9*inch, 0.85*inch, 1*inch, 0.95*inch, 0.85*inch])
            table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                # Data rows
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#fafafa')),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('ALIGNMENT', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1.2, colors.HexColor('#1f4788')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#ffffff'), colors.HexColor('#f0f7ff')])
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.25*inch))
            
            # ========== SUMMARY STATISTICS ==========
            total_students = sum([int(s[2] or 0) for s in stats])
            total_grades = sum([int(s[3] or 0) for s in stats])
            overall_avg = sum([float(s[4] or 0) for s in stats]) / len([s for s in stats if s[4]]) if any(s[4] for s in stats) else 0
            highest_overall = max([float(s[5] or 0) for s in stats]) if stats else 0
            lowest_overall = min([float(s[6] or 0) for s in stats if s[6]]) if any(s[6] for s in stats) else 0
            
            summary_header = ParagraphStyle(
                'SummaryHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph('Overall Statistics', summary_header))
            
            summary_data = [
                ['Total Students:', str(total_students), 'Total Grades:', str(total_grades)],
                ['Overall Average:', f'{overall_avg:.2f}', 'Class High/Low:', f'{highest_overall:.2f} / {lowest_overall:.2f}']
            ]
            
            summary_table = Table(summary_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.whitesmoke)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.3*inch))
            
            # ========== FOOTER ==========
            footer_style = ParagraphStyle(
                'FooterStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=1
            )
            story.append(Paragraph("This report provides statistical analysis of course performance and enrollment data.", footer_style))
            story.append(Paragraph(f"Report ID: {filename.split('.')[0]}", footer_style))
            
            # Build PDF
            doc.build(story)
            
            return True, f"Course statistics PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"
    
    @classmethod
    def generate_top_students_pdf(cls, limit=10):
        """Generate top students by GPA as PDF with professional styling"""
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
            
            # Create PDF with margins
            doc = SimpleDocTemplate(filepath, pagesize=letter,
                                   leftMargin=0.5*inch, rightMargin=0.5*inch,
                                   topMargin=0.75*inch, bottomMargin=0.75*inch)
            story = []
            styles = getSampleStyleSheet()
            
            # ========== HEADER ==========
            header_style = ParagraphStyle(
                'HeaderStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#666666'),
                alignment=1,
                spaceAfter=3
            )
            story.append(Paragraph("Student Records Management System", header_style))
            story.append(Paragraph("Academic Excellence Recognition Report", header_style))
            story.append(Spacer(1, 0.15*inch))
            
            # ========== TITLE ==========
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=26,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=20,
                alignment=1,
                fontName='Helvetica-Bold'
            )
            story.append(Paragraph(f'TOP {limit} STUDENTS BY GPA', title_style))
            
            # ========== REPORT INFO ==========
            info_style = ParagraphStyle(
                'InfoStyle',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.HexColor('#666666'),
                alignment=1,
                spaceAfter=12
            )
            story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", info_style))
            story.append(Paragraph("Academic Performance Recognition List", info_style))
            story.append(Spacer(1, 0.15*inch))
            
            # ========== STUDENTS TABLE ==========
            table_data = [['Rank', 'Student #', 'First Name', 'Last Name', 'GPA', 'Grades']]
            
            for row in students:
                rank_medal = "🥇" if row[0] == 1 else "🥈" if row[0] == 2 else "🥉" if row[0] == 3 else ""
                table_data.append([
                    f"{row[0]}{rank_medal}",
                    str(row[1]),
                    str(row[2]),
                    str(row[3]),
                    f"{float(row[4]):.2f}",
                    str(row[5])
                ])
            
            table = Table(table_data, colWidths=[0.7*inch, 1*inch, 1.3*inch, 1.3*inch, 0.95*inch, 0.8*inch])
            table.setStyle(TableStyle([
                # Header
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGNMENT', (0, 0), (-1, 0), 'CENTER'),
                ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                # Data rows with alternating colors for emphasis
                ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffd700')),  # Gold for rank 1
                ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#c0c0c0')),  # Silver for rank 2
                ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#cd7f32')),  # Bronze for rank 3
                ('BACKGROUND', (0, 4), (-1, -1), colors.HexColor('#f0f7ff')), # Light blue for others
                # Styling for all data rows
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#333333')),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('ALIGNMENT', (0, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 10),
                # Grid and borders
                ('GRID', (0, 0), (-1, -1), 1.2, colors.HexColor('#1f4788')),
                # Bold text for top 3
                ('FONTNAME', (0, 1), (-1, 3), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 1), (-1, 3), 11)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 0.25*inch))
            
            # ========== ACHIEVEMENT SUMMARY ==========
            top_gpa = float(students[0][4]) if students else 0
            avg_top_gpa = sum([float(s[4]) for s in students]) / len(students) if students else 0
            
            achievement_header = ParagraphStyle(
                'AchievementHeader',
                parent=styles['Heading2'],
                fontSize=12,
                textColor=colors.HexColor('#1f4788'),
                spaceAfter=10,
                fontName='Helvetica-Bold'
            )
            
            story.append(Paragraph('Performance Summary', achievement_header))
            
            achievement_data = [
                ['Highest GPA:', f'{top_gpa:.2f}', 'Average Top {0} GPA:'.format(limit), f'{avg_top_gpa:.2f}']
            ]
            
            achievement_table = Table(achievement_data, colWidths=[1.5*inch, 1.2*inch, 2*inch, 1.2*inch])
            achievement_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#1f4788')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10)
            ]))
            
            story.append(achievement_table)
            story.append(Spacer(1, 0.3*inch))
            
            # ========== FOOTER ==========
            footer_style = ParagraphStyle(
                'FooterStyle',
                parent=styles['Normal'],
                fontSize=8,
                textColor=colors.HexColor('#999999'),
                alignment=1
            )
            story.append(Paragraph("This report recognizes academic excellence and outstanding performance.", footer_style))
            story.append(Paragraph(f"Report ID: {filename.split('.')[0]}", footer_style))
            
            # Build PDF
            doc.build(story)
            
            return True, f"Top students PDF saved to {filepath}"
        
        except Exception as e:
            return False, f"Error generating PDF: {str(e)}"

