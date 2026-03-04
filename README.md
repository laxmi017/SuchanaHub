
# mca-3rdsem-pro

# **Software Requirements Specification (SRS)**

## **Project Title:** Smart College Attendance & Guardian Notification System

---

## **1. Introduction**

### **1.1 Purpose**

The Smart College Attendance & Guardian Notification System is a web-based application designed to automate student attendance tracking using biometric fingerprint data and instantly notify guardians about attendance status (Present / Absent / Late). The system improves accuracy, transparency, and communication between the college and guardians.

### **1.2 Scope**

The system provides:

* Secure login for Admin, Teacher, and Staff
* Student record management
* Attendance processing from biometric CSV/Excel files
* Automatic attendance status calculation
* Guardian notification system
* Teacher feedback mechanism
* Analytical reports
* System configuration settings

---

## **2. User Roles**

The system supports three main user roles:

| Role        | Description                                   |
| ----------- | --------------------------------------------- |
| **Admin**   | Full system control and configuration         |
| **Teacher** | Attendance viewing & feedback management      |
| **Staff**   | Upload biometric attendance files (CSV/Excel) |

---

## **3. Functional Requirements**

---

## **3.1 Login Page**

### **Purpose**

Authenticate users and ensure system security.

### **Components**

* Username / Email Field
* Password Field
* Role Selection (Admin / Teacher / Staff)
* Login Button
* Forgot Password Link
* Error Message Section

### **Behavior**

After successful login:

* Admin → Redirect to **Admin Dashboard**
* Teacher → Redirect to **Teacher Dashboard**
* Staff → Redirect to **Staff Dashboard**

---

## **3.2 Dashboard Page**

---

### **3.2.1 Admin Dashboard**

### **Purpose**

Provide system overview and quick navigation.

### **Displays**

* Total Students Count
* Today’s Present Count
* Today’s Absent Count
* Today’s Late Count
* Total Notifications Sent
* Attendance Graph / Charts

### **Quick Access Modules**

* Student Management
* Attendance Records
* Reports
* Notifications Log
* System Settings
* Feedback Messages

---

### **3.2.2 Teacher Dashboard**

### **Purpose**

Provide class-level attendance insights.

### **Displays**

* Class-wise Attendance Summary
* Today’s Attendance List
* Pending Feedback Notifications

### **Quick Actions**

* View Attendance
* Submit Feedback
* View Student List

---

### **3.2.3 Staff Dashboard**

### **Purpose**

Allow staff to upload biometric data.

### **Functions**

* Upload CSV File
* Upload Excel File
* Validate File Format
* Import Attendance Data

---

## **3.3 Student Management Page**

### **Purpose**

Manage student and guardian information.

### **Features**

#### **Add Student Form**

* Student Name
* Class / Section
* Roll Number
* Gender
* Course
* Guardian Name
* Guardian Phone Number
* Address
* Photo Upload (Optional)

#### **Fingerprint Registration**

* Capture Fingerprint
* Store Biometric Template

#### **Student List Table**

* Name
* Class
* Guardian Number
* Attendance Percentage
* Edit / Delete Options

### **Actions**

* Add Student
* Edit Student
* Delete Student
* Register Fingerprint
* View Attendance History

---

## **3.4 Attendance Page**

### **Purpose**

Display attendance records in real-time.

### **Features**

* Date Filter

* Class / Section Filter

* Attendance Table:

  * Student Name
  * Time of Scan
  * Status (Present / Absent / Late)
  * Remarks

* Manual Attendance (Admin / Teacher):

  * Mark Present
  * Mark Absent
  * Mark Late

* Auto Refresh / Update

### **Behavior**

Attendance updates immediately after CSV/Excel import.

---

## **3.5 Notification System Page**

### **Purpose**

Track notifications sent to guardians.

### **Notification Log Table**

* Student Name
* Guardian Phone
* Notification Type
* Time Sent
* Delivery Status

### **Notification Types**

1. Present Notification
2. Absent Notification
3. Late Arrival Notification
4. Feedback Notification

---

## **3.6 Feedback Page (Teacher Module)**

### **Purpose**

Allow teachers to send guardian feedback.

### **Components**

