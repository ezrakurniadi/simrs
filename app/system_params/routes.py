from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from app.system_params import bp
from app.utils import roles_required
from app.system_params.models import get_all_nationalities, Nationality, db
from app.system_params.forms import NationalityForm

@bp.route('/admin/system-params', methods=['GET'])
@roles_required('Admin')
def dashboard():
    return render_template('admin/system_params/dashboard.html')

@bp.route('/admin/system-params/settings', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_settings():
    # TODO: Implement system parameter management logic
    return render_template('admin/system_params/settings.html')

@bp.route('/api/nationalities', methods=['GET'])
def get_nationalities():
    nationalities = get_all_nationalities()
    return jsonify([{'id': n.id, 'name': n.name} for n in nationalities])

@bp.route('/admin/system-params/nationalities', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_nationalities():
    form = NationalityForm()
    if form.validate_on_submit():
        new_nationality = Nationality(name=form.name.data)
        db.session.add(new_nationality)
        db.session.commit()
        flash('Nationality added successfully', 'success')
        return redirect(url_for('admin.system_params.manage_nationalities'))
    nationalities = get_all_nationalities()
    return render_template('admin/system_params/nationalities.html', form=form, nationalities=nationalities)