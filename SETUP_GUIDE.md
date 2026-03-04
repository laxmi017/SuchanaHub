# SUCHANA HUB - Setup & Installation Guide
# A Smart College Attendance & Guardian Notification System
# MCA Semester Project

## 🎯 PROJECT OVERVIEW

SUCHANA HUB is a complete web application for managing college attendance:
- Multi-role login system (Admin, Teacher, Staff)
- Attendance processing from CSV/Excel biometric files
- Automatic guardian notifications
- Teacher feedback system
- Comprehensive reporting and analytics

---

## 📋 SYSTEM REQUIREMENTS

### Minimum Requirements:
- Python 3.8 or higher
- PostgreSQL 12 or higher
- 2GB RAM
- 500MB free disk space
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Recommended:
- Python 3.10+
- PostgreSQL 14+
- 4GB+ RAM
- Windows 10+ / macOS 10.14+ / Linux (any modern distribution)

---

## 🔧 INSTALLATION STEPS

### STEP 1: PREREQUISITES INSTALLATION

#### On Windows:
1. **Install Python 3.10+**
   - Download from: https://www.python.org/downloads/
   - ✓ CHECK "Add Python to PATH" during installation
   - Verify: Open CMD and type: python --version

2. **Install PostgreSQL 14+**
   - Download from: https://www.postgresql.org/download/windows/
   - Remember the password you set for 'postgres' user
   - Installation typically on port 5432

3. **Verify PostgreSQL installation:**
   ```
   psql --version
   ```

#### On macOS:
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Install PostgreSQL
brew install postgresql
brew services start postgresql
```

#### On Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
sudo apt install postgresql postgresql-contrib
```

---

### STEP 2: SET UP PROJECT DIRECTORY

On Windows (PowerShell):
```powershell
# Navigate to your project location
cd "C:\Users\di\Desktop\Suchana Hub"

# Verify all files exist
dir
```

On macOS/Linux:
```bash
cd ~/Desktop/Suchana\ Hub
ls -la
```

Expected files:
```
Suchana Hub/
├── app/
│   ├── __init__.py
│   ├── models.py
│   └── routes/
│       └── [route files]
├── templates/
│   └── [HTML files]
├── static/
│   └── style.css
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

---

### STEP 3: CREATE PYTHON VIRTUAL ENVIRONMENT

A virtual environment isolates project dependencies.

**On Windows (PowerShell):**
```powershell
# Create virtual environment named 'venv'
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

If you get an error about execution policy:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then run the Activate.ps1 again
```

**On macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

You should see `(venv)` prefix in terminal when activated.

---

### STEP 4: INSTALL PYTHON DEPENDENCIES

With virtual environment activated:

```bash
# Upgrade pip to latest version
pip install --upgrade pip

# Install all required packages from requirements.txt
pip install -r requirements.txt
```

Wait for installation to complete. This installs:
- Flask web framework
- SQLAlchemy ORM
- PostgreSQL adapter
- Data processing libraries
- And other dependencies

---

### STEP 5: CREATE PostgreSQL DATABASE

**Option A: Using pgAdmin GUI (Easier)**
1. Open pgAdmin (comes with PostgreSQL)
2. Right-click "Databases" → Create → Database
3. Name: `suchana_hub`
4. Owner: `postgres`
5. Click Save

**Option B: Using Command Line (PowerShell/Terminal)**

On Windows PowerShell:
```powershell
# Connect to PostgreSQL
psql -U postgres

# In psql prompt, execute:
CREATE DATABASE suchana_hub;
CREATE USER suchana_user WITH PASSWORD 'suchana_password';
ALTER ROLE suchana_user SET client_encoding TO 'utf8';
ALTER ROLE suchana_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE suchana_user SET default_transaction_deferrable TO on;
ALTER ROLE suchana_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE suchana_hub TO suchana_user;
\q
```

On macOS/Linux:
```bash
# Same commands, might need sudo
sudo -u postgres psql
# Then execute the SQL commands above
```

**Verify Database Creation:**
```bash
psql -U suchana_user -d suchana_hub -h localhost
# You should get psql prompt if successful
\q # Exit
```

---

### STEP 6: CONFIGURE APPLICATION

Edit `config.py` if needed (optional - defaults should work):

```python
# Line around 20 - Update if using different credentials:
SQLALCHEMY_DATABASE_URI = 'postgresql://suchana_user:suchana_password@localhost:5432/suchana_hub'
```

---

### STEP 7: INITIALIZE DATABASE TABLES

With virtual environment activated, run:

```bash
# Navigate to project directory first
cd "C:\Users\di\Desktop\Suchana Hub"

