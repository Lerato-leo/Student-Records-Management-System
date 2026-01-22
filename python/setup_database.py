"""
Initialize database schema, views, functions, and procedures
Run this once to set up the database structure
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus
from db_config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def execute_sql_statements(sql_content, skip_errors=False):
    """Execute SQL statements, handling each one separately for DDL operations"""
    connection_string = f"postgresql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_string, echo=False)
    
    # Split statements by semicolon (simple but effective for most cases)
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    success_count = 0
    error_count = 0
    
    with engine.connect() as conn:
        for stmt in statements:
            if not stmt:
                continue
            
            try:
                conn.execute(text(stmt))
                conn.commit()
                success_count += 1
            except Exception as e:
                error_str = str(e).lower()
                # Skip "already exists" errors
                if "already exists" in error_str or "duplicate key" in error_str:
                    success_count += 1
                elif skip_errors:
                    error_count += 1
                    print(f"    ⚠ Skipped: {str(e)[:60]}")
                else:
                    raise
    
    engine.dispose()
    return success_count, error_count

def setup_database():
    """Create all database objects from SQL files"""
    
    print("=" * 70)
    print("Initializing Database Schema, Views, Functions & Procedures")
    print("=" * 70)
    
    try:
        # Read SQL files
        with open('../sql/Creating tables.sql', 'r') as f:
            tables_sql = f.read()
        
        with open('../sql/queries_and_procedures.sql', 'r') as f:
            procedures_sql = f.read()
        
        # Execute table creation
        print("\n[1/2] Creating tables and constraints...")
        try:
            success, errors = execute_sql_statements(tables_sql, skip_errors=True)
            print(f"  ✓ Tables processed ({success} created/existed)")
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:100]}")
            raise
        
        # Execute views and procedures
        print("\n[2/2] Creating views, functions, and procedures...")
        try:
            success, errors = execute_sql_statements(procedures_sql, skip_errors=True)
            print(f"  ✓ Views, functions, and procedures created ({success} created/existed)")
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:100]}")
            raise
        
        print("\n" + "=" * 70)
        print("✓ Database initialization complete!")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: SQL file not found: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    setup_database()
