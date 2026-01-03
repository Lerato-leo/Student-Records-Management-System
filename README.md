# Student Records Management System

## Project Overview
This project is a Student Records Management System designed to manage student information, course enrollments, grades, and attendance using a relational database and Python-based ETL pipelines.

The project follows a phased, end-to-end data engineering approach aligned with the IBM Data Engineering Professional Certificate.

## Current Status
**Phase 2 – Database Setup & Table Creation (In Progress)**  
- ERD designed and finalized  
- PostgreSQL installed and configured  
- Database schema planning completed  
- Table creation and constraints underway  

## Core Features (Planned)
- Normalized relational database (3NF)
- Student, course, enrollment, grade, and attendance management
- Python ETL pipelines for loading and transforming data
- Data validation and quality checks
- Advanced SQL queries, views, and stored procedures
- CLI-based application for interacting with the system
- Cloud deployment with secure credentials

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

## Project Structure (Planned)
student-records-system/
- sql/
  - schema.sql
  - queries.sql
  - procedures.sql
- etl/
  - extract.py
  - transform.py
  - load.py
- cli/
  - app.py
- data/
  - sample_data/
- docs/
  - ERD.png
- README.md

## Learning Objectives
- Design and implement a relational database schema
- Build reliable ETL pipelines
- Write efficient and advanced SQL queries
- Apply data validation and testing practices
- Deploy and document a complete data engineering solution

## Author
Lerato Matamela
