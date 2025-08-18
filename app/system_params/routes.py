from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import current_user
from app.system_params import bp
from app.utils import roles_required
from app.system_params.models import get_all_nationalities, PayorType, PayorDetail, IDType, db
from app.system_params.forms import PayorTypeForm, PayorDetailForm, IDTypeForm, EthnicityForm, LanguageForm

@bp.route('/admin/system-params', methods=['GET'])
@roles_required('Admin')
def dashboard():
    # Get counts for summary statistics
    from app.system_params.models import get_nationalities_count, get_active_settings_count, get_system_updates_count, get_last_updated

    nationalities_count = get_nationalities_count()
    active_settings_count = get_active_settings_count()
    system_updates_count = get_system_updates_count()
    last_updated = get_last_updated()

    return render_template(
        'admin/system_params/dashboard.html',
        nationalities_count=nationalities_count,
        active_settings_count=active_settings_count,
        system_updates_count=system_updates_count,
        last_updated=last_updated
    )

@bp.route('/admin/system-params/settings', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_settings():
    # TODO: Implement system parameter management logic
    return render_template('admin/system_params/settings.html')

@bp.route('/api/nationalities', methods=['GET'])
def get_nationalities():
    nationalities = get_all_nationalities()
    return jsonify([{'id': n.id, 'name': n.name} for n in nationalities])

@bp.route('/api/payor-types', methods=['GET'])
def get_payor_types():
    payor_types = PayorType.query.all()
    return jsonify([{'id': pt.id, 'name': pt.name} for pt in payor_types])

@bp.route('/api/payor-details/<int:payor_type_id>', methods=['GET'])
def get_payor_details_by_type(payor_type_id):
    payor_details = PayorDetail.query.filter_by(payor_type_id=payor_type_id).all()
    return jsonify([{'id': pd.id, 'name': pd.name} for pd in payor_details])

@bp.route('/api/id-types', methods=['GET'])
def get_id_types():
    id_types = IDType.query.all()
    return jsonify([{'id': it.id, 'name': it.name} for it in id_types])

@bp.route('/admin/system-params/payor-types', methods=['GET'])
@roles_required('Admin')
def manage_payor_types():
    payor_types = PayorType.query.all()
    return render_template('admin/system_params/payor_types.html', payor_types=payor_types)

@bp.route('/admin/system-params/payor-types/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_payor_type():
    form = PayorTypeForm()
    if form.validate_on_submit():
        payor_type = PayorType(
            name=form.name.data,
            description=form.description.data,
        )
        db.session.add(payor_type)
        db.session.commit()
        flash('Payor type created successfully', 'success')
        return redirect(url_for('system_params.manage_payor_types'))
    return render_template('admin/system_params/payor_type_form.html', form=form, title='Create Payor Type')

@bp.route('/admin/system-params/payor-types/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_payor_type(id):
    payor_type = PayorType.query.get_or_404(id)
    form = PayorTypeForm(obj=payor_type)
    if form.validate_on_submit():
        payor_type.name = form.name.data
        payor_type.description = form.description.data
        db.session.commit()
        flash('Payor type updated successfully', 'success')
        return redirect(url_for('system_params.manage_payor_types'))
    return render_template('admin/system_params/payor_type_form.html', form=form, title='Edit Payor Type')

@bp.route('/admin/system-params/payor-types/<int:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_payor_type(id):
    payor_type = PayorType.query.get_or_404(id)
    db.session.delete(payor_type)
    db.session.commit()
    flash('Payor type deleted successfully', 'success')
    return redirect(url_for('system_params.manage_payor_types'))

@bp.route('/admin/system-params/payor-details', methods=['GET'])
@roles_required('Admin')
def manage_payor_details():
    payor_details = PayorDetail.query.join(PayorType).all()
    return render_template('admin/system_params/payor_details.html', payor_details=payor_details)

@bp.route('/admin/system-params/payor-details/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_payor_detail():
    form = PayorDetailForm()
    # Populate payor type choices
    form.payor_type_id.choices = [(pt.id, pt.name) for pt in PayorType.query.all()]
    if form.validate_on_submit():
        payor_detail = PayorDetail(
            name=form.name.data,
            description=form.description.data,
            payor_type_id=form.payor_type_id.data,
        )
        db.session.add(payor_detail)
        db.session.commit()
        flash('Payor detail created successfully', 'success')
        return redirect(url_for('system_params.manage_payor_details'))
    return render_template('admin/system_params/payor_detail_form.html', form=form, title='Create Payor Detail')

@bp.route('/admin/system-params/payor-details/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_payor_detail(id):
    payor_detail = PayorDetail.query.get_or_404(id)
    form = PayorDetailForm(obj=payor_detail)
    # Populate payor type choices
    form.payor_type_id.choices = [(pt.id, pt.name) for pt in PayorType.query.all()]
    if form.validate_on_submit():
        payor_detail.name = form.name.data
        payor_detail.description = form.description.data
        payor_detail.payor_type_id = form.payor_type_id.data
        db.session.commit()
        flash('Payor detail updated successfully', 'success')
        return redirect(url_for('system_params.manage_payor_details'))
    return render_template('admin/system_params/payor_detail_form.html', form=form, title='Edit Payor Detail')

@bp.route('/admin/system-params/payor-details/<int:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_payor_detail(id):
    payor_detail = PayorDetail.query.get_or_404(id)
    db.session.delete(payor_detail)
    db.session.commit()
    flash('Payor detail deleted successfully', 'success')
    return redirect(url_for('system_params.manage_payor_details'))

@bp.route('/admin/system-params/id-types', methods=['GET'])
@roles_required('Admin')
def manage_id_types():
    id_types = IDType.query.all()
    return render_template('admin/system_params/id_types.html', id_types=id_types)

@bp.route('/admin/system-params/ethnicities', methods=['GET'])
@roles_required('Admin')
def manage_ethnicities():
    ethnicities = Ethnicity.query.all()
    return render_template('admin/system_params/ethnicities.html', ethnicities=ethnicities)

@bp.route('/admin/system-params/ethnicities/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_ethnicity():
    form = EthnicityForm()
    if form.validate_on_submit():
        ethnicity = Ethnicity(
            name=form.name.data,
            description=form.description.data,
        )
        db.session.add(ethnicity)
        db.session.commit()
        flash('Ethnicity created successfully', 'success')
        return redirect(url_for('system_params.manage_ethnicities'))
    return render_template('admin/system_params/ethnicity_form.html', form=form, title='Create Ethnicity')

@bp.route('/admin/system-params/ethnicities/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_ethnicity(id):
    ethnicity = Ethnicity.query.get_or_404(id)
    form = EthnicityForm(obj=ethnicity)
    if form.validate_on_submit():
        ethnicity.name = form.name.data
        ethnicity.description = form.description.data
        db.session.commit()
        flash('Ethnicity updated successfully', 'success')
        return redirect(url_for('system_params.manage_ethnicities'))
    return render_template('admin/system_params/ethnicity_form.html', form=form, title='Edit Ethnicity')

@bp.route('/admin/system-params/ethnicities/<int:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_ethnicity(id):
    ethnicity = Ethnicity.query.get_or_404(id)
    db.session.delete(ethnicity)
    db.session.commit()
    flash('Ethnicity deleted successfully', 'success')
    return redirect(url_for('system_params.manage_ethnicities'))

@bp.route('/admin/system-params/languages', methods=['GET'])
@roles_required('Admin')
def manage_languages():
    languages = Language.query.all()
    return render_template('admin/system_params/languages.html', languages=languages)

@bp.route('/admin/system-params/languages/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_language():
    form = LanguageForm()
    if form.validate_on_submit():
        language = Language(
            name=form.name.data,
            iso_code=form.iso_code.data,
        )
        db.session.add(language)
        db.session.commit()
        flash('Language created successfully', 'success')
        return redirect(url_for('system_params.manage_languages'))
    return render_template('admin/system_params/language_form.html', form=form, title='Create Language')

@bp.route('/admin/system-params/languages/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_language(id):
    language = Language.query.get_or_404(id)
    form = LanguageForm(obj=language)
    if form.validate_on_submit():
        language.name = form.name.data
        language.iso_code = form.iso_code.data
        db.session.commit()
        flash('Language updated successfully', 'success')
        return redirect(url_for('system_params.manage_languages'))
    return render_template('admin/system_params/language_form.html', form=form, title='Edit Language')

@bp.route('/admin/system-params/languages/<int:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_language(id):
    language = Language.query.get_or_404(id)
    db.session.delete(language)
    db.session.commit()
    flash('Language deleted successfully', 'success')
    return redirect(url_for('system_params.manage_languages'))

@bp.route('/admin/system-params/id_types', methods=['GET'])
@roles_required('Admin')
def manage_id_types_underscore():
    # Redirect to the canonical URL with hyphen
    return redirect(url_for('system_params.manage_id_types'))

@bp.route('/admin/system-params/id-types/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_id_type():
    form = IDTypeForm()
    if form.validate_on_submit():
        id_type = IDType(
            name=form.name.data,
            description=form.description.data,
        )
        db.session.add(id_type)
        db.session.commit()
        flash('ID type created successfully', 'success')
        return redirect(url_for('system_params.manage_id_types'))
    return render_template('admin/system_params/id_type_form.html', form=form, title='Create ID Type')

@bp.route('/admin/system-params/id-types/<int:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_id_type(id):
    id_type = IDType.query.get_or_404(id)
    form = IDTypeForm(obj=id_type)
    if form.validate_on_submit():
        id_type.name = form.name.data
        id_type.description = form.description.data
        db.session.commit()
        flash('ID type updated successfully', 'success')
        return redirect(url_for('system_params.manage_id_types'))
    return render_template('admin/system_params/id_type_form.html', form=form, title='Edit ID Type')

@bp.route('/admin/system-params/id-types/<int:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_id_type(id):
    id_type = IDType.query.get_or_404(id)
    db.session.delete(id_type)
    db.session.commit()
    flash('ID type deleted successfully', 'success')
    return redirect(url_for('system_params.manage_id_types'))