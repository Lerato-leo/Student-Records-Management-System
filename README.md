# Student Records Management System

## Project Overview
This project is a Student Records Management System designed to manage student information, course enrollments, grades, and attendance using a relational database and Python-based ETL pipelines with an advanced CLI interface.

The project follows a phased, end-to-end data engineering approach aligned with the IBM Data Engineering Professional Certificate.

## Current Status
**Phase 8 – CLI Enhancement & PDF Export (COMPLETED ✓)** 
- Enhanced CLI with Delete operations (with confirmation prompts)
- Added Search functionality (students by name/number, records by ID)
- Implemented Pagination (5 items per page with navigation)
- Added Sorting capabilities (by student number, first name, last name)
- Integrated PDF export with ReportLab (3 report types)
- Enhanced PDF styling with professional formatting, headers, footers
- Updated documentation with new features
- All PDFs generating successfully with professional appearance

**All 8 Phases Completed** ✅

**Latest Commit:** `be9e769` (PDF Export & Documentation)

## Project Phases

### ✓ Phase 1: Schema Design
- Conceptual and logical data modeling
- Entity-Relationship Diagram (ERD) created
- Normalized schema (3NF) designed

### ✓ Phase 2: Database Setup & Table Creation
- PostgreSQL database created
- Tables created with constraints (PRIMARY KEY, FOREIGN KEY, CHECK)
- Data types and constraints enforced

### ✓ Phase 3: Sample Data Generation & ETL Pipeline
**Sample Data Generation**
- Python script generates realistic sample data using Faker
- 100 students with unique 6-digit numbers (YYYYRR format)
- 15 courses with standard academic curriculum
- 200 enrollments linking students to courses
- 400 grade records with values 0-100
- 1000 attendance records with timestamps
- All CSV files saved with comma delimiters

**ETL Pipeline (Python)**
- **Extract:** Reads all 5 CSV files using pandas
- **Transform:** 
  - Validates all required columns and data types
  - Ensures status values are lowercase (active, inactive, graduated)
  - Validates grade values (0-100 range)
  - Validates enrollment terms (1 or 2)
  - Validates grade types (test, assignment, exam)
  - Removes duplicates by unique constraints
  - Fixes academic_year format (YYYY-YYYY+1)
  - Converts attendance_date to proper timestamps
  - **Foreign Key Validation:** Ensures all referenced IDs exist in parent tables
  - Removes invalid rows to maintain referential integrity
- **Load:** 
  - Clears existing tables safely using DROP CASCADE
  - Inserts data in correct dependency order: students → courses → enrollments → grades → attendance
  - Handles errors gracefully with try/except blocks
- **Data Quality:**
  - 97 valid students inserted
  - 15 courses inserted
  - 195 valid enrollments (5 invalid removed)
  - 392 valid grades (8 invalid removed)
  - 971 valid attendance records (29 invalid removed)

### ✓ Phase 5: SQL Queries & Procedures
**Advanced SQL Development**
- Created 3 database views:
  - `vw_student_transcripts` - Student course history with grades
  - `vw_course_rosters` - Course enrollment lists
  - `vw_attendance_reports` - Attendance tracking by student
- Implemented 5 SQL functions:
  - `get_students_by_course(course_id)` - List students in a course
  - `get_course_grade_statistics(course_id)` - Grade distribution and averages
  - `get_low_attendance_students(threshold)` - Identify attendance issues
  - `get_top_students_by_gpa(limit)` - Rank students by academic performance
  - `get_enrollment_statistics()` - Overall enrollment insights
- Built 3 stored procedures with validation:
  - `add_student_enrollment()` - Enroll student with duplicate checking
  - `record_grade()` - Insert grades with 0-100 range validation
  - `mark_attendance()` - Record attendance with timestamp
- **Status:** Tested on live PostgreSQL ✓ (Commit: a0dc407)

### ✓ Phase 6: Python CLI Application
**Complete CLI Interface with 5 Modules:**

