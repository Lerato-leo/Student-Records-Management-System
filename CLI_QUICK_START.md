# Enhanced CLI Quick Start Guide

## Running the Application

### From Project Root
```bash
cd Student-Records-Management-System
python python/app.py
```

### Features Available Now

## 🎓 STUDENT MANAGEMENT
**Menu Option: 1**

### Add New Student
- Entry fields: Student Number, First Name, Last Name, DOB (YYYY-MM-DD), Email
- Validates all inputs before inserting
- Returns confirmation with new Student ID

### Search Students ⭐ NEW
- Search by name or student number
- Case-insensitive name matching
- Displays matching results in table format

### View All Students (Paginated) ⭐ NEW
- Browse students 5 per page
- Navigation: `n` = Next | `p` = Previous | `q` = Quit
- Shows: ID, Number, Name, DOB, Email, Status

### View Student Details
- Enter Student ID
- Shows complete profile
- All fields displayed clearly

### Update Student Status
- Change status to: active, inactive, graduated
- Useful for marking students as graduated or inactive

### Delete Student ⭐ NEW with CONFIRMATION
- Two-level confirmation before deletion
- Safety warning displayed
- Performs soft delete (marks as inactive)

### Sort Students ⭐ NEW
- Sort by Student Number (Ascending/Descending)
- Sort by First Name (A-Z)
- Sort by Last Name (A-Z)

---

## 📚 ENROLLMENT MANAGEMENT
**Menu Option: 2**

### Add Student to Course
- Enter: Student ID, Course ID, Academic Year, Term
- Creates enrollment record with today's date

### View All Enrollments (Paginated) ⭐ NEW
- Browse all enrollments 5 per page
- Shows: Enrollment ID, Student ID, Course ID, Year, Term, Date
- Navigation available

### Search Enrollments ⭐ NEW
- Search by Student ID or Course ID
- Displays matching enrollment records

### Delete Enrollment ⭐ NEW with CONFIRMATION
- Remove enrollment with safety confirmation
- Hard delete (actual record removal)

### View Course Roster ⭐ NEW
- Shows students enrolled in each course
- Uses vw_course_rosters view
- Displays attendance counts

---

## 📊 GRADES & ATTENDANCE
**Menu Option: 3**

### Add Grade
- Enter: Enrollment ID, Grade Type (test/assignment/exam), Grade Value (0-100)
- Validates grade range
- Records today's date

### View Grades (Paginated) ⭐ NEW
- Browse all grades 5 per page
- Shows: Grade ID, Enrollment ID, Type, Value, Date
- Sortable and searchable

### Search Grades ⭐ NEW
- Find grades by Enrollment ID
- Displays all grades for that enrollment

### Delete Grade ⭐ NEW with CONFIRMATION
- Remove grade record with confirmation
- Useful for correcting data entry errors

### Mark Attendance
- Enter: Enrollment ID, Status (present/absent/late)
- Records attendance for today

### View Attendance Report ⭐ NEW
- Shows attendance statistics from vw_attendance_reports view
- Displays: Student name, course, total classes, present/absent counts

---

## 📈 REPORTS
**Menu Option: 4**

### Student Transcript ⭐ Using Database View
- Enter Student ID
- Shows all enrollments with average grades per course
- Source: `vw_student_transcripts` view
- Display: Student info, course code/name, academic year, term, average grade

### Course Grade Statistics
- Shows all courses with statistics
- Displays: Course code, name, student count, grade count, average grade

### Enrollment Statistics
- Shows enrollment counts by course
- Displays: Course code, name, total enrollments, unique students

### Top Students by GPA ⭐ RANKED
- Displays students ranked by GPA
- Shows: Rank, Student Number, Name, GPA, Total Grades
- Limited to Top 10

### Low Attendance Report ⭐ FILTERED
- Shows students with less than 75% attendance
- Displays: Student name, course, total classes, present count, percentage
- Helps identify at-risk students

### Export All Reports to CSV
- Generates all reports to `/reports/` directory
- Files timestamped for version tracking
- Include all available data

---

