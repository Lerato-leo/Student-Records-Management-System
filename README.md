# Student Records Management System

## Project Overview
This project is a Student Records Management System designed to manage student information, course enrollments, grades, and attendance using a relational database and Python-based ETL pipelines.

The project follows a phased, end-to-end data engineering approach aligned with the IBM Data Engineering Professional Certificate.

## Current Status
**Phase 3 – Sample Data Generation & ETL Pipeline (COMPLETED ✓)**  
- Sample data generator created using Faker  
- Generated 100 students, 15 courses, 200 enrollments, 400 grades, 1000 attendance records  
- CSV files created with proper data validation  
- Python ETL pipeline implemented with Extract, Transform, Load stages  
- Data quality checks and foreign key validation completed  
- All data successfully loaded into PostgreSQL database  

**Next: Phase 4 – SQL Queries, Interface & Testing (Upcoming)**

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

### 📅 Phase 4: SQL Queries, Interface & Testing (Next)
**SQL Query Development**
- Create advanced SQL scripts to:
  - View all students in a specific course
  - Calculate course-level average grades
  - Identify students with <75% attendance
  - Rank top 10 students by GPA
  - Generate course enrollment statistics
- Build:
  - Stored procedures for enrollment, grade entry, and attendance updates
  - Views for transcripts, rosters, and attendance reports

**Python Application Interface**
- Develop a CLI-based interface to:
  - Add students and enroll in courses
  - Record grades and mark attendance
  - Generate reports (CSV/PDF using ReportLab)
  - Perform CRUD operations with input validation
  - Query student records and statistics

**Data Quality & Testing**
- Validate grade ranges, date formats, and duplicate detection
- Create test cases for:
  - Data inserts and updates
  - ETL pipeline execution
  - SQL query accuracy
  - Foreign key constraint enforcement
- Document all testing results

### 📅 Phase 5: Deployment (End Goal)
- Deploy database using Render (Free PostgreSQL) or Railway
- Update Python ETL and CLI to use cloud database credentials
- Store credentials securely in environment variables
- Push complete solution to GitHub with documentation

## Tech Stack
- **Database:** PostgreSQL  
- **Backend / ETL:** Python  
- **Data Generation:** Faker  
- **Query Language:** SQL  
- **Deployment:** Render or Railway  

## Database Design
The database is designed using a normalized schema with the following core entities:
- Students
- Courses
- Enrollments
- Grades
- Attendance  

Entity relationships are enforced using primary keys, foreign keys, and integrity constraints to ensure data accuracy and consistency.

## Project Structure
```
Student-Records-Management-System/
├── sql/
│   ├── Creating tables.sql       # Database schema and table definitions
│   └── clear_data.sql             # Script to clear existing data
├── python/
│   ├── generate_sample_data.py    # Generates realistic sample data using Faker
│   ├── etl_pipeline.py            # Extract, Transform, Load pipeline
│   └── db_config.py               # Database connection configuration
├── data/
│   ├── students.csv               # Sample student records
│   ├── courses.csv                # Course catalog
│   ├── enrollments.csv            # Student-course enrollments
│   ├── grades.csv                 # Student grades by course
│   └── attendance.csv             # Attendance records
├── docs/
│   └── ERD.png                    # Entity-Relationship Diagram
├── README.md                       # Project documentation
└── .gitignore                     # Git ignore configuration
```

**Key Files:**
- `generate_sample_data.py` - Generates 100 students, 15 courses, and related records
- `etl_pipeline.py` - Validates and loads data into PostgreSQL with error handling
- `Creating tables.sql` - Defines schema with PRIMARY KEY, FOREIGN KEY, and CHECK constraints
- CSV files - Source data files validated and loaded by the ETL pipeline

## Learning Objectives
- Design and implement a relational database schema
- Build reliable ETL pipelines
- Write efficient and advanced SQL queries
- Apply data validation and testing practices
- Deploy and document a complete data engineering solution

## Author
Lerato Matamela
