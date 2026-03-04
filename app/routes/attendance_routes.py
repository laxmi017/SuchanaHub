"""
SUCHANA HUB - Attendance Routes
Handles attendance upload, processing, and management
Implements the core attendance logic: Present/Late/Absent categorization
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime, time
import csv
from io import StringIO
from app.models import db, Attendance, Student, Settings
from app.routes.auth_routes import login_required

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


# ============================================================================
# HELPER FUNCTIONS - Attendance Processing Logic
# ============================================================================

def get_cutoff_time():
    """
    Get cut-off time from settings or use default
    Time after which students are marked LATE
    """
    try:
        setting = Settings.query.filter_by(setting_key='morning_cutoff_time').first()
        if setting:
            return datetime.strptime(setting.setting_value, '%H:%M').time()
    except:
        pass
    
    return time(9, 0)  # Default: 09:00


def categorize_attendance(check_in_time, cutoff_time):
    """
    Categorize attendance based on check-in time
    
    Logic:
    - If check_in_time is None: ABSENT
    - If check_in_time <= cutoff_time: PRESENT
    - If check_in_time > cutoff_time: LATE
    
    Args:
        check_in_time: datetime.time object of check-in
        cutoff_time: datetime.time object for cut-off
    
    Returns:
        String: 'present', 'late', or 'absent'
    """
    
    if check_in_time is None:
        return 'absent'
    
    if check_in_time <= cutoff_time:
        return 'present'
    else:
        return 'late'


def parse_csv_attendance(csv_content, date, class_name):
    """
    Parse CSV attendance file and create attendance records
    
    Expected CSV format:
    student_id, roll_no, timestamp
    
    Args:
        csv_content: String content of CSV file
        date: Date for attendance
        class_name: Class/Section name
    
    Returns:
        Tuple: (records_created, errors)
    """
    
    records_created = 0
    errors = []
    cutoff_time = get_cutoff_time()
    
    try:
        # Parse CSV
        csv_reader = csv.DictReader(StringIO(csv_content))
        
        for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 (header is row1)
            try:
                student_id = row.get('student_id', '').strip()
                timestamp_str = row.get('timestamp', '').strip()
                
                if not student_id:
                    errors.append(f'Row {row_num}: Missing student_id')
                    continue
                
                # Find student
                student = Student.query.filter_by(student_id=student_id).first()
                if not student:
                    errors.append(f'Row {row_num}: Student {student_id} not found')
                    continue
                
                # Parse timestamp
                check_in_time = None
                if timestamp_str:
                    try:
                        check_in_time = datetime.strptime(timestamp_str, '%H:%M:%S').time()
                    except ValueError:
                        errors.append(f'Row {row_num}: Invalid time format for {student_id}')
                        continue
                
                # Categorize attendance
                status = categorize_attendance(check_in_time, cutoff_time)
                
                # Check if record already exists
                existing = Attendance.query.filter_by(
                    student_id=student.id,
                    date=date
                ).first()
                
                if existing:
                    # Update existing record
                    existing.check_in_time = check_in_time
                    existing.status = status
                else:
                    # Create new record
                    attendance = Attendance(
                        student_id=student.id,
                        date=date,
                        check_in_time=check_in_time,
                        class_name=class_name,
                        status=status
                    )
                    db.session.add(attendance)
                
                records_created += 1
            
            except Exception as e:
                errors.append(f'Row {row_num}: {str(e)}')
        
        db.session.commit()
    
    except Exception as e:
        errors.append(f'CSV parsing error: {str(e)}')
    
    return records_created, errors


# ============================================================================
# ATTENDANCE UPLOAD ROUTE
# ============================================================================
@attendance_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def attendance_upload():
    """
    Handle attendance file upload and processing
    Supports CSV and Excel formats
    """
    
    if request.method == 'POST':
        try:
            # Check if file is present
            if 'attendance_file' not in request.files:
                flash('No file selected.', 'danger')
                return redirect(url_for('attendance.attendance_upload'))
            
            file = request.files['attendance_file']
            
            if file.filename == '':
                flash('No file selected.', 'danger')
                return redirect(url_for('attendance.attendance_upload'))
            
            # Get other form data
            attendance_date_str = request.form.get('attendance_date', '')
            class_id = request.form.get('class_id', '')
            
            if not attendance_date_str or not class_id:
                flash('Please select date and class.', 'danger')
                return redirect(url_for('attendance.attendance_upload'))
            
            # Parse date
            try:
                attendance_date = datetime.strptime(attendance_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'danger')
                return redirect(url_for('attendance.attendance_upload'))
            
            # Read file
            if file.filename.endswith('.csv'):
                # Handle CSV file
                stream = StringIO(file.read().decode('UTF-8'))
                csv_content = stream.getvalue()
                
                records_created, errors = parse_csv_attendance(csv_content, attendance_date, class_id)
                
                if errors:
                    flash(f'Processed {records_created} records with {len(errors)} errors.', 'warning')
                    for error in errors[:5]:  # Show first 5 errors
                        flash(f'  • {error}', 'info')
                else:
                    flash(f'Successfully processed {records_created} attendance records!', 'success')
            
            elif file.filename.endswith(('.xlsx', '.xls')):
                # Handle Excel file - simplified (would need openpyxl package)
                flash('Excel files are not yet supported. Please use CSV format.', 'info')
            
            else:
                flash('File format not supported. Please use CSV or Excel.', 'danger')
            
            return redirect(url_for('attendance.view_attendance'))
        
        except Exception as e:
            flash(f'Error processing file: {str(e)}', 'danger')
            return redirect(url_for('attendance.attendance_upload'))
    
    return render_template('attendance.html')


# ============================================================================
# VIEW ATTENDANCE RECORDS
# ============================================================================
@attendance_bp.route('/view', methods=['GET'])
@login_required
def view_attendance():
    """
    Display attendance records with filtering options
    """
    
    try:
        # Get filter parameters from query string
        date_filter = request.args.get('date', '')
        class_filter = request.args.get('class', '')
        status_filter = request.args.get('status', '')
        
        # Base query
        query = Attendance.query
        
        # Apply filters
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter_by(date=filter_date)
            except:
                pass
        
        if class_filter:
            query = query.filter_by(class_name=class_filter)
        
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        # Get records with student relationship
        attendance_records = query.join(Student).add_columns(
            Student.name.label('student_name'),
            Student.roll_no.label('roll_no')
        ).all()
        
        return render_template('attendance.html', attendance_records=attendance_records)
    
    except Exception as e:
        flash(f'Error fetching attendance records: {str(e)}', 'danger')
        return render_template('attendance.html', attendance_records=[])


# ============================================================================
# MARK ATTENDANCE MANUALLY
# ============================================================================
@attendance_bp.route('/mark/<int:student_id>', methods=['POST'])
@login_required
def mark_attendance(student_id):
    """
    Manually mark attendance for a student
    Useful for corrections or special cases
    """
    
    try:
        student = Student.query.get_or_404(student_id)
        
        status = request.form.get('status', 'present')
        date_str = request.form.get('date', '')
        notes = request.form.get('notes', '')
        
        # Validate
        if status not in ['present', 'late', 'absent']:
            flash('Invalid status.', 'danger')
            return redirect(url_for('attendance.view_attendance'))
        
        if not date_str:
            flash('Date is required.', 'danger')
            return redirect(url_for('attendance.view_attendance'))
        
        try:
            attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format.', 'danger')
            return redirect(url_for('attendance.view_attendance'))
        
        # Check if already exists
        existing = Attendance.query.filter_by(
            student_id=student_id,
            date=attendance_date
        ).first()
        
        if existing:
            existing.status = status
            existing.notes = notes
            message = 'Attendance updated'
        else:
            attendance = Attendance(
                student_id=student_id,
                date=attendance_date,
                status=status,
                notes=notes,
                class_name=student.class_name
            )
            db.session.add(attendance)
            message = 'Attendance marked'
        
        db.session.commit()
        flash(f'{message} successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error marking attendance: {str(e)}', 'danger')
    
    return redirect(url_for('attendance.view_attendance'))
