"""
SUCHANA HUB - Report Routes
Generates reports and analytics on attendance and system usage
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import db, Attendance, Student, Notification, Feedback
from app.routes.auth_routes import login_required

report_bp = Blueprint('report', __name__, url_prefix='/reports')


# ============================================================================
# HELPER FUNCTIONS - Report Generation
# ============================================================================

def get_attendance_summary(start_date=None, end_date=None, class_filter=None):
    """
    Generate attendance summary statistics
    Returns aggregated data for reporting
    """
    
    try:
        query = Attendance.query
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        if class_filter:
            query = query.filter_by(class_name=class_filter)
        
        # Get statistics
        total = query.count()
        present = query.filter_by(status='present').count()
        late = query.filter_by(status='late').count()
        absent = query.filter_by(status='absent').count()
        
        return {
            'total': total,
            'present': present,
            'late': late,
            'absent': absent,
            'attendance_percentage': (present / total * 100) if total > 0 else 0,
            'late_percentage': (late / total * 100) if total > 0 else 0,
            'absent_percentage': (absent / total * 100) if total > 0 else 0
        }
    
    except Exception as e:
        print(f'Error generating attendance summary: {e}')
        return None


def get_absent_students(start_date=None, end_date=None):
    """
    Get list of chronically absent students
    """
    
    try:
        query = Attendance.query.filter_by(status='absent')
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        # Group by student and count absences
        absent_records = query.join(Student).group_by(
            Student.id
        ).add_columns(
            Student.roll_no.label('roll_no'),
            Student.name.label('student_name'),
            func.count(Attendance.id).label('absent_count')
        ).order_by(func.count(Attendance.id).desc()).all()
        
        return absent_records
    
    except Exception as e:
        print(f'Error getting absent students: {e}')
        return []


def get_late_arrivals(start_date=None, end_date=None):
    """
    Get students with late arrivals
    """
    
    try:
        query = Attendance.query.filter_by(status='late')
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        late_records = query.join(Student).add_columns(
            Student.roll_no.label('roll_no'),
            Student.name.label('student_name'),
            Attendance.date.label('date'),
            Attendance.check_in_time.label('check_in_time')
        ).order_by(Attendance.date.desc()).all()
        
        return late_records
    
    except Exception as e:
        print(f'Error getting late arrivals: {e}')
        return []


def get_student_attendance_record(student_id, start_date=None, end_date=None):
    """
    Get detailed attendance record for a specific student
    """
    
    try:
        query = Attendance.query.filter_by(student_id=student_id)
        
        if start_date:
            query = query.filter(Attendance.date >= start_date)
        if end_date:
            query = query.filter(Attendance.date <= end_date)
        
        records = query.order_by(Attendance.date.desc()).all()
        
        if records:
            total = len(records)
            present = len([r for r in records if r.status == 'present'])
            late = len([r for r in records if r.status == 'late'])
            absent = len([r for r in records if r.status == 'absent'])
            
            return {
                'records': records,
                'total': total,
                'present': present,
                'late': late,
                'absent': absent,
                'attendance_percentage': (present / total * 100) if total > 0 else 0
            }
        
        return None
    
    except Exception as e:
        print(f'Error getting student attendance: {e}')
        return None


# ============================================================================
# VIEW REPORTS
# ============================================================================
@report_bp.route('/view', methods=['GET'])
@login_required
def view_reports():
    """
    Display reports dashboard with various report options
    """
    
    try:
        # Get date range from query parameters (default to last 30 days)
        end_date_str = request.args.get('end_date', '')
        start_date_str = request.args.get('start_date', '')
        
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        else:
            end_date = datetime.now().date()
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        else:
            start_date = end_date - timedelta(days=30)
        
        # Get summaries
        attendance_summary = get_attendance_summary(start_date, end_date)
        
        return render_template('reports.html',
                             attendance_summary=attendance_summary,
                             start_date=start_date,
                             end_date=end_date)
    
    except Exception as e:
        flash(f'Error generating reports: {str(e)}', 'danger')
        return render_template('reports.html')


# ============================================================================
# ATTENDANCE SUMMARY REPORT
# ============================================================================
@report_bp.route('/attendance-summary', methods=['GET'])
@login_required
def attendance_summary_report():
    """
    Generate detailed attendance summary report
    """
    
    try:
        # Get filters
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        class_filter = request.args.get('class', '')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        # Generate report
        summary = get_attendance_summary(start_date, end_date, class_filter)
        
        # Get daily breakdown
        daily_query = db.session.query(
            Attendance.date,
            func.count(Attendance.id).label('total'),
            func.sum(func.cast(Attendance.status == 'present', db.Integer)).label('present'),
            func.sum(func.cast(Attendance.status == 'late', db.Integer)).label('late'),
            func.sum(func.cast(Attendance.status == 'absent', db.Integer)).label('absent')
        ).group_by(Attendance.date)
        
        if start_date:
            daily_query = daily_query.filter(Attendance.date >= start_date)
        if end_date:
            daily_query = daily_query.filter(Attendance.date <= end_date)
        if class_filter:
            daily_query = daily_query.filter(Attendance.class_name == class_filter)
        
        daily_summary = daily_query.order_by(Attendance.date.desc()).all()
        
        return render_template('reports.html',
                             report_type='attendance_summary',
                             summary=summary,
                             daily_summary=daily_summary)
    
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('report.view_reports'))


# ============================================================================
# ABSENT STUDENTS REPORT
# ============================================================================
@report_bp.route('/absent-students', methods=['GET'])
@login_required
def absent_students_report():
    """
    Generate report of absent and chronically absent students
    """
    
    try:
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        absent_students = get_absent_students(start_date, end_date)
        
        return render_template('reports.html',
                             report_type='absent_students',
                             absent_students=absent_students)
    
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('report.view_reports'))


# ============================================================================
# LATE ARRIVALS REPORT
# ============================================================================
@report_bp.route('/late-arrivals', methods=['GET'])
@login_required
def late_arrivals_report():
    """
    Generate report of late arrivals
    """
    
    try:
        start_date_str = request.args.get('start_date', '')
        end_date_str = request.args.get('end_date', '')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        late_arrivals = get_late_arrivals(start_date, end_date)
        
        return render_template('reports.html',
                             report_type='late_arrivals',
                             late_arrivals=late_arrivals)
    
    except Exception as e:
        flash(f'Error generating report: {str(e)}', 'danger')
        return redirect(url_for('report.view_reports'))
