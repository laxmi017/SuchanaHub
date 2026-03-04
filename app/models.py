"""
SUCHANA HUB - Database Models
Defines all database tables using SQLAlchemy ORM
For academic project - extensively commented for learners to understand database design

Database Schema:
- Users: Stores admin, teacher, and staff accounts
- Students: Stores student information with guardian details  
- Attendance: Stores attendance records (Present/Late/Absent)
- Notifications: Logs of sent notifications to guardians
- Feedback: Teacher feedback on student performance
- Settings: System-wide configuration settings
"""

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy - ORM (Object Relational Mapping) that converts Python objects to database records
db = SQLAlchemy()


# ============================================================================
# USER MODEL - Handles authentication and role-based access
# ============================================================================
class User(db.Model):
    """
    User Model
    Represents Admin, Teacher, and Staff accounts
    Uses role-based access control (RBAC)
    
    Relationships:
    - Can have multiple attendance records
    - Teachers can give multiple feedback records
    """
    
    __tablename__ = 'users'
    
    # Primary Key - Unique identifier for each user
    id = db.Column(db.Integer, primary_key=True)
    
    # User credentials
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)  # Hashed password (never store plain text!)
    
    # User information
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    
    # Role-based access control
    # Valid values: 'admin', 'teacher', 'staff'
    role = db.Column(db.String(20), nullable=False, default='staff')
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (Foreign Keys)
    # A teacher can give feedback to multiple students
    feedback = db.relationship('Feedback', backref='teacher', lazy=True, foreign_keys='Feedback.teacher_id')
    
    def set_password(self, password):
        """Hash and store password securely"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password during login"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


# ============================================================================
# STUDENT MODEL - Stores student information
# ============================================================================
class Student(db.Model):
    """
    Student Model
    Stores student records with guardian contact information
    
    Relationships:
    - Can have multiple attendance records
    - Can receive multiple notifications
    - Can receive multiple feedback records
    """
    
    __tablename__ = 'students'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Student identification
    student_id = db.Column(db.String(20), unique=True, nullable=False, index=True)  # Unique ID (e.g., from RFID)
    roll_no = db.Column(db.String(20), unique=True, nullable=False, index=True)  # Roll number
    
    # Student basic information
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    
    # Class/Section information
    class_name = db.Column(db.String(50), nullable=False, index=True)  # e.g., "CS101", "MCA1"
    section = db.Column(db.String(20))
    
    # Guardian information - For sending notifications
    guardian_name = db.Column(db.String(120), nullable=False)
    guardian_phone = db.Column(db.String(20), nullable=False)
    guardian_email = db.Column(db.String(120))
    
    # Additional information
    date_of_birth = db.Column(db.Date)
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    
    # Account status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='student', lazy=True, cascade='all, delete-orphan')
    feedback = db.relationship('Feedback', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.roll_no} - {self.name}>'


# ============================================================================
# ATTENDANCE MODEL - Records attendance with status (Present/Late/Absent)
# ============================================================================
class Attendance(db.Model):
    """
    Attendance Model
    Stores attendance records with automatic status categorization
    
    Status Logic:
    - PRESENT: Check-in before cut-off time
    - LATE: Check-in after cut-off time but within threshold
    - ABSENT: No check-in record
    
    Relationships:
    - Many-to-One with Student
    """
    
    __tablename__ = 'attendance'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key to Student
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    
    # Attendance Information
    date = db.Column(db.Date, nullable=False, index=True)
    check_in_time = db.Column(db.Time)  # Time when student checked in
    
    # Biometric/CSV data fields
    class_name = db.Column(db.String(50), nullable=False)
    
    # Status - Automatically determined
    # Valid values: 'present', 'late', 'absent'
    status = db.Column(db.String(20), nullable=False, default='absent', index=True)
    
    # Additional information
    notes = db.Column(db.Text)  # Notes about attendance (e.g., "Medical leave approved")
    device_id = db.Column(db.String(50))  # Biometric device ID
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Attendance {self.student_id} - {self.date} - {self.status}>'


# ============================================================================
# NOTIFICATION MODEL - Logs communications sent to guardians
# ============================================================================
class Notification(db.Model):
    """
    Notification Model
    Logs all notifications/SMS/emails sent to guardians
    Helps track communication history
    
    Relationships:
    - Many-to-One with Student
    """
    
    __tablename__ = 'notifications'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Key to Student
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    
    # Notification Details
    notification_type = db.Column(db.String(50), nullable=False)  # 'attendance_alert', 'feedback', etc.
    message = db.Column(db.Text, nullable=False)
    
    # Recipient Information
    recipient_name = db.Column(db.String(120), nullable=False)
    recipient_phone = db.Column(db.String(20))  # For SMS
    recipient_email = db.Column(db.String(120))  # For Email
    
    # Delivery Status
    # Valid values: 'sent', 'pending', 'failed'
    status = db.Column(db.String(20), default='pending', index=True)
    
    # Delivery method
    delivery_method = db.Column(db.String(20))  # 'sms', 'email', 'both'
    
    # Tracking information
    delivery_timestamp = db.Column(db.DateTime)
    error_message = db.Column(db.Text)  # If delivery failed
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Notification {self.id} - {self.notification_type} - {self.status}>'


# ============================================================================
# FEEDBACK MODEL - Teacher feedback on student performance
# ============================================================================
class Feedback(db.Model):
    """
    Feedback Model
    Stores teacher feedback on student performance, behavior, and participation
    
    Relationships:
    - Many-to-One with Student
    - Many-to-One with User (Teacher)
    """
    
    __tablename__ = 'feedback'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    
    # Feedback Details
    category = db.Column(db.String(50), nullable=False)  # 'academic', 'behavior', 'participation', etc.
    rating = db.Column(db.Integer, nullable=False)  # 1-5 star rating
    comments = db.Column(db.Text, nullable=False)
    
    # Visibility Options
    share_with_student = db.Column(db.Boolean, default=True)
    share_with_guardian = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.teacher_id} -> {self.student_id}>'


# ============================================================================
# SETTINGS MODEL - System-wide configuration
# ============================================================================
class Settings(db.Model):
    """
    Settings Model
    Stores configurable system parameters
    Allows admin to customize application behavior without code changes
    
    Examples:
    - morning_cutoff_time: 09:00
    - notify_on_absent: true
    - min_attendance_percentage: 75
    """
    
    __tablename__ = 'settings'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Setting Key-Value pairs
    # Using string key makes it flexible for different config types
    setting_key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    setting_value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255))  # What this setting does
    
    # Metadata
    data_type = db.Column(db.String(20))  # 'string', 'integer', 'boolean', 'time'
    is_visible_to_admin = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Settings {self.setting_key}={self.setting_value}>'


# ============================================================================
# DATABASE INITIALIZATION HELPERS
# ============================================================================

def init_db(app):
    """
    Initialize database with app context
    Call this once at application startup
    """
    with app.app_context():
        # Create all tables defined by models
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Create default admin user if it doesn't exist
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@suchanahub.com',
                full_name='System Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')  # DEFAULT PASSWORD - CHANGE IN PRODUCTION!
            db.session.add(admin)
            
        # Create default teacher user
        teacher = User.query.filter_by(username='teacher').first()
        if not teacher:
            teacher = User(
                username='teacher',
                email='teacher@suchanahub.com',
                full_name='Sample Teacher',
                role='teacher',
                is_active=True
            )
            teacher.set_password('teacher123')  # DEFAULT PASSWORD - CHANGE IN PRODUCTION!
            db.session.add(teacher)
        
        # Create default staff user
        staff = User.query.filter_by(username='staff').first()
        if not staff:
            staff = User(
                username='staff',
                email='staff@suchanahub.com',
                full_name='Office Staff',
                role='staff',
                is_active=True
            )
            staff.set_password('staff123')  # DEFAULT PASSWORD - CHANGE IN PRODUCTION!
            db.session.add(staff)
        
        db.session.commit()
        print("✓ Default users created successfully!")
