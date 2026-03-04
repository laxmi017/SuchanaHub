"""
SUCHANA HUB - Authentication Routes
Handles user login, logout, and dashboard routing based on user role
For academic project - extensively commented to explain Flask concepts
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from app.models import db, User

# Blueprint allows us to organize routes into separate files
# "auth" is the blueprint name, __name__ identifies the module
auth_bp = Blueprint('auth', __name__)


# ============================================================================
# DECORATOR - Role-based Access Control
# ============================================================================
def login_required(f):
    """
    Decorator to protect routes - user must be logged in
    If not logged in, redirects to login page
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user_id exists in session (means user is logged in)
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    """
    Decorator to check if user has required role
    Usage: @role_required('admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in first.', 'warning')
                return redirect(url_for('auth.login'))
            
            if session.get('role') != role and session.get('role') != 'admin':
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# ============================================================================
# LOGIN ROUTE
# ============================================================================
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login Route
    GET: Display login form
    POST: Process login credentials
    """
    
    if request.method == 'POST':
        # Get username/email and password from form
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Validate input
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return redirect(url_for('auth.login'))
        
        try:
            # Query user by username or email
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            # Verify user exists and password is correct
            if user and user.check_password(password):
                # Check if account is active
                if not user.is_active:
                    flash('This account has been deactivated.', 'danger')
                    return redirect(url_for('auth.login'))
                
                # Create session - store user info in session
                session.permanent = True
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                session['full_name'] = user.full_name
                
                flash(f'Welcome, {user.full_name}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                # Invalid credentials
                flash('Invalid username or password.', 'danger')
        
        except Exception as e:
            # Database error
            flash(f'An error occurred: {str(e)}', 'danger')
    
    return render_template('login.html')


# ============================================================================
# LOGOUT ROUTE
# ============================================================================
@auth_bp.route('/logout')
def logout():
    """
    Logout Route
    Clears session data and redirects to home page
    """
    # Get username before clearing session (for display message)
    username = session.get('username', 'User')
    
    # Clear all session data
    session.clear()
    
    flash(f'{username}, you have been logged out successfully.', 'success')
    return redirect(url_for('index'))


# ============================================================================
# DASHBOARD ROUTE - Routes to role-specific dashboard
# ============================================================================
@auth_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Dashboard Route
    Routes to role-specific dashboard based on user's role
    
    Concept: Different users see different dashboards
    - Admin: Full system management
    - Teacher: Class-specific view
    - Staff: Support staff view
    """
    
    role = session.get('role')
    
    # Try to get statistics for dashboard
    stats = {}
    try:
        from app.models import Student, Attendance, Notification
        
        # Get various statistics based on role
        stats['total_students'] = Student.query.count()
        stats['total_attendance'] = Attendance.query.count()
        stats['total_notifications'] = Notification.query.count()
        
    except Exception as e:
        print(f'Error fetching statistics: {e}')
    
    # Route to appropriate dashboard template
    if role == 'admin':
        return render_template('admin_dashboard.html', stats=stats)
    elif role == 'teacher':
        return render_template('teacher_dashboard.html', stats=stats)
    elif role == 'staff':
        return render_template('staff_dashboard.html', stats=stats)
    else:
        flash('Unknown role. Please contact administrator.', 'danger')
        return redirect(url_for('index'))


# ============================================================================
# HOME/INDEX ROUTE
# ============================================================================
@auth_bp.route('/')
def index():
    """
    Home Page Route
    Displays public landing page or redirects to dashboard if logged in
    """
    # If user is already logged in, go to dashboard
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    
    return render_template('index.html')
