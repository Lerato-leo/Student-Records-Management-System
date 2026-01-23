"""
Fill Missing Grades Script
Ensures every student has grades for all assessment types (Test, Assignment, Exam)
for each course they're enrolled in
"""

import random
from datetime import datetime, timedelta
from database import DatabaseConnection

def get_missing_grade_combinations():
    """Find all enrollment-assessment type combinations that are missing"""
    query = """
    WITH assessment_types AS (
        SELECT 'test' as grade_type
        UNION ALL
        SELECT 'assignment'
        UNION ALL
        SELECT 'exam'
    ),
    enrollments_with_types AS (
        SELECT 
            e.enrollment_id,
            e.student_id,
            e.course_id,
            at.grade_type
        FROM enrollments e
        CROSS JOIN assessment_types at
    )
    SELECT 
        ewt.enrollment_id,
        ewt.student_id,
        ewt.course_id,
        ewt.grade_type
    FROM enrollments_with_types ewt
    WHERE NOT EXISTS (
        SELECT 1 FROM grades g 
        WHERE g.enrollment_id = ewt.enrollment_id 
        AND g.grade_type = ewt.grade_type
    )
    ORDER BY ewt.enrollment_id;
    """
    return DatabaseConnection.execute_query(query)

def generate_realistic_grade():
    """Generate a realistic grade value (0-100)"""
    # Weighted distribution: more grades towards middle (60-90)
    rand = random.random()
    if rand < 0.05:  # 5% very low
        return random.randint(0, 40)
    elif rand < 0.10:  # 5% low
        return random.randint(40, 60)
    elif rand < 0.80:  # 70% average to good
        return random.randint(60, 90)
    else:  # 20% excellent
        return random.randint(90, 100)

def get_enrollment_date(enrollment_id):
    """Get the enrollment date to set realistic grade dates"""
    query = f"""
    SELECT academic_year, term 
    FROM enrollments 
    WHERE enrollment_id = {enrollment_id};
    """
    result = DatabaseConnection.execute_query(query)
    if result:
        academic_year, term = result[0]
        # Parse year (e.g., "2024-2025")
        year = int(academic_year.split('-')[0])
        # Set date based on term
        if term == 1:
            return datetime(year, 3, 15)  # Mid-semester 1
        else:
            return datetime(year, 10, 15)  # Mid-semester 2
    return datetime.now()

def insert_missing_grades_batch(missing_combinations):
    """Insert missing grade records using batch SQL insert"""
    if not missing_combinations:
        print("✓ No missing grades found!")
        return 0
    
    print(f"\nInserting {len(missing_combinations)} missing grades...")
    print("-" * 60)
    
    # Create SQL for batch insert
    values_list = []
    for enrollment_id, student_id, course_id, grade_type in missing_combinations:
        grade_value = generate_realistic_grade()
        grade_date = get_enrollment_date(enrollment_id)
        grade_date = grade_date + timedelta(days=random.randint(0, 30))
        
        values_list.append(
            f"({enrollment_id}, '{grade_type}', {grade_value}, '{grade_date.strftime('%Y-%m-%d')}')"
        )
    
    try:
        # Build batch insert query
        values_str = ',\n'.join(values_list)
        query = f"""
        INSERT INTO grades (enrollment_id, grade_type, grade_value, grade_date)
        VALUES 
        {values_str}
        ON CONFLICT DO NOTHING;
        """
        
        # Execute batch insert using procedure method which commits
        DatabaseConnection.execute_procedure(query)
        print(f"✓ Successfully inserted: {len(missing_combinations)} grades")
        return len(missing_combinations)
    
    except Exception as e:
        print(f"✗ Error during batch insert: {str(e)}")
        return 0

def verify_completion():
    """Verify that all enrollments now have all 3 assessment types"""
    query = """
    SELECT 
        COUNT(*) as incomplete_enrollments
    FROM (
        SELECT 
            e.enrollment_id,
            COUNT(DISTINCT g.grade_type) as assessment_count
        FROM enrollments e
        LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
        GROUP BY e.enrollment_id
        HAVING COUNT(DISTINCT g.grade_type) < 3
    ) as incomplete;
    """
    
    result = DatabaseConnection.execute_query(query)
    if result:
        incomplete = result[0][0]
        if incomplete == 0:
            return True, 0
        return False, incomplete
    return False, -1

def generate_summary():
    """Generate summary statistics"""
    query = """
    SELECT 
        e.enrollment_id,
        s.student_number,
        c.course_code,
        COUNT(DISTINCT g.grade_type) as assessment_types,
        AVG(g.grade_value) as avg_grade,
        STRING_AGG(DISTINCT g.grade_type, ', ' ORDER BY g.grade_type) as types
    FROM enrollments e
    JOIN students s ON e.student_id = s.student_id
    JOIN courses c ON e.course_id = c.course_id
    LEFT JOIN grades g ON e.enrollment_id = g.enrollment_id
    GROUP BY e.enrollment_id, s.student_number, c.course_code
    ORDER BY s.student_number, c.course_code;
    """
    
    results = DatabaseConnection.execute_query(query)
    
    complete = sum(1 for r in results if r[3] == 3)
    total = len(results)
    
    return {
        'complete': complete,
        'total': total,
        'percentage': (complete / total * 100) if total > 0 else 0,
        'details': results
    }

def main():
    print("╔" + "═" * 58 + "╗")
    print("║  MISSING GRADES FILLER - Ensure Complete Assessment Data ║")
    print("╚" + "═" * 58 + "╝")
    print()
    
    # Step 1: Find missing grades
    print("STEP 1: Identifying Missing Grade Combinations")
    print("-" * 60)
    missing = get_missing_grade_combinations()
    print(f"✓ Found {len(missing)} missing grade records")
    print()
    
    # Step 2: Insert missing grades
    print("STEP 2: Generating and Inserting Realistic Grades")
    print("-" * 60)
    if missing:
        inserted = insert_missing_grades_batch(missing)
        if inserted == 0:
            print("✗ Failed to insert grades")
    print()
    
    # Step 3: Verify completion
    print("STEP 3: Verifying Grade Completeness")
    print("-" * 60)
    success, remaining = verify_completion()
    if success:
        print("✓ ALL ENROLLMENTS NOW HAVE COMPLETE GRADES!")
        print("✓ Every student has grades for Test, Assignment, and Exam")
    else:
        print(f"✗ Still missing: {remaining} incomplete enrollments")
    print()
    
    # Step 4: Summary
    print("STEP 4: Final Summary")
    print("-" * 60)
    summary = generate_summary()
    print(f"✓ Complete Enrollments: {summary['complete']}/{summary['total']} ({summary['percentage']:.1f}%)")
    print()
    
    print("SAMPLE OF UPDATED RECORDS:")
    print("-" * 60)
    for i, record in enumerate(summary['details'][:5]):
        enrollment_id, student_num, course_code, types, avg_grade, type_list = record
        print(f"Student {student_num} | Course {course_code}")
        print(f"  Assessment Types: {type_list}")
        print(f"  Average Grade: {float(avg_grade or 0):.2f}")
        print()
    
    print("✓ Grade filling process complete!")

if __name__ == "__main__":
    main()
