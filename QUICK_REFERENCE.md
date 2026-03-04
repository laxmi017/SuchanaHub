# SUCHANA HUB - Quick Reference Guide

## 🚀 Quick Commands

### Start Application
```bash
python run.py
```

### Create Sample Data
```bash
flask create-demo-data
```

### Database Initialization
```bash
flask init-database
```

### Interactive Shell
```bash
flask shell
>>> from app.models import Student
>>> students = Student.query.all()
```

---

## 🔐 Default Credentials

| Role | Username | Password | Purpose |
|------|----------|----------|---------|
| Admin | admin | admin123 | Full system access |
| Teacher | teacher | teacher123 | Class & feedback management |
| Staff | staff | staff123 | Attendance & support operations |

---

## 📊 Attendance Processing Logic

**Cut-off Times:**
- Morning class: 09:00 AM
- Afternoon class: 02:00 PM

**Categorization:**
```
Check-in time <= Cut-off time → PRESENT ✓
Check-in time > Cut-off time → LATE ⏰
No check-in record → ABSENT ✗
```

---

## 📁 CSV File Format

Required columns for attendance upload:
```
student_id,roll_no,timestamp
```

Example:
```
STU001,001,09:15:30
STU002,002,08:45:00
STU003,003,14:05:00
```

---

## 🗄️ Database Info

**Database Name:** suchana_hub
**Default User:** suchana_user
**Default Password:** suchana_password
**Port:** 5432

Connection string:
```
postgresql://suchana_user:suchana_password@localhost:5432/suchana_hub
```

---

## 🌐 Application URLs

| Feature | URL | Access |
|---------|-----|--------|
| Home | http://localhost:5000/ | Public |
| Login | http://localhost:5000/login | Public |
| Dashboard | http://localhost:5000/dashboard | Authenticated |
| Students | http://localhost:5000/students/view | Admin/Staff |
| Attendance | http://localhost:5000/attendance/view | All |
| Notifications | http://localhost:5000/notifications/view | All |
| Feedback | http://localhost:5000/feedback/view | Teachers |
| Reports | http://localhost:5000/reports/view | All |
| Settings | http://localhost:5000/settings/ | Admin |

---

## 📝 Key Features by Role

### Admin Dashboard
✓ User management
✓ Student CRUD
✓ Attendance upload
✓ View all notifications
✓ System settings
✓ All reports

### Teacher Dashboard
✓ View class attendance
✓ Add/Edit feedback
✓ View notification logs
✓ Generate attendance reports
✗ Cannot manage settings

### Staff Dashboard
✓ Upload attendance
✓ View attendance
✓ View notifications
✓ Generate reports
✗ Cannot give feedback

---

## ⚠️ Important Notes

1. **Change Default Passwords** before production deployment
2. **Set SECRET_KEY** to random value in config.py
3. **Enable HTTPS** for production environment
4. **Configure Email/SMS** for actual notifications
5. **Back up database** regularly
6. **Monitor logs** for errors

---

## 🆘 Common Issues & Fixes

### "AttributeError: 'NoneType' object"
→ Check if record exists in database

### "IntegrityError: duplicate key"
→ Record with same ID/email already exists

### "OperationalError: connection refused"
→ PostgreSQL is not running

### "FileNotFoundError"
→ Check file path - use absolute paths

---

## 📚 Project Files Overview

| File | Purpose |
|------|---------|
| run.py | Application entry point |
| config.py | Database & app configuration |
| app/__init__.py | Flask app factory |
| app/models.py | Database models |
| templates/ | HTML pages (Jinja2) |
| static/style.css | CSS styling |
| routes/ | URL handlers (modular) |
| requirements.txt | Python dependencies |

---

## 🔄 Development Workflow

1. **Modify code** in app/ or templates/
2. **Flask autoreload** detects changes automatically
3. **Refresh browser** to see changes
4. **Check console** for error messages
5. **Debug using flask shell** if needed

---

## 📊 Database Queries Examples

```python
# All students
students = Student.query.all()

# Students in specific class
cs_students = Student.query.filter_by(class_name='CS101').all()

# Today's attendance
today = datetime.now().date()
today_attendance = Attendance.query.filter_by(date=today).all()

# Absent students
absent = Attendance.query.filter_by(status='absent').all()

# Count present students
present_count = Attendance.query.filter_by(status='present').count()
```

---

## 🎨 UI Customization

CSS file: `static/style.css`

Main color variables (customizable):
- Primary: #2196F3 (Blue)
- Success: #4CAF50 (Green)
- Danger: #F44336 (Red)
- Warning: #FFC107 (Yellow)

---

## 🔐 Security Checklist

- [ ] Change default SQL passwords
- [ ] Set strong SECRET_KEY
- [ ] Disable DEBUG mode in production
- [ ] Use environment variables
- [ ] Enable SSL/HTTPS
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Monitor access logs
- [ ] Regular dependency updates

---

**Last Updated:** March 3, 2026
**Version:** 1.0
