# Student Records Management System

## Project Overview
This project is a Student Records Management System designed to manage student information, course enrollments, grades, and attendance using a relational database and Python-based ETL pipelines.

The project follows a phased, end-to-end data engineering approach aligned with the IBM Data Engineering Professional Certificate.

## Current Status
**Phase 7 – Testing & Deployment (COMPLETED ✓)** 
- Comprehensive test suite created: 75 unit tests (all PASSING)
- Deployment guides written for Render and Railway
- Python dependencies documented in requirements.txt
- Production-ready codebase with full documentation

**All 7 Phases Completed** ✅

**Latest Commit:** `5ef02dd` (Phase 7: Testing & Deployment)

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

**app.py** - Menu-driven CLI (600+ lines)
- Main menu: 5 submenu options
- Student Management: Add, view all, view details, update status
- Enrollment Management: Enroll students, view rosters
- Grades & Attendance: Record grades, mark attendance, view records
- Reports: 5 report types (transcript, statistics, enrollment, low attendance, top students)
- Help system with comprehensive user guide

**operations.py** - Business logic layer (300+ lines)
- StudentOperations: CRUD operations for students
- CourseOperations: Course retrieval
- EnrollmentOperations: Enrollment management via stored procedure
- GradeOperations: Grade recording and transcript generation
- AttendanceOperations: Attendance tracking
- ReportOperations: Analytics and reporting functions

**validators.py** - Input validation (200+ lines)
- 12 validator classes with 50+ validation methods
- Student number (YYYYRR), email, name, date, DOB (18+)
- Academic year (YYYY-YYYY), term (1-2), grade type, grade value (0-100)
- Attendance status, student status, integer range validation

**database.py** - Connection management
- DatabaseConnection singleton class
- SQLAlchemy engine pooling
- Query execution methods with transaction support

**report_generator.py** - CSV report generation
- 5 report formats: transcripts, statistics, enrollment, low attendance, top students
- Automated report generation to `/reports` directory

- **Status:** Fully functional and tested ✓ (Commit: 7f435a6)

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

- **Status:** All tests passing, ready for production deployment ✓ (Commit: 5ef02dd)

## Tech Stack
- **Database:** PostgreSQL 12+
- **Backend/ETL:** Python 3.8+ (tested with 3.11.9)
- **ORM:** SQLAlchemy 2.0
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

# Launch CLI application
python python/app.py
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

## Learning Objectives Achieved
✅ Design and implement a normalized relational database schema (3NF)  
✅ Build reliable ETL pipelines with error handling and data quality checks  
✅ Write efficient advanced SQL queries (views, functions, procedures)  
✅ Apply comprehensive data validation and testing practices (75 tests)  
✅ Deploy and document a complete data engineering solution  
✅ Create production-ready Python application with modular architecture  
✅ Implement security best practices (environment variables, credentials management)  

## Project Links
- **GitHub Repository:** https://github.com/Lerato-leo/Student-Records-Management-System
- **Deployment Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Testing Report:** [TESTING_REPORT.md](TESTING_REPORT.md)
- **Project Verification:** [PROJECT_VERIFICATION_REPORT.md](PROJECT_VERIFICATION_REPORT.md)
- **Reflections:** [REFLECTIONS.md](REFLECTIONS.md)

## Author & License
**Lerato Matamela** - IBM Data Engineering Professional Certificate  
License: MIT