* Student Selection Dropdown
* Feedback Text Box
* Send Notification Button
* Feedback History Table

### **Sample Feedback**

* “Student was attentive today.”
* “Did not attend class.”
* “Late in class.”
* “Needs improvement in discipline.”

---

## **3.7 Reports Page**

### **Purpose**

Generate attendance analytics.

### **Report Types**

* Daily Attendance Report
* Weekly Attendance Summary
* Monthly Attendance Chart
* Student-wise Attendance Percentage
* Class-wise Comparison

### **Export Formats**

* PDF
* Excel
* CSV

### **Visualizations**

* Pie Charts
* Bar Graphs
* Line Charts

---

## **3.8 Settings Page (Admin Only)**

### **Purpose**

Configure system behavior.

### **Settings Include**

* SMS API Setup

* Email Notifications

* Attendance Cut-off Time

* User Management:

  * Add Admin
  * Add Teacher
  * Reset Password

* Biometric Device Configuration:

  * Device IP
  * Data Sync Interval

---

## **4. Attendance Processing Logic**

### **Input Source**

Biometric fingerprint device exports attendance data in:

* CSV File
* Excel File

### **Processing Steps**

1. Staff/Admin uploads file
2. System reads scan timestamps
3. System evaluates cut-off time
4. Status Calculation:

| Condition           | Status  |
| ------------------- | ------- |
| Scan before cut-off | Present |
| Scan after cut-off  | Late    |
| No scan             | Absent  |

5. Notification triggered automatically

---

## **5. Overall Workflow**

1. User logs in → Dashboard
2. Student data stored in database
3. Students scan fingerprint daily
4. Biometric device exports CSV/Excel
5. Staff uploads file
6. System calculates attendance
7. Guardians receive notifications
8. Teachers send feedback (optional)
9. Admin generates reports

---

## **6. System Objectives**

The system ensures:

✔ Accurate attendance tracking
✔ Reduced manual work
✔ Real-time guardian communication
✔ Attendance transparency
✔ Analytical academic monitoring

=======
# SUCHANA HUB - Smart College Attendance & Guardian Notification System

> A Complete Web Application built with Flask + PostgreSQL for MCA Semester Project

## 🎓 Project Overview

SUCHANA HUB is a comprehensive attendance management system designed for colleges and educational institutions. It automates the tedious process of tracking student attendance, processing biometric data, and notifying guardians about their ward's attendance status.

### Key Features