# Initialize database with tables and default users
python run.py
```

OR use Flask CLI:
```bash
flask shell
>>> from app import create_app, db
>>> app = create_app()
>>> db.create_all()
>>> exit()
```

This creates tables and adds default users:
- Admin: admin / admin123
- Teacher: teacher / teacher123
- Staff: staff / staff123

---

### STEP 8: RUN THE APPLICATION

With virtual environment activated:

```bash
python run.py
```

You should see:
```
╔════════════════════════════════════════════════════════════╗
║          SUCHANA HUB - Attendance & Notification System   ║
╚════════════════════════════════════════════════════════════╝

🚀 Server Starting...
- URL: http://localhost:5000
- Debug Mode: True

📚 Default Login Credentials:
- Admin: admin / admin123
- Teacher: teacher / teacher123  
- Staff: staff / staff123
```

---

## 🌐 ACCESSING THE APPLICATION

Open web browser and go to:
```
http://localhost:5000
```

### Login with default credentials:
1. **Admin Account:**
   - Username: `admin`
   - Password: `admin123`
   - Access: Full system management

2. **Teacher Account:**
   - Username: `teacher`
   - Password: `teacher123`
   - Access: Class management, feedback

3. **Staff Account:**
   - Username: `staff`
   - Password: `staff123`
   - Access: Support operations

---

## 📊 USING THE APPLICATION

### Admin Dashboard:
1. Manage students and users
2. Upload attendance data
3. View and process attendance
4. Send notifications
5. Configure system settings
6. Generate reports

### Teacher Dashboard:
1. View class attendance
2. Provide student feedback
3. View feedback history
4. Check notification logs

### Attendance Upload:
1. Go to "Attendance Upload"
2. Prepare CSV file with format:
   ```
   student_id,roll_no,timestamp
   STU001,001,09:15:30
   STU002,002,09:20:00
   ```
3. Upload file for current date and class
4. System automatically categorizes as:
   - **Present**: Before 09:00
   - **Late**: After 09:00 but within threshold
   - **Absent**: No record

### Create Sample Data:
```bash
flask create-demo-data
```
This creates test students and attendance records.

---

## 🔐 SECURITY RECOMMENDATIONS (For Production)

⚠️ **IMPORTANT**: Before deploying to production:

1. **Change Default Passwords:**
   ```python
   # Edit app/models.py, change password hashes for:
   # - admin user
   # - teacher user
   # - staff user
   ```

2. **Update Configuration:**
   ```python
   # In config.py:
   SECRET_KEY = 'generate-random-secret-key'
   DEBUG = False  # Disable debug mode
   SESSION_COOKIE_SECURE = True
   ```

3. **Use Environment Variables:**
   Create `.env` file:
   ```
   FLASK_ENV=production
   DATABASE_URL=postgresql://user:password@host:5432/db
   SECRET_KEY=your-secret-key-here
   ```

4. **Set up HTTPS/SSL Certificate**

5. **Configure email/SMS gateway** for actual notifications

---

## 🐛 TROUBLESHOOTING

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Solution:** Ensure virtual environment is activated
```bash
# Windows
.\venv\Scripts\Activate.ps1
# macOS/Linux
source venv/bin/activate
```

### Problem: "could not connect to server: Connection refused"
**Solution:** PostgreSQL is not running
```bash
# Windows - PostgreSQL should auto-start
# Check Services: Press Win+R, type "services.msc"

# macOS
brew services start postgresql

# Linux
sudo systemctl start postgresql
```

### Problem: "FATAL: role 'suchana_user' does not exist"
**Solution:** Create the database user (see STEP 5)

### Problem: Application runs but database is empty
**Solution:** Run initialization:
```bash
python run.py  # Will auto-create tables
# OR
flask create-demo-data
```

### Problem: Port 5000 already in use
**Solution:** Change port in run.py or:
```bash
# Find process using port 5000 and kill it
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

---

## 📚 PROJECT STRUCTURE EXPLAINED

