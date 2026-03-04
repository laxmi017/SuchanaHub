"""
SUCHANA HUB - Student Routes
Handles student management (CRUD operations)
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Student
from app.routes.auth_routes import login_required, role_required

# Create blueprint for student routes
student_bp = Blueprint('student', __name__, url_prefix='/students')


# ============================================================================
# VIEW STUDENTS - List all students
# ============================================================================
@student_bp.route('/view', methods=['GET'])
@login_required
def view_students():
    """
    Display list of all students
    Accessible to Admin and Staff only
    """
    
    # Get all students from database
    try:
        students = Student.query.all()
        return render_template('student_management.html', students=students)
    except Exception as e:
        flash(f'Error fetching students: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))


# ============================================================================
# ADD STUDENT - Create new student
# ============================================================================
@student_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_student():
    """
    Add new student to system
    POST: Process form submission
    """
    
    if request.method == 'POST':
        try:
            # Get form data
            student_id = request.form.get('student_id', '').strip()
            roll_no = request.form.get('roll_no', '').strip()
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            class_name = request.form.get('class_name', '').strip()
            guardian_name = request.form.get('guardian_name', '').strip()
            guardian_phone = request.form.get('guardian_phone', '').strip()
            guardian_email = request.form.get('guardian_email', '').strip()
            
            # Validate required fields
            if not all([student_id, roll_no, name, class_name, guardian_name, guardian_phone]):
                flash('Please fill all required fields.', 'danger')
                return render_template('student_management.html')
            
            # Check if student already exists
            existing = Student.query.filter(
                (Student.student_id == student_id) | (Student.roll_no == roll_no)
            ).first()
            
            if existing:
                flash('Student ID or Roll Number already exists.', 'danger')
                return render_template('student_management.html')
            
            # Create new student object
            new_student = Student(
                student_id=student_id,
                roll_no=roll_no,
                name=name,
                email=email,
                class_name=class_name,
                guardian_name=guardian_name,
                guardian_phone=guardian_phone,
                guardian_email=guardian_email
            )
            
            # Add to database
            db.session.add(new_student)
            db.session.commit()
            
            flash(f'Student {name} added successfully!', 'success')
            return redirect(url_for('student.view_students'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
            return render_template('student_management.html')
    
    return render_template('student_management.html')


# ============================================================================
# EDIT STUDENT - Update student information
# ============================================================================
@student_bp.route('/edit/<int:student_id>', methods=['GET', 'POST'])
@login_required
def edit_student(student_id):
    """
    Edit existing student record
    """
    
    try:
        # Get student from database
        student = Student.query.get_or_404(student_id)
        
        if request.method == 'POST':
            # Update student fields
            student.name = request.form.get('name', '').strip()
            student.email = request.form.get('email', '').strip()
            student.class_name = request.form.get('class_name', '').strip()
            student.guardian_name = request.form.get('guardian_name', '').strip()
            student.guardian_phone = request.form.get('guardian_phone', '').strip()
            student.guardian_email = request.form.get('guardian_email', '').strip()
            
            # Save changes
            db.session.commit()
            flash(f'Student {student.name} updated successfully!', 'success')
            return redirect(url_for('student.view_students'))
        
        # Display edit form (GET request)
        return render_template('student_management.html', student=student)
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating student: {str(e)}', 'danger')
        return redirect(url_for('student.view_students'))


# ============================================================================
# DELETE STUDENT - Remove student from system
# ============================================================================
@student_bp.route('/delete/<int:student_id>', methods=['POST'])
@login_required
def delete_student(student_id):
    """
    Delete student record (may not be recommended - better to mark as inactive)
    """
    
    try:
        student = Student.query.get_or_404(student_id)
        student_name = student.name
        
        # Instead of deleting, mark as inactive (better for data integrity)
        student.is_active = False
        db.session.commit()
        
        flash(f'Student {student_name} has been deactivated.', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('student.view_students'))


# ============================================================================
# VIEW STUDENT ATTENDANCE - Show attendance for specific student
# ============================================================================
@student_bp.route('/<int:student_id>/attendance', methods=['GET'])
@login_required
def view_student_attendance(student_id):
    """
    Display attendance records for a specific student
    """
    
    try:
        from app.models import Attendance
        
        student = Student.query.get_or_404(student_id)
        attendance_records = Attendance.query.filter_by(student_id=student_id).all()
        
        return render_template('attendance.html', 
                             student=student, 
                             attendance_records=attendance_records)
    
    except Exception as e:
        flash(f'Error fetching student attendance: {str(e)}', 'danger')
        return redirect(url_for('student.view_students'))