✅ **Multi-Role System** - Separate dashboards for Admin, Teachers, and Staff
✅ **Biometric Integration** - Process attendance from CSV/Excel biometric files
✅ **Smart Categorization** - Automatically mark students as Present/Late/Absent
✅ **Guardian Notifications** - Auto-send SMS/Email alerts to parents
✅ **Teacher Feedback** - Comprehensive feedback system on student performance
✅ **Analytics & Reports** - Detailed reports on attendance patterns
✅ **System Settings** - Configurable cut-off times and notification rules
✅ **Responsive UI** - Works perfectly on desktop, tablet, and mobile

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Installation](#installation)
6. [Database Design](#database-design)
7. [User Roles](#user-roles)
8. [API Routes](#api-routes)
9. [Contributing](#contributing)
10. [License](#license)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip (Python package manager)

### Installation (5 minutes)

```bash
# 1. Clone/Navigate to project
cd "Suchana Hub"

# 2. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create PostgreSQL database
createdb suchana_hub

# 5. Run application
python run.py
```

### Access Application
```
http://localhost:5000

Default Credentials:
- Admin: admin / admin123
- Teacher: teacher / teacher123
- Staff: staff / staff123
```

---

## ✨ Features in Detail

### 1. **Multi-Role Authentication**
- **Admin**: Full system access, user management, settings
- **Teacher**: Class management, feedback giving, attendance viewing
- **Staff**: Support operations, attendance upload, data management
- Secure session management with 30-minute timeout

### 2. **Student Management**
- Add, edit, view, delete student records
- Store guardian contact information
- Track class and section assignments
- Active/inactive status management

### 3. **Attendance Processing**
**The Core Feature** - Automatically processes attendance:

```
CSV Format:
student_id,roll_no,timestamp
STU001,001,09:15:30
STU002,002,14:05:00

Processing Logic:
09:00 → Cut-off time for morning class
├── Before 09:00 → PRESENT ✓
├── After 09:00 → LATE ⏰
└── No record → ABSENT ✗
```

### 4. **Guardian Notifications**
- Automated notifications on mark absent
- Optional late arrival alerts
- Manual notification sending
- SMS/Email delivery tracking
- Re-send functionality for failed deliveries

### 5. **Teacher Feedback System**
- Rate students (1-5 stars):
  - Academic Performance
  - Behavior & Conduct
  - Class Participation
- Add detailed comments
- Option to share with student/guardian
- Edit and delete feedback

### 6. **Reports & Analytics**
- Attendance summary reports
- Chronically absent students list
- Late arrivals analysis
- Individual student records
- Date range filtering
- Class-wise breakdowns

### 7. **System Settings**
- Configurable cut-off times
- Notification rules and templates
- Email/SMS provider configuration
- Session timeout settings
- Institution information

---

## 🏗️ Technology Stack

### Backend
- **Framework**: Flask 2.3 (Python web framework)
- **ORM**: SQLAlchemy 2.0 (Database abstraction)
- **Authentication**: Werkzeug (Password hashing)

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Responsive design with flexbox/grid
- **Jinja2** - Template engine

### Database
- **PostgreSQL 12+** - Relational database
- **psycopg2** - Python PostgreSQL adapter

### Data Processing
- **pandas** - CSV/Excel file handling
- **openpyxl** - Excel format support

### Deployment Ready
- **Development**: Flask development server
- **Production**: Gunicorn WSGI server
- **Cloud**: Heroku, AWS, DigitalOcean ready

---

## 📁 Project Structure

```
Suchana Hub/
│
├── app/                              # Main application package
│   ├── __init__.py                  # Flask app factory
│   ├── models.py                    # SQLAlchemy database models
│   │                                 #   └─ User, Student, Attendance
│   │                                 #   └─ Notification, Feedback, Settings
│   │
│   └── routes/                      # Modular route handlers
│       ├── auth_routes.py           # Login/logout, role-based dashboards
│       ├── student_routes.py        # Student CRUD operations
│       ├── attendance_routes.py     # Attendance upload & processing
│       ├── notification_routes.py   # Guardian notifications
│       ├── feedback_routes.py       # Teacher feedback
│       ├── report_routes.py         # Reports & analytics
│       ├── settings_routes.py       # System configuration
│       └── __init__.py              # Routes package marker
│
├── templates/                       # HTML templates (Jinja2)
│   ├── base.html                   # Base layout with navigation
│   ├── index.html                  # Homepage
│   ├── login.html                  # Login form
│   ├── admin_dashboard.html        # Admin interface
│   ├── teacher_dashboard.html      # Teacher interface
│   ├── staff_dashboard.html        # Staff interface
│   ├── student_management.html     # Student management
│   ├── attendance.html             # Attendance interface
│   ├── notifications.html          # Notifications interface
│   ├── feedback.html               # Feedback interface
│   ├── reports.html                # Reports interface
│   └── settings.html               # Settings interface
│
├── static/                         # Static files
│   └── style.css                   # Comprehensive CSS (500+ lines)
│
├── uploads/                        # CSV/Excel uploads (auto-created)
│
├── config.py                       # Configuration settings
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── SETUP_GUIDE.md                  # Detailed setup instructions
├── README.md                       # This file
└── .gitignore                      # Git ignore rules (optional)

```

---

## 🗄️ Database Schema

### Tables Created

1. **users** - Admin, Teacher, Staff accounts
   ```
   id | username | email | password_hash | role | is_active | created_at
   ```

2. **students** - Student records with guardian info
   ```
   id | student_id | roll_no | name | email | class_name | guardian_name 
   | guardian_phone | guardian_email | is_active | created_at
   ```

3. **attendance** - Attendance records (automatically categorized)
   ```
   id | student_id | date | check_in_time | status(present/late/absent)
   | class_name | notes | created_at
   ```

4. **notifications** - Sent notifications log
   ```
   id | student_id | notification_type | message | recipient_phone/email
   | status(sent/pending/failed) | delivery_method | created_at
   ```

5. **feedback** - Teacher feedback on students
   ```
   id | student_id | teacher_id | category | rating(1-5) | comments
   | share_with_student | share_with_guardian | created_at
   ```

6. **settings** - System configuration
   ```
   id | setting_key | setting_value | description | data_type | created_at
   ```

---

## 👥 User Roles & Permissions

### Admin
- ✓ View all students, teachers, staff
- ✓ Create, edit, delete student records
- ✓ Upload and process attendance
- ✓ View all notifications
- ✓ Access system settings
- ✓ Generate all reports
- ✓ Manage user accounts

### Teacher
- ✓ View class attendance
- ✓ Add feedback to students
- ✓ View their own feedback
- ✓ See notification logs for their classes
- ✓ Generate attendance reports
- ✗ Cannot edit student records
- ✗ Cannot access system settings

### Staff
- ✓ View all students
- ✓ Upload attendance files
- ✓ Process attendance records
- ✓ View attendance records
- ✓ View notification logs
- ✓ Generate reports
- ✗ Cannot give feedback
- ✗ Cannot change system settings

---

## 🔌 API Routes

### Authentication
```
POST   /login              - User login
GET    /logout             - User logout
GET    /dashboard          - Role-based dashboard
GET    /                   - Homepage
```

### Students
```
GET    /students/view      - List all students
GET    /students/add       - Add student form
POST   /students/add       - Create student
GET    /students/edit/<id> - Edit student form
POST   /students/edit/<id> - Update student
POST   /students/delete/<id> - Delete student
```

### Attendance
```
GET    /attendance/view    - View attendance records
GET    /attendance/upload  - Upload form
POST   /attendance/upload  - Process CSV/Excel file
POST   /attendance/mark/<id> - Mark attendance manually
```

### Notifications
```
GET    /notifications/view     - View notification log
POST   /notifications/send     - Send notification
POST   /notifications/resend   - Resend notification
```

### Feedback
```
GET    /feedback/view      - View feedback records
GET    /feedback/add       - Add feedback form
POST   /feedback/add       - Save feedback
GET    /feedback/edit/<id> - Edit feedback form
POST   /feedback/edit/<id> - Update feedback
```

### Reports
```
GET    /reports/view       - Reports dashboard
GET    /reports/attendance-summary - Attendance summary
GET    /reports/absent-students   - Absent students report
GET    /reports/late-arrivals     - Late arrivals report
```

### Settings
```
GET    /settings/          - Settings page
POST   /settings/save      - Save settings
POST   /settings/profile/update - Update profile
```

---

## 💡 Key Implementation Concepts

### 1. Application Factory Pattern
```python
def create_app(config=None):
    app = Flask(__name__)
    db.init_app(app)
    # ... register blueprints
    return app
```
**Benefit:** Allows multiple app instances, easier testing

### 2. Database Models with Relationships
```python
class Student(db.Model):
    attendance = db.relationship('Attendance', backref='student')
    feedback = db.relationship('Feedback', backref='student')
```
**Benefit:** Easy navigation between related records

### 3. Role-Based Access Control (RBAC)
```python
@role_required('admin')
def admin_only_route():
    pass
```
**Benefit:** Secure, role-specific functionality

### 4. Blueprint Modularity
Each module (student, attendance, etc.) is separate for:
- Clean code organization
- Easy maintenance
- Scalability
- Team collaboration

### 5. Attendance Categorization Logic
```python
def categorize_attendance(check_in_time, cutoff_time):
    if check_in_time <= cutoff_time:
        return 'present'
    else:
        return 'late'
```
**Benefit:** Automatic, consistent categorization

---

## 📊 Sample Data Format

### Attendance CSV Template
```csv
student_id,roll_no,timestamp
STU001,001,09:15:30
STU002,002,09:45:00
STU003,003,14:20:15
STU004,004,14:05:00
```

### Processing Result
| Student ID | Roll No | Time | Status | Reason |
|-----------|---------|------|--------|--------|
| STU001 | 001 | 09:15 | LATE | After 09:00 cutoff |
| STU002 | 002 | 09:45 | LATE | After 09:00 cutoff |
| STU003 | 003 | 14:20 | LATE | After 14:00 cutoff |
| STU004 | 004 | 14:05 | LATE | After 14:00 cutoff |
| STU005 | 005 | - | ABSENT | No entry |

---

## 🔒 Security Features

- ✓ Password hashing with Werkzeug
- ✓ SQL injection prevention via SQLAlchemy ORM
- ✓ Session management with timeout
- ✓ CSRF protection ready
- ✓ XSS prevention with Jinja2 escaping
- ✓ Role-based access control
- ✓ Secure headers configuration

### Production Security Notes
- Change default passwords
- Use environment variables for sensitive data
- Enable HTTPS/SSL
- Set DEBUG = False
- Configure CORS for APIs
- Use strong SECRET_KEY

---

## 📱 Responsive Design

Application works seamlessly on:
- 📺 Desktop (1920px+)
- 💻 Laptop (1366px+)
- 📱 Tablet (768px+)
- 📲 Mobile (320px+)

CSS breakpoints:
- Extra large: 1200px+
- Large: 992px+
- Medium: 768px+
- Small: 480px+

---

## 🚀 Deployment Guide

### Development
```bash
python run.py
# Runs on http://localhost:5000
```

### Production (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### With Nginx Reverse Proxy
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 5000 in use | Change port in run.py or kill process |
| Database not found | Run database initialization |
| Import errors | Activate virtual environment |
| CSS not loading | Clear browser cache, hard refresh (Ctrl+Shift+R) |
| Login fails | Check PostgreSQL is running, verify credentials |

---

## 📚 Learning Resources

This project is designed for MCA students to learn:

1. **Flask Framework**
   - Application factory pattern
   - Blueprints and modular design
   - Request/response handling
   - Session management

2. **SQLAlchemy ORM**
   - Model definition
   - Relationships (One-to-Many, Many-to-One)
   - Query building
   - Database migrations

3. **Web Development**
   - HTML5 semantic markup
   - CSS3 responsive design
   - Form handling
   - File uploads (CSV/Excel)

4. **Database Design**
   - Relational schema
   - Normalization
   - Foreign keys
   - Indexing

5. **Security**
   - Password hashing
   - Session management
   - Role-based access control
   - Input validation

---

## 📝 Mini Documentation

### How Attendance Works
1. Admin/Staff uploads CSV with `student_id, roll_no, timestamp`
2. System reads each record
3. Compares check-in time with cut-off (default 09:00)
4. Automatically marks as:
   - ✓ PRESENT if before cut-off
   - ⏰ LATE if after cut-off
   - ✗ ABSENT if no record
5. Creates notification if configured
6. Records saved in database

### How Notifications Work
1. After attendance processing, system checks notification settings
2. If "notify_on_absent" enabled AND student marked ABSENT:
3. Creates notification record with guardian contact
4. (In production) Sends SMS/Email via configured provider
5. Logs status (sent/pending/failed)
6. Admin can view notification history and resend if needed

### How Reports Work
1. Query attendance records within date range
2. Group and aggregate by date/class/student
3. Calculate percentages
4. Display in tabular format
5. Export options available

---

## 🤝 Contributing

Students are encouraged to:
1. Add new features (e.g., student login, parent portal)
2. Improve UI/UX
3. Optimize database queries
4. Add automated tests
5. Implement additional reports

---

## 📄 License

This is an academic project for MCA semester.
Free to modify and distribute for educational purposes.

---

## ✅ Viva Preparation Checklist

Before presentation, verify:
- [ ] All features working as intended
- [ ] Database properly configured
- [ ] Can log in with all three roles
- [ ] CSV attendance processing works
- [ ] Code is well-commented
- [ ] Responsive design tested
- [ ] No hardcoded values (use config)
- [ ] Error handling implemented
- [ ] Understands each concept
- [ ] Ready to explain architecture

---

## 📞 Support

For questions or issues:
- Review SETUP_GUIDE.md for detailed instructions
- Check troubleshooting section
- Examine code comments for implementation details
- Refer to inline documentation in models.py and routes

---

**Version:** 1.0  
**Last Updated:** March 3, 2026  
**Status:** Production Ready  
**Maintainer:** MCA Student

---

🎓 **Happy Learning!** Your feedback helps improve this project for future students 🚀
 (Initial commit: Suchana Hub)
