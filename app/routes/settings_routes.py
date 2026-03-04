"""
SUCHANA HUB - Settings Routes
Handles system configuration and user profile management
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models import db, Settings, User
from app.routes.auth_routes import login_required

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


# ============================================================================
# VIEW SETTINGS PAGE
# ============================================================================
@settings_bp.route('/', methods=['GET'])
@login_required
def view_settings():
    """
    Display system settings page
    Admin can change system settings
    All users can change their profile
    """
    
    try:
        # Get current user
        user = User.query.get(session.get('user_id'))
        
        # Get system settings if admin
        system_settings = {}
        if session.get('role') == 'admin':
            settings = Settings.query.all()
            for setting in settings:
                system_settings[setting.setting_key] = setting.setting_value
        
        return render_template('settings.html',
                             user=user,
                             system_settings=system_settings)
    
    except Exception as e:
        flash(f'Error loading settings: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))


# ============================================================================
# SAVE SYSTEM SETTINGS
# ============================================================================
@settings_bp.route('/save', methods=['POST'])
@login_required
def save_settings():
    """
    Save system settings (Admin only)
    """
    
    # Check if user is admin
    if session.get('role') != 'admin':
        flash('You do not have permission to change system settings.', 'danger')
        return redirect(url_for('settings.view_settings'))
    
    try:
        # Map of settings to save
        settings_to_save = {
            'morning_cutoff_time': request.form.get('morning_cutoff_time', '09:00'),
            'afternoon_cutoff_time': request.form.get('afternoon_cutoff_time', '14:00'),
            'absent_threshold': request.form.get('absent_threshold', '120'),
            'min_attendance_percentage': request.form.get('min_attendance_percentage', '75'),
            'smtp_server': request.form.get('smtp_server', 'smtp.gmail.com'),
            'smtp_port': request.form.get('smtp_port', '587'),
            'sender_email': request.form.get('sender_email', ''),
            'sms_provider': request.form.get('sms_provider', ''),
            'institution_name': request.form.get('institution_name', ''),
        }
        
        # Save or update settings
        for key, value in settings_to_save.items():
            setting = Settings.query.filter_by(setting_key=key).first()
            
            if setting:
                setting.setting_value = value
            else:
                setting = Settings(
                    setting_key=key,
                    setting_value=value,
                    data_type='string'
                )
                db.session.add(setting)
        
        # Handle boolean settings
        boolean_settings = {
            'notify_on_absent': 'notify_on_absent',
            'notify_on_late': 'notify_on_late',
            'count_late_as_present': 'count_late_as_present'
        }
        
        for key, form_key in boolean_settings.items():
            value = 'true' if form_key in request.form else 'false'
            setting = Settings.query.filter_by(setting_key=key).first()
            
            if setting:
                setting.setting_value = value
            else:
                setting = Settings(
                    setting_key=key,
                    setting_value=value,
                    data_type='boolean'
                )
                db.session.add(setting)
        
        db.session.commit()
        flash('Settings saved successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error saving settings: {str(e)}', 'danger')
    
    return redirect(url_for('settings.view_settings'))


# ============================================================================
# UPDATE USER PROFILE
# ============================================================================
@settings_bp.route('/profile/update', methods=['POST'])
@login_required
def update_profile():
    """
    Update logged-in user's profile information
    """
    
    try:
        user = User.query.get(session.get('user_id'))
        
        # Update profile information
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validate email uniqueness
        existing_email = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()
        
        if existing_email:
            flash('Email is already in use.', 'danger')
            return redirect(url_for('settings.view_settings'))
        
        # Update fields
        if full_name:
            user.full_name = full_name
        if email:
            user.email = email
        if phone:
            user.phone = phone
        
        # Handle password change
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        if current_password:
            # Verify current password
            if not user.check_password(current_password):
                flash('Current password is incorrect.', 'danger')
                return redirect(url_for('settings.view_settings'))
            
            # Verify new passwords match
            if new_password != confirm_password:
                flash('New passwords do not match.', 'danger')
                return redirect(url_for('settings.view_settings'))
            
            if len(new_password) < 6:
                flash('Password must be at least 6 characters.', 'danger')
                return redirect(url_for('settings.view_settings'))
            
            # Set new password
            user.set_password(new_password)
            flash('Password changed successfully!', 'success')
        
        db.session.commit()
        
        # Update session with new info
        session['full_name'] = user.full_name
        
        flash('Profile updated successfully!', 'success')
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating profile: {str(e)}', 'danger')
    
    return redirect(url_for('settings.view_settings'))


# ============================================================================
# SEND TEST NOTIFICATION (for configuration testing)
# ============================================================================
@settings_bp.route('/test-notification', methods=['POST'])
@login_required
def test_notification():
    """
    Send a test notification to verify configuration
    """
    
    try:
        # Get notification settings
        smtp_server = request.form.get('smtp_server', 'smtp.gmail.com')
        smtp_port = request.form.get('smtp_port', '587')
        
        # In production, would test actual email sending here
        flash('Test notification configuration is valid! (Actual sending not implemented)', 'info')
    
    except Exception as e:
        flash(f'Error testing notification: {str(e)}', 'danger')
    
    return redirect(url_for('settings.view_settings'))


# ============================================================================
# GET SETTING VALUE (Helper function)
# ============================================================================
def get_setting(key, default=None):
    """
    Retrieve a setting value by key
    Returns default if not found
    """
    try:
        setting = Settings.query.filter_by(setting_key=key).first()
        if setting:
            return setting.setting_value
    except:
        pass
    
    return default
