from flask import url_for

def get_user_dashboard_url(user):
    """Get the dashboard URL for a user based on their roles."""
    if user.has_role('Admin'):
        return url_for('admin.dashboard')
    elif user.has_role('Doctor'):
        return url_for('doctor.dashboard')
    elif user.has_role('Nurse'):
        return url_for('nurse.dashboard')
    elif user.has_role('Receptionist'):
        return url_for('receptionist.dashboard')
    elif user.has_role('Lab Technician'):
        return url_for('lab.technician_dashboard')
    else:
        return url_for('patients.index')