**app.py** - Menu-driven CLI (988+ lines, fully enhanced)
- Main menu: 5 submenu options
- **Student Management:** 
  - Add new student
  - Search students (by name, student number)
  - View all students (paginated, 5 per page)
  - View student details
  - Update student status
  - **Delete student** (with two-level confirmation)
  - **Sort students** (by number, first name, last name)
- **Enrollment Management:** 
  - Enroll student in course
  - View enrollments (paginated)
  - **Search enrollments** (by ID)
  - **Delete enrollment** (with confirmation)
  - View course roster
- **Grades & Attendance:** 
  - Record grade
  - View grades (paginated)
  - **Search grades** (by ID)
  - **Delete grades** (with confirmation)
  - Mark attendance
  - View attendance (paginated)
- **Reports Menu (9 options):**
  - View student transcript
  - Course grade statistics
  - Enrollment statistics
  - Top students by GPA
  - Low attendance report
  - Export all reports to CSV
  - **✨ Student Transcript as PDF (NEW)**
  - **✨ Course Statistics as PDF (NEW)**
  - **✨ Top Students as PDF (NEW)**
- Help system with comprehensive user guide

**operations.py** - Business logic layer (300+ lines)
- StudentOperations: CRUD operations for students, Search, Pagination, Sorting, Delete
- CourseOperations: Course retrieval
- EnrollmentOperations: Enrollment management, Search, Delete
- GradeOperations: Grade recording, Search, Delete
- AttendanceOperations: Attendance tracking, Pagination
- ReportOperations: Analytics and reporting functions

**report_generator.py** - Report generation (750+ lines)
- **CSV Export:**
  - export_all_reports() - Generates 5 CSV files
  - export_student_transcript_csv(student_id) - Individual transcripts
- **PDF Export with Professional Styling:**
  - generate_student_transcript_pdf(student_id)
    * Institution header with report title
    * Student information box
    * Course transcript table with grades
    * Academic summary (GPA, course count)
    * Professional footer with generation details
    * Styling: Dark blue headers, alternating row colors, proper formatting
  - generate_course_statistics_pdf()
    * Course performance table (Code, Name, Enrollments, Statistics)
    * Overall statistics summary
    * Professional formatting with headers and footers
    * Statistics on total students, grades, averages
  - generate_top_students_pdf(limit)
    * Ranked student list by GPA
    * Medal awards (🥇🥈🥉) for top 3
    * Performance summary
    * Color-coded rankings
    * Professional layout with achievement header

### ✓ Phase 7: Testing & Deployment
- Comprehensive test suite: 75 unit tests (all PASSING)
- Deployment guides written for Render and Railway
- Python dependencies documented in requirements.txt
- Production-ready codebase with full documentation

### ✓ Phase 8: CLI Enhancement & PDF Export
- **CRUD Operations Enhanced:**
  - ✅ Create (Add) - Working for all entities
  - ✅ Read (View/Search) - Paginated with search functionality
  - ✅ Update - Modify student/enrollment status
  - ✅ Delete - With two-level confirmation prompts
- **Search Functionality:**
  - Students: By name or student number
  - Enrollments/Grades: By ID with pagination
- **Pagination System:**
  - 5 items per page
  - Next/Previous navigation
  - Current page display
  - Works across all list views
- **Sorting Capabilities:**
  - Students: By student number, first name, last name
  - Ascending/Descending order
- **PDF Export with ReportLab:**
  - Professional styling with headers and footers
  - Formatted tables with color-coded rows
  - Institution information and metadata
  - Generation timestamps and report IDs
  - 3 report types: Transcripts, Statistics, Rankings


**validators.py** - Input validation (200+ lines)
- 12 validator classes with 50+ validation methods
- Student number (YYYYRR), email, name, date, DOB (18+)
- Academic year (YYYY-YYYY), term (1-2), grade type, grade value (0-100)
- Attendance status, student status, integer range validation

