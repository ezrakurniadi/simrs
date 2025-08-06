from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.lab import bp
from app.utils import roles_required
from app.lab.forms import LabOrderForm, LabResultForm, LabOrderSearchForm
from app.lab.models import LabOrder, LabResult, db
from app.patients.models import Patient
from app.auth.models import User
from datetime import datetime, timedelta

@bp.route('/dashboard', methods=['GET', 'POST'])
@roles_required('Lab Technician')
def technician_dashboard():
    form = LabOrderSearchForm()
    
    # Get filter parameters from form or query args
    patient_name = request.args.get('patient_name') or request.form.get('patient_name', '')
    test_type = request.args.get('test_type') or request.form.get('test_type', '')
    ordered_by = request.args.get('ordered_by') or request.form.get('ordered_by', '')
    start_date = request.args.get('start_date') or request.form.get('start_date')
    end_date = request.args.get('end_date') or request.form.get('end_date')
    status = request.args.get('status') or request.form.get('status', 'Ordered')
    
    # Build query
    query = LabOrder.query
    
    # Apply filters
    if patient_name:
        query = query.join(Patient).filter(
            db.or_(
                Patient.first_name.ilike(f"%{patient_name}%"),
                Patient.last_name.ilike(f"%{patient_name}%")
            )
        )
    
    if test_type and test_type != '':
        query = query.filter(LabOrder.test_type == test_type)
    
    if ordered_by:
        query = query.join(User, LabOrder.ordered_by == User.id).filter(
            db.or_(
                User.first_name.ilike(f"%{ordered_by}%"),
                User.last_name.ilike(f"%{ordered_by}%")
            )
        )
    
    if start_date:
        if isinstance(start_date, str):
            try:
                from datetime import datetime
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            except ValueError:
                start_date = None
        if start_date:
            query = query.filter(LabOrder.order_date >= start_date)
    
    if end_date:
        if isinstance(end_date, str):
            try:
                from datetime import datetime
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                end_date = None
        if end_date:
            # Add one day to include the entire end date
            end_date_plus_one = datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
            query = query.filter(LabOrder.order_date < end_date_plus_one)
    
    # Apply status filter (special handling for 'all')
    if status and status != 'all':
        query = query.filter(LabOrder.status == status)
    
    # Order by order_date descending
    lab_orders = query.order_by(LabOrder.order_date.desc()).all()
    
    # Set form data for display
    form.patient_name.data = patient_name
    form.test_type.data = test_type
    form.ordered_by.data = ordered_by
    form.start_date.data = start_date if isinstance(start_date, (datetime, type(None))) else None
    form.end_date.data = end_date if isinstance(end_date, (datetime, type(None))) else None
    form.status.data = status
    
    return render_template('lab/dashboard.html', lab_orders=lab_orders, form=form, status=status)

@bp.route('/patients/<string:patient_id>/lab_orders', methods=['GET'])
@roles_required('Doctor')
def view_lab_orders(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    lab_orders = LabOrder.query.filter_by(patient_id=patient.id).order_by(LabOrder.order_date.desc()).all()
    return render_template('lab/view.html', patient=patient, lab_orders=lab_orders)

@bp.route('/patients/<string:patient_id>/lab_orders/new', methods=['GET', 'POST'])
@roles_required('Doctor')
def order_lab_test(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = LabOrderForm()
    
    if form.validate_on_submit():
        try:
            lab_order = LabOrder(
                patient_id=patient.id,
                ordered_by=str(current_user.id),
                test_type=form.test_type.data,
                order_date=datetime.utcnow()
            )
            
            db.session.add(lab_order)
            db.session.commit()
            
            flash('Lab test ordered successfully!', 'success')
            return redirect(url_for('lab.view_lab_orders', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while ordering the lab test. Please try again.', 'error')
            print(f"Error ordering lab test: {str(e)}")
    
    return render_template('lab/new.html', form=form, patient=patient)

@bp.route('/patients/<string:patient_id>/lab_orders/<string:order_id>', methods=['GET'])
@roles_required('Doctor', 'Lab Technician')
def view_lab_order(patient_id, order_id):
    patient = Patient.query.get_or_404(patient_id)
    lab_order = LabOrder.query.filter_by(id=order_id, patient_id=patient.id).first_or_404()
    return render_template('lab/detail.html', patient=patient, lab_order=lab_order)

@bp.route('/patients/<string:patient_id>/lab_results', methods=['GET'])
@roles_required('Doctor', 'Lab Technician')
def view_patient_lab_results(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    # Get all completed lab orders with results for this patient
    lab_orders = LabOrder.query.filter_by(patient_id=patient.id, status='Completed').order_by(LabOrder.order_date.desc()).all()
    return render_template('lab/view.html', patient=patient, lab_orders=lab_orders)

@bp.route('/patients/<string:patient_id>/lab_orders/<string:order_id>/results/new', methods=['GET', 'POST'])
@roles_required('Lab Technician')
def enter_lab_result(patient_id, order_id):
    patient = Patient.query.get_or_404(patient_id)
    lab_order = LabOrder.query.filter_by(id=order_id, patient_id=patient.id).first_or_404()
    
    # Check if the lab order already has results
    if lab_order.lab_results:
        flash('Lab results for this order have already been entered.', 'warning')
        return redirect(url_for('lab.technician_dashboard'))
    
    form = LabResultForm()
    
    if form.validate_on_submit():
        try:
            lab_result = LabResult(
                order_id=lab_order.id,
                performed_by=str(current_user.id),
                result_data=form.result_data.data,
                result_date=datetime.utcnow()
            )
            
            # Update the lab order status to 'Completed'
            lab_order.status = 'Completed'
            
            db.session.add(lab_result)
            db.session.commit()
            
            flash('Lab results submitted successfully!', 'success')
            return redirect(url_for('lab.technician_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while submitting the lab results. Please try again.', 'error')
            print(f"Error submitting lab results: {str(e)}")
    
    return render_template('lab/enter_result.html', form=form, patient=patient, lab_order=lab_order)

@bp.route('/help', methods=['GET'])
@roles_required('Lab Technician')
def help():
    return render_template('lab/help.html')