from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import current_user
from app.clinical_notes import bp
from app.utils import roles_required
from app.clinical_notes.forms import ClinicalNoteForm
from app.clinical_notes.models import ClinicalNote
from app.auth.models import db
from app.patients.models import Patient

@bp.route('/patients/<int:patient_id>/clinical_notes', methods=['GET'])
@roles_required('Doctor')
def view_clinical_notes(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    clinical_notes = ClinicalNote.query.filter_by(patient_id=patient.id).order_by(ClinicalNote.date.desc()).all()
    return render_template('clinical_notes/view.html', patient=patient, clinical_notes=clinical_notes)

@bp.route('/patients/<int:patient_id>/clinical_notes/new', methods=['GET', 'POST'])
@roles_required('Doctor')
def add_clinical_note(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = ClinicalNoteForm()
    
    if form.validate_on_submit():
        try:
            clinical_note = ClinicalNote(
                patient_id=patient.id,
                written_by=str(current_user.id),
                date=form.date.data,
                note_type=form.note_type.data,
                content=form.content.data
            )
            
            db.session.add(clinical_note)
            db.session.commit()
            
            flash('Clinical note saved successfully!', 'success')
            return redirect(url_for('clinical_notes.view_clinical_notes', patient_id=patient.id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while saving the clinical note. Please try again.', 'error')
            print(f"Error saving clinical note: {str(e)}")
    
    return render_template('clinical_notes/new.html', form=form, patient=patient)

@bp.route('/patients/<int:patient_id>/clinical_notes/<string:note_id>', methods=['GET'])
@roles_required('Doctor')
def view_clinical_note(patient_id, note_id):
    patient = Patient.query.get_or_404(patient_id)
    clinical_note = ClinicalNote.query.filter_by(id=note_id, patient_id=patient.id).first_or_404()
    return render_template('clinical_notes/detail.html', patient=patient, clinical_note=clinical_note)