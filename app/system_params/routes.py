from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.system_params import bp
from app.utils import roles_required


@bp.route('/admin/system-params', methods=['GET'])
@roles_required('Admin')
def dashboard():
    return render_template('admin/system_params/dashboard.html')


@bp.route('/admin/system-params/settings', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_settings():
    # TODO: Implement system parameter management logic
    return render_template('admin/system_params/settings.html')