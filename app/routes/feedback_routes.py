"""
SUCHANA HUB - Feedback Routes
Handles teacher feedback on student performance
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from app.models import db, Feedback, Student, User
from app.routes.auth_routes import login_required

feedback_bp = Blueprint('feedback', __name__, url_prefix='/feedback')


# ============================================================================
# VIEW FEEDBACK RECORDS
# ============================================================================
@feedback_bp.route('/view', methods=['GET'])
@login_required
def view_feedback():
    """
    Display feedback records with filtering based on role
    - Admin: Can view all feedback
    - Teachers: Can see their own feedback
    """
    
    try:
        # Get role from session
        role = session.get('role')
        user_id = session.get('user_id')
        
        # Base query
        query = Feedback.query
        
        # If teacher, only show their feedback
        if role == 'teacher':
            query = query.filter_by(teacher_id=user_id)
        
        # Get filter parameters
        student_filter = request.args.get('student', '')
        category_filter = request.args.get('category', '')
        
        # Apply filters
        if student_filter:
            query = query.join(Student).filter(Student.name.ilike(f'%{student_filter}%'))
        
        if category_filter:
            query = query.filter_by(category=category_filter)
        
        # Get feedback with relationships
        feedbacks = query.join(Student).join(User, User.id == Feedback.teacher_id).add_columns(
            Student.name.label('student_name'),
            Student.roll_no.label('student_roll_no'),
            User.full_name.label('teacher_name')
        ).all()
        
        return render_template('feedback.html', feedbacks=feedbacks)
    
    except Exception as e:
        flash(f'Error fetching feedback: {str(e)}', 'danger')
        return render_template('feedback.html', feedbacks=[])


# ============================================================================
# ADD NEW FEEDBACK
# ============================================================================
@feedback_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_feedback():
    """
    Add new feedback for a student
    Only teachers can add feedback
    """
    
    if request.method == 'POST':
        try:
            student_id = request.form.get('student_id')
            category = request.form.get('category')
            rating = request.form.get('rating')
            comments = request.form.get('comments', '')
            
            # Validate
            if not all([student_id, category, rating, comments]):
                flash('All fields are required.', 'danger')
                return redirect(url_for('feedback.add_feedback'))
            
            # Validate rating is between 1-5
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    raise ValueError
            except ValueError:
                flash('Rating must be between 1 and 5.', 'danger')
                return redirect(url_for('feedback.add_feedback'))
            
            # Verify student exists
            student = Student.query.get_or_404(student_id)
            
            # Create feedback record
            feedback = Feedback(
                student_id=student_id,
                teacher_id=session.get('user_id'),
                category=category,
                rating=rating,
                comments=comments,
                share_with_student=request.form.get('share_with_student') == 'on',
                share_with_guardian=request.form.get('share_with_guardian') == 'on'
            )
            
            db.session.add(feedback)
            db.session.commit()
            
            flash(f'Feedback added for {student.name} successfully!', 'success')
            return redirect(url_for('feedback.view_feedback'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding feedback: {str(e)}', 'danger')
            return redirect(url_for('feedback.add_feedback'))
    
    return render_template('feedback.html')


# ============================================================================
# EDIT FEEDBACK
# ============================================================================
@feedback_bp.route('/edit/<int:feedback_id>', methods=['GET', 'POST'])
@login_required
def edit_feedback(feedback_id):
    """
    Edit existing feedback record
    Only the teacher who created it can edit
    """
    
    try:
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # Check if user is the teacher who created this feedback
        if feedback.teacher_id != session.get('user_id') and session.get('role') != 'admin':
            flash('You do not have permission to edit this feedback.', 'danger')
            return redirect(url_for('feedback.view_feedback'))
        
        if request.method == 'POST':
            # Update feedback
            feedback.category = request.form.get('category')
            feedback.rating = int(request.form.get('rating', 3))
            feedback.comments = request.form.get('comments', '')
            feedback.share_with_student = request.form.get('share_with_student') == 'on'
            feedback.share_with_guardian = request.form.get('share_with_guardian') == 'on'
            
            db.session.commit()
            flash('Feedback updated successfully!', 'success')
            return redirect(url_for('feedback.view_feedback'))
        
        return render_template('feedback.html', feedback=feedback)
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating feedback: {str(e)}', 'danger')
        return redirect(url_for('feedback.view_feedback'))


# ============================================================================
# DELETE FEEDBACK
# ============================================================================
@feedback_bp.route('/delete/<int:feedback_id>', methods=['POST'])
@login_required
def delete_feedback(feedback_id):
    """
    Delete feedback record
    """
    
    try:
        feedback = Feedback.query.get_or_404(feedback_id)
        
        # Check permissions
        if feedback.teacher_id != session.get('user_id') and session.get('role') != 'admin':
            flash('You do not have permission to delete this feedback.', 'danger')
            return redirect(url_for('feedback.view_feedback'))
        
        db.session.delete(feedback)
        db.session.commit()
        
        flash('Feedback deleted successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting feedback: {str(e)}', 'danger')
    
    return redirect(url_for('feedback.view_feedback'))