## ❓ HELP & NAVIGATION
**Menu Option: 5**

Shows complete feature overview and keyboard navigation tips

---

## 🎮 KEYBOARD NAVIGATION

### Main Menu
- `1` - Student Management
- `2` - Enrollment Management
- `3` - Grades & Attendance
- `4` - Reports
- `5` - Help
- `0` - Exit

### Pagination (when enabled)
- `p` - Previous page
- `n` - Next page
- `q` - Quit/Return to menu

### Confirmations
- `yes` or `y` - Confirm action
- `no` or `n` - Cancel action

---

## 💾 DATA FEATURES

### Search Functionality
- **Students**: Search by first/last name or student number
- **Enrollments**: Search by Student ID or Course ID
- **Grades**: Search by Enrollment ID
- All searches are case-insensitive

### Pagination
- All list views support pagination
- Default: 5 items per page
- Page info shows: "Page X/Y (total items)"

### Sorting
- **Students only**: Sort by number, first name, or last name
- Supports ascending/descending for numbers

### Delete Operations (Safety-First)
- **Students**: Two-level confirmation + soft delete (status → inactive)
- **Enrollments**: One-level confirmation + hard delete
- **Grades**: One-level confirmation + hard delete

---

## ⚠️ IMPORTANT NOTES

### Data Integrity
- Student deletions are soft deletes (status = inactive)
- This prevents breaking enrollment references
- Soft-deleted students will not appear in reports

### Required Fields
- All date fields use format: YYYY-MM-DD
- Email requires valid format (user@domain.com)
- Grade values must be 0-100

### Performance
- Large datasets (>100 enrollments) display in pages
- Search queries are optimized for speed
- Database views materialized for report queries

---

## 🔍 EXAMPLE WORKFLOWS

### Workflow 1: Add a Student and Enroll in Course
1. Main Menu → 1 (Student Management)
2. Add New Student
3. Save returned Student ID (e.g., 42)
4. Main Menu → 2 (Enrollment Management)
5. Add Student to Course
6. Use Student ID 42 and select Course ID

### Workflow 2: Record Grades for a Student
1. Main Menu → 3 (Grades & Attendance)
2. Add Grade (enter enrollment ID, grade type, value)
3. Repeat for multiple grades
4. View Grades (Paginated) to verify
5. Main Menu → 4 (Reports) → Student Transcript to see average

### Workflow 3: Find Low Attendance Students
1. Main Menu → 4 (Reports)
2. Select "Low Attendance Report"
3. View students with <75% attendance
4. Take action (mark absent, contact student, etc.)

### Workflow 4: Generate Report Export
1. Main Menu → 4 (Reports)
2. Select "Export All Reports to CSV"
3. Reports generated to `reports/` directory
4. Open in Excel or spreadsheet application

---

## 🆘 TROUBLESHOOTING

### "Cannot connect to PostgreSQL database"
- Ensure PostgreSQL is running
- Check `python/db_config.py` has correct credentials
- Verify database `student_records_db` exists

### "No transcript data found"
- Student may have no enrollments
- Views must be created (run `python setup_database.py`)
- Check student status is "active"

### "Invalid date format"
- Use YYYY-MM-DD format
- Example: 2025-01-22 (not 01/22/2025)

### "Grade must be between 0 and 100"
- Check grade value is integer
- Value must be inclusive 0-100

### Pagination not showing "Next/Previous"
- Only available if more than 5 items
- Single page displays "n/a" for unavailable options

---

## 📝 TIPS & BEST PRACTICES

1. **Use Search Before Delete**: Search for student before deleting to confirm correct person
2. **Verify Data Before Export**: Review reports on screen before exporting to CSV
3. **Check Status**: Use "View Student Details" to verify status before operations
4. **Batch Operations**: Mark attendance for multiple students efficiently
5. **Regular Backups**: Export reports periodically for backup

---

## 🚀 NEXT STEPS

1. Populate database with student data (already done with sample data)
2. Enroll students in courses
3. Record grades as term progresses
4. Track attendance
5. Generate reports for academic review
6. Export data for end-of-term reports
