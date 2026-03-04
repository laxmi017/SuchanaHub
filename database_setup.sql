-- SUCHANA HUB - PostgreSQL Database Setup Script
-- Run this to set up database and user from scratch

-- Create database user
CREATE USER suchana_user WITH PASSWORD 'suchana_password';

-- Create database
CREATE DATABASE suchana_hub;

-- Connect to the database
\c suchana_hub

-- Grant privileges to user
ALTER ROLE suchana_user SET client_encoding TO 'utf8';
ALTER ROLE suchana_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE suchana_user SET default_transaction_deferrable TO on;
ALTER ROLE suchana_user SET timezone TO 'UTC';

-- Grant all privileges on database to user
GRANT ALL PRIVILEGES ON DATABASE suchana_hub TO suchana_user;

-- Grant schema privileges
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO suchana_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO suchana_user;
GRANT USAGE ON SCHEMA public TO suchana_user;

-- Create tables (SQLAlchemy will do this, but here's the manual creation for reference)
-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(20) NOT NULL DEFAULT 'staff',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(20) UNIQUE NOT NULL,
    roll_no VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120),
    phone VARCHAR(20),
    class_name VARCHAR(50) NOT NULL,
    section VARCHAR(20),
    guardian_name VARCHAR(120) NOT NULL,
    guardian_phone VARCHAR(20) NOT NULL,
    guardian_email VARCHAR(120),
    date_of_birth DATE,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    date DATE NOT NULL,
    check_in_time TIME,
    class_name VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'absent',
    notes TEXT,
    device_id VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    notification_type VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    recipient_name VARCHAR(120) NOT NULL,
    recipient_phone VARCHAR(20),
    recipient_email VARCHAR(120),
    status VARCHAR(20) DEFAULT 'pending',
    delivery_method VARCHAR(20),
    delivery_timestamp TIMESTAMP,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
);

-- Feedback table
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL,
    teacher_id INTEGER NOT NULL,
    category VARCHAR(50) NOT NULL,
    rating INTEGER NOT NULL,
    comments TEXT NOT NULL,
    share_with_student BOOLEAN DEFAULT TRUE,
    share_with_guardian BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Settings table
CREATE TABLE IF NOT EXISTS settings (
    id SERIAL PRIMARY KEY,
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    description VARCHAR(255),
    data_type VARCHAR(20),
    is_visible_to_admin BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_students_student_id ON students(student_id);
CREATE INDEX idx_students_roll_no ON students(roll_no);
CREATE INDEX idx_students_class_name ON students(class_name);
CREATE INDEX idx_attendance_student_id ON attendance(student_id);
CREATE INDEX idx_attendance_date ON attendance(date);
CREATE INDEX idx_attendance_status ON attendance(status);
CREATE INDEX idx_attendance_class_name ON attendance(class_name);
CREATE INDEX idx_notifications_student_id ON notifications(student_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_created_at ON notifications(created_at);
CREATE INDEX idx_feedback_student_id ON feedback(student_id);
CREATE INDEX idx_feedback_teacher_id ON feedback(teacher_id);
CREATE INDEX idx_feedback_created_at ON feedback(created_at);
CREATE INDEX idx_settings_setting_key ON settings(setting_key);

-- Insert default settings
INSERT INTO settings (setting_key, setting_value, description, data_type)
VALUES 
('morning_cutoff_time', '09:00', 'Morning class cut-off time', 'time'),
('afternoon_cutoff_time', '14:00', 'Afternoon class cut-off time', 'time'),
('absent_threshold', '120', 'Minutes to mark student absent', 'integer'),
('min_attendance_percentage', '75', 'Minimum attendance percentage threshold', 'integer'),
('notify_on_absent', 'true', 'Send notification when student is absent', 'boolean'),
('notify_on_late', 'false', 'Send notification when student is late', 'boolean'),
('institution_name', 'College of Engineering', 'Institution name', 'string')
ON CONFLICT (setting_key) DO NOTHING;

-- Grant all permissions on new tables to user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO suchana_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO suchana_user;

-- Output for verification
\dt

COMMIT;

-- All done! Database is ready.
-- Connection string: postgresql://suchana_user:suchana_password@localhost:5432/suchana_hub
