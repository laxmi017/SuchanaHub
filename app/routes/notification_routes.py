"""
SUCHANA HUB - Notification Routes
Handles sending and logging notifications to guardians
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models import db, Notification, Student
from app.routes.auth_routes import login_required

notification_bp = Blueprint('notification', __name__, url_prefix='/notifications')


# ============================================================================
# HELPER FUNCTIONS - Notification Sending
# ============================================================================

def send_notification(student_id, message, notification_type, delivery_method='email'):
    """
    Send notification to guardian and log it
    
    Simulated sending - in production would use SMS/Email APIs
    """
    
    try:
        student = Student.query.get(student_id)
        if not student:
            return False
        
        # Create notification record
        notification = Notification(
            student_id=student_id,
            notification_type=notification_type,
            message=message,
            recipient_name=student.guardian_name,
            recipient_phone=student.guardian_phone,
            recipient_email=student.guardian_email,
            delivery_method=delivery_method,
            status='sent',  # In production, would be 'pending' then updated after actual send
            delivery_timestamp=datetime.utcnow()
        )
        
        db.session.add(notification)
        db.session.commit()
        
        # TODO: Integrate with actual SMS/Email service
        # e.g., Twilio, SendGrid, AWS SES, etc.
        
        return True
    
    except Exception as e:
        print(f'Error sending notification: {e}')
        return False


def generate_attendance_message(student, status, date):
    """Generate automated attendance notification message"""
    
    if status == 'absent':
        return f"Dear {student.guardian_name}, your ward {student.name} was marked ABSENT on {date}. Please contact school for details."
    elif status == 'late':
        return f"Dear {student.guardian_name}, your ward {student.name} arrived LATE on {date}. Please ensure timely arrival."
    else:
        return f"Dear {student.guardian_name}, your ward {student.name} is marked PRESENT on {date}."


# ============================================================================
# VIEW NOTIFICATIONS
# ============================================================================
@notification_bp.route('/view', methods=['GET'])
@login_required
def view_notifications():
    """
    Display notification logs with filtering
    """
    
    try:
        # Get filter parameters
        status_filter = request.args.get('status', '')
        date_from = request.args.get('date_from', '')
        date_to = request.args.get('date_to', '')
        
        # Base query
        query = Notification.query
        
        # Apply filters
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        if date_from:
            try:
                from_date = datetime.strptime(date_from, '%Y-%m-%d')
                query = query.filter(Notification.created_at >= from_date)
            except:
                pass
        
        if date_to:
            try:
                to_date = datetime.strptime(date_to, '%Y-%m-%d')
                query = query.filter(Notification.created_at <= to_date)
            except:
                pass
        
        # Get all notifications, sorted by recent first
        notifications = query.order_by(Notification.created_at.desc()).all()
        
        return render_template('notifications.html', notifications=notifications)
    
    except Exception as e:
        flash(f'Error fetching notifications: {str(e)}', 'danger')
        return render_template('notifications.html', notifications=[])


# ============================================================================
# SEND MANUAL NOTIFICATION
# ============================================================================
@notification_bp.route('/send', methods=['POST'])
@login_required
def send_manual_notification():
    """
    Send manual notification to guardian
    """
    
    try:
        student_id = request.form.get('student_id')
        message = request.form.get('message', '')
        notification_type = request.form.get('notification_type', 'general_message')
        
        # Validate
        if not student_id or not message:
            flash('Student and message are required.', 'danger')
            return redirect(url_for('notification.view_notifications'))
        
        # Send notification
        if send_notification(student_id, message, notification_type):
            flash('Notification sent successfully!', 'success')
        else:
            flash('Error sending notification.', 'danger')
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('notification.view_notifications'))


# ============================================================================
# RESEND NOTIFICATION
# ============================================================================
@notification_bp.route('/resend/<int:notification_id>', methods=['POST'])
@login_required
def resend_notification(notification_id):
    """
    Resend a previously sent notification
    """
    
    try:
        notification = Notification.query.get_or_404(notification_id)
        
        # Create copy and resend
        if send_notification(
            notification.student_id,
            notification.message,
            notification.notification_type,
            notification.delivery_method
        ):
            flash('Notification resent successfully!', 'success')
        else:
            flash('Error resending notification.', 'danger')
    
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    
    return redirect(url_for('notification.view_notifications'))


# ============================================================================
# AUTO-SEND ABSENT NOTIFICATIONS
# ============================================================================
def send_absent_notifications(attendance_records):
    """
    Send notifications for absent students
    Call this after processing attendance
    """
    
    try:
        for attendance in attendance_records:
            if attendance.status == 'absent':
                student = Student.query.get(attendance.student_id)
                if student and student.guardian_phone:
                    message = generate_attendance_message(
                        student,
                        attendance.status,
                        attendance.date
                    )
                    send_notification(
                        attendance.student_id,
                        message,
                        'attendance_alert',
                        'sms'
                    )
    
    except Exception as e:
        print(f'Error sending absent notifications: {e}')
