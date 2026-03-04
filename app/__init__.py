"""
SUCHANA HUB - Flask Application Factory
Initializes and configures the Flask application
Uses Application Factory Pattern for better modularity

This file sets up:
1. Flask app instance
2. Database connection
3. Routes and blueprints
4. Error handlers
5. Session management
"""

from flask import Flask, render_template
from flask_session import Session
from config import Config, DevelopmentConfig
from app.models import db, init_db


def create_app(config=None):
    """
    Application Factory Function
    Creates and configures Flask app instance
    
    Why use factory pattern?
    - Allows creating multiple app instances with different configs
    - Makes testing easier
    - Better code organization
    - Supports different environments (dev, prod, test)
    
    Args:
        config: Configuration object to use
    
    Returns:
        Configured Flask application instance
    """
    
    # Create Flask application
    app = Flask(__name__, instance_relative_config=True)
    
    # Load configuration
    if config is None:
        config = DevelopmentConfig()
    
    app.config.from_object(config)
    
    # ========================================================================
    # DATABASE INITIALIZATION
    # ========================================================================
    
    # Initialize SQLAlchemy with app
    # This sets up the database connection
    db.init_app(app)
    
    # Initialize Flask-Session
    # This handles server-side session storage
    Session(app)
    
    # Create database tables on app startup
    with app.app_context():
        try:
            db.create_all()
            init_db(app)
        except Exception as e:
            print(f'Database initialization error: {e}')
    
    # ========================================================================
    # REGISTER BLUEPRINTS (Routes)
    # ========================================================================
    # Blueprints are like mini-applications that can be plugged into Flask
    # Each module handles a specific area of functionality
    
    from app.routes.auth_routes import auth_bp
    from app.routes.student_routes import student_bp
    from app.routes.attendance_routes import attendance_bp
    from app.routes.notification_routes import notification_bp
    from app.routes.feedback_routes import feedback_bp
    from app.routes.report_routes import report_bp
    from app.routes.settings_routes import settings_bp
    
    # Register blueprints
    app.register_blueprint(auth_bp)  # Authentication routes (/, /login, /logout)
    app.register_blueprint(student_bp)  # Student management
    app.register_blueprint(attendance_bp)  # Attendance processing
    app.register_blueprint(notification_bp)  # Guardian notifications
    app.register_blueprint(feedback_bp)  # Teacher feedback
    app.register_blueprint(report_bp)  # Reports and analytics
    app.register_blueprint(settings_bp)  # System settings
    
    # ========================================================================
    # ERROR HANDLERS
    # ========================================================================
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 - Page Not Found errors"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 - Internal Server errors"""
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Handle 403 - Forbidden errors"""
        return render_template('errors/403.html'), 403
    
    # ========================================================================
    # CONTEXT PROCESSORS
    # ========================================================================
    
    @app.context_processor
    def inject_user():
        """
        Make user info available in all templates
        Context processors add variables to template context
        """
        from flask import session
        return dict(
            user_id=session.get('user_id'),
            username=session.get('username'),
            role=session.get('role')
        )
    
    # ========================================================================
    # SHELL CONTEXT FOR flask shell COMMAND
    # ========================================================================
    
    @app.shell_context_processor
    def make_shell_context():
        """
        Make objects available in 'flask shell' command
        Useful for database debugging and testing
        """
        return {
            'db': db,
            'User': get_model('User'),
            'Student': get_model('Student'),
            'Attendance': get_model('Attendance'),
        }
    
    # ========================================================================
    # TEMPLATE FILTERS (Custom Jinja2 filters)
    # ========================================================================
    
    @app.template_filter('status_badge')
    def status_badge_filter(status):
        """
        Custom Jinja2 filter to display status as badge
        Usage in template: {{ record.status | status_badge }}
        """
        badge_class = {
            'present': 'badge-success',
            'late': 'badge-warning',
            'absent': 'badge-danger'
        }
        return badge_class.get(status, 'badge-info')
    
    @app.template_filter('format_date')
    def format_date_filter(date):
        """Format date for display"""
        if date:
            return date.strftime('%d-%m-%Y')
        return '-'
    
    @app.template_filter('format_time')
    def format_time_filter(time):
        """Format time for display"""
        if time:
            return time.strftime('%H:%M:%S')
        return '-'
    
    # ========================================================================
    # BEFORE/AFTER REQUEST HOOKS
    # ========================================================================
    
    @app.before_request
    def before_request():
        """
        Runs before each request
        Good place for authentication checks, logging, etc.
        """
        from flask import session
        
        # Set session to permanent (use PERMANENT_SESSION_LIFETIME from config)
        session.permanent = True
    
    @app.after_request
    def after_request(response):
        """
        Runs after each request
        Useful for response modification, logging, etc.
        """
        # Ensure browsers don't cache pages
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response
    
    # ========================================================================
    # CLI COMMANDS
    # ========================================================================
    
    @app.cli.command()
    def init_database():
        """Initialize database with tables and default data"""
        try:
            db.create_all()
            init_db(app)
            print('✓ Database initialized successfully!')
        except Exception as e:
            print(f'✗ Error initializing database: {e}')
    
    @app.cli.command()
    def create_demo_data():
        """Create sample data for testing"""
        from app.models import Student, Attendance
        from datetime import datetime, timedelta
        
        try:
            # Check if data already exists
            if Student.query.first():
                print('Demo data already exists!')
                return
            
            # Create sample students
            students = [
                Student(
                    student_id='STU001',
                    roll_no='001',
                    name='Raj Kumar',
                    email='raj@example.com',
                    class_name='CS101',
                    guardian_name='Usha Kumar',
                    guardian_phone='+91-9876543210',
                    guardian_email='usha@example.com'
                ),
                Student(
                    student_id='STU002',
                    roll_no='002',
                    name='Priya Singh',
                    email='priya@example.com',
                    class_name='CS101',
                    guardian_name='Rajesh Singh',
                    guardian_phone='+91-9876543211',
                    guardian_email='rajesh@example.com'
                ),
            ]
            
            for student in students:
                db.session.add(student)
                db.session.commit()
                
                # Add some attendance records
                for i in range(10):
                    date = datetime.now().date() - timedelta(days=i)
                    attendance = Attendance(
                        student_id=student.id,
                        date=date,
                        check_in_time=datetime.strptime('09:15:00', '%H:%M:%S').time(),
                        class_name='CS101',
                        status='present' if i % 3 != 0 else 'absent'
                    )
                    db.session.add(attendance)
            
            db.session.commit()
            print(f'✓ Created {len(students)} sample students')
        
        except Exception as e:
            db.session.rollback()
            print(f'✗ Error creating demo data: {e}')
    
    return app


def get_model(model_name):
    """Helper to get model by name"""
    from app.models import User, Student, Attendance, Notification, Feedback, Settings
    
    models = {
        'User': User,
        'Student': Student,
        'Attendance': Attendance,
        'Notification': Notification,
        'Feedback': Feedback,
        'Settings': Settings,
    }
    
    return models.get(model_name)


# ============================================================================
# DEBUG MODE TOOLBAR (only in development)
# ============================================================================
# Uncomment below to enable Flask Debug Toolbar for debugging
# from flask_debugtoolbar import DebugToolbarExtension
# def init_debug_toolbar(app):
#     toolbar = DebugToolbarExtension(app)