```
Suchana Hub/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (SQLAlchemy)
│   └── routes/                  # URL routing modules
│       ├── auth_routes.py       # Login, logout, dashboards
│       ├── student_routes.py    # Student CRUD operations
│       ├── attendance_routes.py # Attendance upload & processing
│       ├── notification_routes.py # Guardian notifications
│       ├── feedback_routes.py   # Teacher feedback system
│       ├── report_routes.py     # Reports and analytics
│       └── settings_routes.py   # System settings
│
├── templates/                    # HTML files (Jinja2)
│   ├── base.html                # Base template with navbar/footer
│   ├── index.html               # Home page
│   ├── login.html               # Login form
│   ├── admin_dashboard.html     # Admin dashboard
│   ├── teacher_dashboard.html   # Teacher dashboard
│   ├── staff_dashboard.html     # Staff dashboard
│   ├── student_management.html  # Student CRUD
│   ├── attendance.html          # Attendance management
│   ├── notifications.html       # Notifications
│   ├── feedback.html            # Feedback system
│   ├── reports.html             # Reports and analytics
│   └── settings.html            # Settings and configuration
│
├── static/                       # Static files
│   └── style.css                # All CSS styling
│
├── uploads/                      # CSV/Excel file uploads (auto-created)
│
├── config.py                     # Database and app configuration
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

---

## 🔄 DATABASE SCHEMA

### Users Table
- id (Primary Key)
- username, email, password_hash
- full_name, phone, role
- is_active, created_at, updated_at

### Students Table
- id (Primary Key)
- student_id, roll_no (Unique identifiers)
- name, email, phone
- class_name, section
- guardian_name, guardian_phone, guardian_email
- is_active, created_at, updated_at

### Attendance Table (Core Logic)
- id (Primary Key)
- student_id (Foreign Key → Students)
- date, check_in_time
- status (present/late/absent) - **Automatically calculated**
- class_name, notes
- created_at, updated_at

### Notifications Table
- id (Primary Key)
- student_id (Foreign Key → Students)
- notification_type, message
- recipient_name, recipient_phone, recipient_email
- status (sent/pending/failed)
- delivery_method (email/sms/both)
- created_at

### Feedback Table
- id (Primary Key)
- student_id, teacher_id (Foreign Keys)
- category (academic/behavior/participation)
- rating (1-5), comments
- share_with_student, share_with_guardian

### Settings Table
- id (Primary Key)
- setting_key (PRIMARY UNIQUE INDEX)
- setting_value, description
- data_type, created_at, updated_at

---

## 📖 KEY CONCEPTS FOR LEARNERS

### 1. **Flask App Factory Pattern**
```python
# In app/__init__.py
def create_app(config=None):
    app = Flask(__name__)
    # ... initialize and configure app
    return app
```
**Why?** - Allows multiple instances, easier testing, better modularity

### 2. **SQLAlchemy ORM**
Maps Python objects to database tables:
```python
# Define model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

# Use in code
student = Student(name="Raj")
db.session.add(student)
db.session.commit()
```

### 3. **Blueprints for Modularity**
Organize routes into separate files:
```python
# In auth_routes.py
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    ...

# In app/__init__.py
app.register_blueprint(auth_bp)
```

### 4. **Role-Based Access Control**
```python
@role_required('admin')
def admin_only_function():
    ...
```

### 5. **CSV Attendance Processing**
Automatically categorizes as Present/Late/Absent based on time

---

## 🚀 DEPLOYMENT OPTIONS

### Option 1: Heroku (Cloud)
```bash
# Create Procfile
echo "web: gunicorn run:app" > Procfile

# Deploy
heroku login
heroku create suchana-hub
git push heroku main
```

### Option 2: AWS
Use Elastic Beanstalk or EC2 with Gunicorn + Nginx

### Option 3: DigitalOcean
Simple VPS deployment with systemd service

### Option 4: Docker
Create Dockerfile for containerization

---

## 📞 SUPPORT & CONTACT

For issues, improvements, or questions:
- Email: admin@suchanahub.com
- GitHub: [Your Repository]

---

## 📄 LICENSE & TERMS

This is an academic project for MCA semester.
Feel free to modify and distribute for educational purposes.

---

## ✅ CHECKLIST FOR VIVA/DEMO

Before your viva presentation, ensure:
- [ ] Application runs without errors
- [ ] Can log in with all three roles
- [ ] Can upload CSV attendance file
- [ ] Attendance categorizes correctly (present/late/absent)
- [ ] Can add, edit, delete students
- [ ] Can add feedback for students
- [ ] Reports generate without errors
- [ ] Settings page accessible
- [ ] Responsive design works on mobile
- [ ] Comments in code explain key concepts
- [ ] Database properly configured

---

**Last Updated:** March 3, 2026
**Version:** 1.0
**Status:** Production Ready