**database.py** - Connection management
- DatabaseConnection singleton class
- SQLAlchemy engine pooling
- Query execution methods with transaction support

**report_generator.py** - Report generation (750+ lines)
- CSV export for all report types
- PDF export with professional ReportLab styling
- Automated report generation to `/reports` directory

**Status:** Fully functional and tested ✓ (Commit: 7f435a6)

### ✓ Phase 7: Testing & Deployment
**Comprehensive Test Suite (75 Tests - ALL PASSING ✅)**

**test_validators.py (53 unit tests)**
- Student number format (YYYYRR validation)
- Email validation (RFC standard)
- Name validation (2-50 chars, letters only)
- Date & date_of_birth validation
- Academic year format (YYYY-YYYY)
- Term validation (1 or 2)
- Grade type validation (test, assignment, exam)
- Grade value validation (0-100 range)
- Attendance status validation (present, absent, late)
- Student status validation (active, inactive, graduated)
- Integer range validation with bounds

**test_data_quality.py (22 data quality tests)**
- UNIQUE constraints (student_number, course_code, enrollment composite)
- NOT NULL constraints enforcement
- CHECK constraints (status values, grade ranges, term values)
- FOREIGN KEY constraint validation
- Data type constraints (INT, DATE, TIMESTAMP)
- Format constraints (academic_year YYYY-YYYY, student_number YYYYRR)

**Documentation & Deployment Guides**
- **DEPLOYMENT_GUIDE.md** (500+ lines) - Step-by-step cloud deployment
  - Render PostgreSQL setup option
  - Railway deployment alternative
  - Environment variable configuration
  - Security best practices
  - Database backup procedures
  - Monitoring & maintenance
  - Troubleshooting guide
  - Deployment checklist
- **TESTING_REPORT.md** (400+ lines) - Comprehensive test results
  - Test coverage summary (60 total tests)
  - Test execution guide with pytest commands
  - Integration test results
  - Constraint validation summary
  - Deployment readiness checklist
  - Performance notes & recommendations
- **requirements.txt** - Python dependencies
  - SQLAlchemy 2.0.23 (ORM)
  - psycopg2-binary 2.9.9 (PostgreSQL driver)
  - Faker 20.1.0 (data generation)
  - pandas 2.1.3 (data processing)
  - pytest 9.0.2 (testing framework)
  - ReportLab 4.4.9 (PDF generation)

- **Status:** All tests passing, ready for production deployment ✓ (Commit: 5ef02dd)

### ✓ Phase 8: CLI Enhancement & PDF Export
**Advanced CLI Features**
- **CRUD Operations:** Complete Create, Read (Search), Update, Delete with confirmations
- **Pagination:** 5 items per page with next/previous navigation
- **Search:** Students by name/number, records by ID
- **Sorting:** Multiple sort options for students
- **PDF Export:** 3 professional report types with ReportLab styling
- **Features:** Confirmation prompts, navigation menus, user-friendly error handling

