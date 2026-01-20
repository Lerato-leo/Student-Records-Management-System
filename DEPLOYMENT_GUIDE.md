"""
Deployment Guide - Phase 7
Instructions for deploying the Student Records Management System to the cloud
"""

# ============================================================================
# DEPLOYMENT GUIDE: Student Records Management System
# ============================================================================

## Option 1: Deploy to Render (Recommended for PostgreSQL)

### Prerequisites:
- GitHub account with repository pushed
- Render.com account (https://render.com)

### Step 1: Create PostgreSQL Database on Render

1. Login to Render.com
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - Name: `student-records-db`
   - Database: `student_records_db`
   - User: `student_user` (or choose)
   - Region: Choose closest to you
4. Click "Create Database"
5. Wait for database to be created (5-10 minutes)
6. Copy the "External Database URL" from the dashboard

### Step 2: Initialize Database Schema

1. Connect to the Render PostgreSQL database using the external URL:
   ```powershell
   psql [YOUR_EXTERNAL_DATABASE_URL]
   ```

2. Run the schema creation script:
   ```sql
   -- Execute contents of: sql/Creating tables.sql
   ```

3. Run the ETL pipeline to load sample data:
   ```powershell
   cd python
   python etl_pipeline.py
   ```
   
   Update `db_config.py` with Render database credentials first:
   ```python
   DB_HOST = 'your-render-host.c.db.onrender.com'
   DB_PORT = 5432
   DB_NAME = 'student_records_db'
   DB_USER = 'student_user'
   DB_PASSWORD = 'your_password'
   ```

4. Create stored procedures and views:
   ```sql
   -- Execute contents of: sql/queries_and_procedures.sql
   ```

### Step 3: Deploy Python Application

Option A: Deploy as Web Service
1. In Render, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `python python/app.py`
5. Set environment variables:
   - `DB_HOST`: Your Render database host
   - `DB_PORT`: 5432
   - `DB_NAME`: student_records_db
   - `DB_USER`: student_user
   - `DB_PASSWORD`: Your password
6. Click "Create Web Service"

Option B: Keep CLI Local
- Just deploy the database to Render
- Update local `db_config.py` to connect to Render
- Run CLI locally: `python app.py`

### Step 4: Verify Deployment

1. Test database connection:
   ```python
   from database import DatabaseConnection
   
   if DatabaseConnection.test_connection():
       print("✅ Connected to cloud database")
   ```

2. Run sample CLI operations:
   ```powershell
   python app.py
   # Test: View students, enrollments, generate reports
   ```

---

## Option 2: Deploy to Railway

### Prerequisites:
- Railway.app account (https://railway.app)
- GitHub account

### Step 1: Create PostgreSQL on Railway

1. Login to Railway
2. Create new project → PostgreSQL
3. Wait for database provisioning
4. Click on PostgreSQL service
5. Copy "Database URL" from Connect tab

### Step 2: Configure Local Environment

Create `.env` file in project root:
```
DB_HOST=your-railway-host
DB_PORT=5432
DB_NAME=student_records_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### Step 3: Initialize Database

Same as Render (Step 2 above)

### Step 4: Deploy Application

1. In Railway, create new service → GitHub repo
2. Select: `Student-Records-Management-System`
3. Set environment variables from `.env`
4. Railway auto-detects Python and runs `python app.py`

---

## Environment Variables (Recommended)

Never hardcode credentials! Use environment variables:

### Create `.env` file:
```
DB_HOST=your-host.com
DB_PORT=5432
DB_NAME=student_records_db
DB_USER=student_user
DB_PASSWORD=your_password
```

### Update `db_config.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 5432))
DB_NAME = os.getenv('DB_NAME', 'student_records_db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
```

### Install python-dotenv:
```powershell
pip install python-dotenv
```

---

## Security Best Practices

1. **Never commit credentials**:
   ```
   # Add to .gitignore
   .env
   db_config.py
   db_config.*.py
   ```

2. **Use strong passwords**:
   - Minimum 16 characters
   - Mix upper/lowercase, numbers, special chars

3. **Enable SSL connections**:
   - Render/Railway provide SSL by default
   - Always use encrypted connections

4. **Regular backups**:
   - Render: Automatic daily backups
   - Railway: Configure backup schedule
   - Export backups to GitHub/cloud storage

5. **Limit database access**:
   - Only allow connections from authorized apps
   - Use database-specific users (not admin)
   - Use IP whitelisting if available

---

## Database Backups

### Export Database Locally:
```powershell
# Create backup
pg_dump "postgresql://user:password@host:5432/student_records_db" > backup.sql

# Restore from backup
psql "postgresql://user:password@host:5432/student_records_db" < backup.sql
```

### Schedule Regular Backups:
- Render: Automatic (check dashboard)
- Railway: Use pg_dump with cron job
- Store backups in GitHub/S3/Google Drive

---

## Monitoring & Maintenance

### Monitor Database Performance:
```sql
-- Check database size
SELECT pg_size_pretty(pg_database_size('student_records_db'));

-- List active connections
SELECT * FROM pg_stat_activity;

-- Check slow queries (if enabled)
SELECT query, mean_time FROM pg_stat_statements ORDER BY mean_time DESC;
```

### Monitor Application Logs:
- Render: Logs tab in dashboard
- Railway: Logs tab in service
- Look for errors in `operations.py` and database connections

---

## Scaling Considerations

### If Performance Degrades:

1. **Add Indexes** (Phase 2 enhancement):
   ```sql
   CREATE INDEX idx_student_status ON students(status);
   CREATE INDEX idx_enrollment_student ON enrollments(student_id);
   CREATE INDEX idx_grades_enrollment ON grades(enrollment_id);
   ```

2. **Upgrade Database Plan**:
   - Render: Upgrade to paid plan for more CPU/RAM
   - Railway: Increase resource allocation

3. **Cache Query Results**:
   - Implement Redis caching for reports
   - Cache student/course lookups

4. **Optimize Queries**:
   - Use EXPLAIN ANALYZE to find slow queries
   - Add missing indexes
   - Consider query rewriting

---

## Troubleshooting

### Cannot Connect to Database:
```
Error: could not connect to server
```

**Solution**:
- Verify DB_HOST, DB_PORT, DB_USER, DB_PASSWORD
- Check if database is running (Render/Railway dashboard)
- Verify SSL certificate (use `sslmode=require`)
- Check firewall/network access

### Stored Procedure Not Found:
```
Error: function add_student_enrollment does not exist
```

**Solution**:
- Run `sql/queries_and_procedures.sql` on cloud database
- Verify procedures were created: `\df` in psql

### Data Not Persisting:
```
Data inserted but doesn't appear after restart
```

**Solution**:
- Ensure you're writing to cloud database (not local)
- Check connection string is correct
- Verify transaction commits (`.commit()`)

---

## Deployment Checklist

- [ ] GitHub repository is public with all code
- [ ] `.gitignore` includes `.env` and `db_config.py`
- [ ] Cloud database created (Render or Railway)
- [ ] Database schema initialized
- [ ] ETL pipeline successfully loaded sample data
- [ ] Views and stored procedures created
- [ ] Application connects to cloud database
- [ ] CLI interface tested on cloud database
- [ ] Reports generate correctly
- [ ] All tests passing
- [ ] Documentation complete

---

## After Deployment

### Monitor Application:
- Check logs regularly
- Monitor database performance
- Review user feedback
- Track bug reports

### Keep Updated:
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Monitor PostgreSQL security updates
- Test backups regularly

### Scale as Needed:
- Add caching for frequently accessed data
- Implement database connection pooling
- Consider API layer (Flask/FastAPI)
- Add authentication/authorization

---

**Deployment is complete! Your Student Records Management System is now live on the cloud.** 🚀
