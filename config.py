"""
SUCHANA HUB - Configuration File
Handles database configuration, Flask settings, and application constants
For academic project - explicitly commented for learners
"""

import os
from datetime import timedelta

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# PostgreSQL Connection String Format:
# postgresql://username:password@localhost:5432/database_name
# This tells Flask-SQLAlchemy how to connect to our PostgreSQL database

class Config:
    """
    Base Configuration Class
    Contains settings common to all environments
    """
    
    # Flask Secret Key - Used for session management and CSRF protection
    # IMPORTANT: Change this to a random string in production!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQLAlchemy Configuration
    # This uses PostgreSQL database (could also use MySQL, SQLite, etc.)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://suchana_user:suchana_password@localhost:5432/suchana_hub'
    
    # Disable modification tracking to save memory
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Enable SQL query echoing in development (useful for debugging)
    SQLALCHEMY_ECHO = False
    
    # ========================================================================
    # APPLICATION SETTINGS
    # ========================================================================
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Session expires after 30 minutes
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevent JavaScript from accessing cookies
    
    # Attendance Processing Settings
    MORNING_CUTOFF_TIME = '09:00'  # Default cut-off for morning classes
    AFTERNOON_CUTOFF_TIME = '14:00'  # Default cut-off for afternoon classes
    ABSENT_THRESHOLD_MINUTES = 120  # Mark absent if no check-in within X minutes
    
    # Notification Settings
    MIN_ATTENDANCE_PERCENTAGE = 75  # Trigger warning if attendance < 75%
    NOTIFY_ON_ABSENT = True
    NOTIFY_ON_LATE = False  # Can be configured by admin
    
    # File Upload Settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Maximum 16MB file upload
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    
    # ========================================================================
    # LOGGING CONFIGURATION
    # ========================================================================
    LOG_FILE = 'suchana_hub.log'
    LOG_LEVEL = 'INFO'


class DevelopmentConfig(Config):
    """
    Development Environment Configuration
    Used for local development with debugging enabled
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Print SQL queries for debugging


class ProductionConfig(Config):
    """
    Production Environment Configuration
    Used when deploying to production server
    """
    DEBUG = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """
    Testing Environment Configuration
    Used for running automated tests
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_password@localhost:5432/suchana_hub_test'
    WTF_CSRF_ENABLED = False


# Select configuration based on environment variable
# Default to development if not specified
config_name = os.environ.get('FLASK_ENV') or 'development'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Get the appropriate configuration
Config = config.get(config_name, config['default'])