**PDF Export Capabilities**
- Student Transcript PDF: Personal records with GPA calculation
- Course Statistics PDF: Department-level performance metrics
- Top Students PDF: Academic achievement ranking with color-coded display
- All PDFs include: Headers, footers, timestamps, report IDs
- Professional styling with: Dark blue (#1f4788) headers, alternating row colors, proper spacing

- **Status:** Enhanced CLI fully functional, PDF export tested ✓ (Commit: be9e769)

## Repository Structure

### Documentation Files
- **README.md** - Project overview, features, and quick start guide
- **REFLECTIONS.md** - Learning insights and project retrospective
- **TESTING_REPORT.md** - Comprehensive test suite documentation and results
- **TECHNICAL_REPORT_CONDENSED.md** - Technical architecture and implementation details

### Python Files (`python/` directory)
**CLI Application:**
- `app.py` - Complete CLI application (2300+ lines) with:
  - DatabaseConnection: Singleton database connection manager
  - StudentOperations, CourseOperations, EnrollmentOperations, GradeOperations, AttendanceOperations, ReportOperations
  - ReportGenerator: CSV and PDF report generation with audit compliance
  - StudentRecordsApp: Main CLI interface with CRUD, search, pagination, sorting
  - PaginationManager: Pagination system for large datasets
- `validators.py` - Input validation module (160+ lines) with:
  - Validators class with 15+ validation methods
  - Validates: student numbers, emails, names, dates, academic years, terms, grades, attendance, status

**ETL Pipeline (2 files):**
- `etl_pipeline.py` - ETL pipeline for data extraction and loading
- `generate_sample_data.py` - Sample data generation using Faker

**Configuration (2 files):**
- `db_config.example.py` - Example database configuration template
- `db_config.py` - Database credentials (not pushed to GitHub)

**Test Suite (2 files):**
- `test_validators.py` - 53 unit tests for validation logic
- `test_data_quality.py` - 22 data quality constraint tests

### SQL Files (`sql/` directory)
- `Creating tables.sql` - Database schema creation (5 normalized tables)
- `queries_and_procedures.sql` - Views, functions, and stored procedures

### Data Files (`data/` directory)
- `students.csv` - Student records
- `courses.csv` - Course catalog
- `enrollments.csv` - Student-course enrollment data
- `grades.csv` - Grade records
- `attendance.csv` - Attendance tracking records

### Local Documentation (Not Pushed)
Files kept locally in parent directory for reference:
- DELIVERABLES_COMPLETE.md
- ENHANCEMENTS_COMPLETE.md
- ERD_DIAGRAM.md
- PRESENTATION_OUTLINE.md
- README_SUBMISSION.md
- SUBMISSION_CHECKLIST.md
- SUBMISSION_SUMMARY.md

## Tech Stack
- **Database:** PostgreSQL 12+ (16+ recommended)
- **Backend/ETL:** Python 3.8+ (tested with 3.11.9)
- **ORM:** SQLAlchemy 2.0
- **PDF Generation:** ReportLab 4.4.9
- **Testing:** pytest 7.4+
- **Data Generation:** Faker 20.1
- **Data Processing:** pandas 2.1
- **Version Control:** Git/GitHub
- **Deployment:** Render or Railway (cloud PostgreSQL)

## Database Design
The database is designed using a normalized schema (3NF) with the following core entities:
- **Students** - Student profiles with unique student numbers
- **Courses** - Course catalog with course codes
- **Enrollments** - Student-course relationships by academic year/term
- **Grades** - Grade records with type validation (test/assignment/exam)
- **Attendance** - Attendance tracking with timestamps

Entity relationships are enforced using:
- **Primary Keys:** Unique identification for each entity
- **Foreign Keys:** Referential integrity constraints
- **Check Constraints:** Status/value validation
- **Unique Constraints:** No duplicate enrollments, student numbers, course codes
- **NOT NULL Constraints:** Required fields enforcement

## Features Overview

### 🎓 Student Management
- ➕ Add new students with validation
- 🔍 Search students by name or number
- 📋 View paginated student list
- 👤 View detailed student information
- ✏️ Update student status (active/inactive/graduated)
- 🗑️ Delete students (with confirmation)
- 📊 Sort students by various criteria

### 📚 Course & Enrollment Management
- View course catalog
- 📝 Enroll students in courses
- 👥 View course rosters (paginated)
- 🔍 Search enrollments by ID
- 🗑️ Delete enrollments (with confirmation)

### 📈 Grades & Attendance Tracking
- ➕ Record student grades
- 📊 View grade history (paginated)
- 🔍 Search grades by ID
- ✅ Mark student attendance
- 📅 View attendance records (paginated)

### 📑 Reporting & Export
- 📄 View student transcripts
- 📊 Course grade statistics
- 📈 Enrollment statistics
- ⭐ Top students by GPA
- 📉 Low attendance alerts
- 💾 Export reports to CSV
- **📕 Export student transcripts as PDF**
- **📗 Export course statistics as PDF**
- **📘 Export top students rankings as PDF**

## Quick Start

### Prerequisites
- Python 3.8+ (tested with 3.11.9)
- PostgreSQL 12+ (or use Render/Railway cloud database)
- pip package manager

### Installation
```bash
# Clone the repository
git clone https://github.com/Lerato-leo/Student-Records-Management-System.git
cd Student-Records-Management-System

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database connection
cp python/db_config.example.py python/db_config.py
# Edit db_config.py with your database credentials

# Initialize database
# Run sql/Creating tables.sql in your PostgreSQL client

# Generate sample data
python python/generate_sample_data.py
python python/etl_pipeline.py

# Run database setup (create views and procedures)
# Execute sql/queries_and_procedures.sql in your PostgreSQL client

# Launch CLI application
python python/app.py
```

### Running the CLI
```bash
# Start the application (from python directory)
cd python
python app.py

# Main Menu Options:
# 1 - Student Management
# 2 - Enrollment Management  
# 3 - Grades & Attendance
# 4 - Reports
# 5 - Help & Documentation
# 0 - Exit
```

### Running Tests
```bash
# Run all tests (75 total)
pytest python/test_validators.py python/test_data_quality.py -v

# Run specific test file
pytest python/test_validators.py -v

# Run with coverage report
pytest python/test_*.py --cov=python --cov-report=html
```

### Cloud Deployment
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for step-by-step instructions:
- **Option 1:** Deploy to Render (recommended for PostgreSQL)
- **Option 2:** Deploy to Railway (alternative platform)

## Project Phases Summary

| Phase | Objective | Status | Lines of Code |
|-------|-----------|--------|------------------|
| 1 | Requirements & Schema Design | ✅ Complete | - |
| 2 | Database Setup & Tables | ✅ Complete | 200 SQL |
| 3 | Sample Data Generation & ETL | ✅ Complete | 600 Python |
| 4 | Data Quality Validation | ✅ Complete | 500 Python |
| 5 | SQL Queries & Procedures | ✅ Complete | 352 SQL |
| 6 | Python CLI Application | ✅ Complete | 1400 Python |
| 7 | Testing & Deployment | ✅ Complete | 500+ Python + Docs |
| 8 | CLI Enhancement & PDF Export | ✅ Complete | 800+ Python |

## Learning Objectives Achieved
✅ Design and implement a normalized relational database schema (3NF)  
✅ Build reliable ETL pipelines with error handling and data quality checks  
✅ Write efficient advanced SQL queries (views, functions, procedures)  
✅ Apply comprehensive data validation and testing practices (75 tests)  
✅ Deploy and document a complete data engineering solution  
✅ Create production-ready Python application with modular architecture  
✅ Implement security best practices (environment variables, credentials management)  
✅ Build advanced CLI with CRUD operations, search, pagination, and sorting  
✅ Generate professional PDF reports with ReportLab  
✅ Enhance user experience with confirmation prompts and intuitive navigation  

## Project Links
- **GitHub Repository:** https://github.com/Lerato-leo/Student-Records-Management-System
- **Deployment Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Testing Report:** [TESTING_REPORT.md](TESTING_REPORT.md)
- **Project Verification:** [PROJECT_VERIFICATION_REPORT.md](PROJECT_VERIFICATION_REPORT.md)
- **Reflections:** [REFLECTIONS.md](REFLECTIONS.md)
- **CLI Quick Start:** [CLI_QUICK_START.md](CLI_QUICK_START.md)
- **PDF Export Guide:** [PDF_EXPORT_GUIDE.md](PDF_EXPORT_GUIDE.md)

## Author & License
**Lerato Matamela** - IBM Data Engineering Professional Certificate  
License: MIT
