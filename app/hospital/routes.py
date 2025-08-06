from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.hospital import bp
from app.hospital.forms import HospitalForm, ClinicForm, WardForm, RoomClassForm, DoctorProfileForm, DoctorScheduleForm, BedAssignmentForm, DischargeForm, TransferForm, WardRoomClassAssignmentForm
from app.hospital.models import Hospital, Clinic, Ward, RoomClass, DoctorProfile, DoctorSchedule, db, Bed, WardRoom, Admission, WardRoomClassAssignment
from app.auth.models import User
from app.utils import roles_required
from app.patients.models import Patient


@bp.route('/admin/hospital', methods=['GET'])
@roles_required('Admin')
def dashboard():
    hospital = Hospital.query.first()
    return render_template('hospital/dashboard.html', hospital=hospital)


@bp.route('/admin/hospital/settings', methods=['GET', 'POST'])
@roles_required('Admin')
def manage_settings():
    hospital = Hospital.query.first()
    form = HospitalForm(obj=hospital)
    
    if form.validate_on_submit():
        try:
            if hospital is None:
                # Create new hospital
                hospital = Hospital(
                    name=form.name.data,
                    code=form.code.data,
                    address=form.address.data,
                    phone=form.phone.data,
                    email=form.email.data,
                    created_by=current_user.id,
                    updated_by=current_user.id
                )
                db.session.add(hospital)
            else:
                # Update existing hospital
                hospital.name = form.name.data
                hospital.code = form.code.data
                hospital.address = form.address.data
                hospital.phone = form.phone.data
                hospital.email = form.email.data
                hospital.updated_by = current_user.id
            
            db.session.commit()
            flash('Hospital information saved successfully.', 'success')
            return redirect(url_for('hospital.manage_settings'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error saving hospital information: {str(e)}', 'error')
    
    return render_template('hospital/settings.html', form=form, hospital=hospital)


# Clinic Management Routes
@bp.route('/admin/clinics', methods=['GET'])
@roles_required('Admin')
def list_clinics():
    clinics = Clinic.query.all()
    return render_template('hospital/clinics/list.html', clinics=clinics)


@bp.route('/admin/clinics/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_clinic():
    form = ClinicForm()
    hospital = Hospital.query.first()
    
    if form.validate_on_submit():
        try:
            clinic = Clinic(
                hospital_id=hospital.id if hospital else None,
                name=form.name.data,
                code=form.code.data,
                description=form.description.data,
                is_active=form.is_active.data,
                created_by=current_user.id,
                updated_by=current_user.id
            )
            db.session.add(clinic)
            db.session.commit()
            flash('Clinic created successfully.', 'success')
            return redirect(url_for('hospital.list_clinics'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating clinic: {str(e)}', 'error')
    
    return render_template('hospital/clinics/new.html', form=form)


@bp.route('/admin/clinics/<string:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_clinic(id):
    clinic = Clinic.query.get_or_404(id)
    form = ClinicForm(obj=clinic)
    
    if form.validate_on_submit():
        try:
            clinic.name = form.name.data
            clinic.code = form.code.data
            clinic.description = form.description.data
            clinic.is_active = form.is_active.data
            clinic.updated_by = current_user.id
            
            db.session.commit()
            flash('Clinic updated successfully.', 'success')
            return redirect(url_for('hospital.list_clinics'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating clinic: {str(e)}', 'error')
    
    return render_template('hospital/clinics/edit.html', form=form, clinic=clinic)


@bp.route('/admin/clinics/<string:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_clinic(id):
    clinic = Clinic.query.get_or_404(id)
    
    try:
        db.session.delete(clinic)
        db.session.commit()
        flash('Clinic deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting clinic: {str(e)}', 'error')
    
    return redirect(url_for('hospital.list_clinics'))


# Ward Management Routes
@bp.route('/admin/wards', methods=['GET'])
@roles_required('Admin')
def list_wards():
    wards = Ward.query.all()
    return render_template('hospital/wards/list.html', wards=wards)


@bp.route('/admin/wards/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_ward():
    form = WardForm()
    hospital = Hospital.query.first()
    
    # Populate preferred room class choices
    form.preferred_room_class_id.choices = [('', 'None')] + [(rc.id, rc.name) for rc in RoomClass.query.all()]
    
    if form.validate_on_submit():
        try:
            ward = Ward(
                hospital_id=hospital.id if hospital else None,
                name=form.name.data,
                code=form.code.data,
                description=form.description.data,
                floor=form.floor.data,
                preferred_room_class_id=form.preferred_room_class_id.data if form.preferred_room_class_id.data else None,
                is_active=form.is_active.data,
                created_by=current_user.id,
                updated_by=current_user.id
            )
            db.session.add(ward)
            db.session.commit()
            flash('Ward created successfully.', 'success')
            return redirect(url_for('hospital.list_wards'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating ward: {str(e)}', 'error')
    
    return render_template('hospital/wards/new.html', form=form)


@bp.route('/admin/wards/<string:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_ward(id):
    ward = Ward.query.get_or_404(id)
    form = WardForm(obj=ward)
    
    if form.validate_on_submit():
        try:
            ward.name = form.name.data
            ward.code = form.code.data
            ward.description = form.description.data
            ward.floor = form.floor.data
            ward.is_active = form.is_active.data
            ward.updated_by = current_user.id
            
            db.session.commit()
            flash('Ward updated successfully.', 'success')
            return redirect(url_for('hospital.list_wards'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating ward: {str(e)}', 'error')
    
    return render_template('hospital/wards/edit.html', form=form, ward=ward)


@bp.route('/admin/wards/<string:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_ward(id):
    ward = Ward.query.get_or_404(id)
    
    try:
        db.session.delete(ward)
        db.session.commit()
        flash('Ward deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ward: {str(e)}', 'error')
    

# Room Class Management Routes
@bp.route('/admin/room_classes', methods=['GET'])
@roles_required('Admin')
def list_room_classes():
    room_classes = RoomClass.query.all()
    return render_template('hospital/room_classes/list.html', room_classes=room_classes)


@bp.route('/admin/room_classes/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_room_class():
    form = RoomClassForm()
    
    if form.validate_on_submit():
        try:
            room_class = RoomClass(
                name=form.name.data,
                code=form.code.data,
                description=form.description.data,
                daily_rate=form.daily_rate.data if form.daily_rate.data else None,
                care_level=form.care_level.data,
                specialty=form.specialty.data,
                is_active=form.is_active.data,
                created_by=current_user.id,
                updated_by=current_user.id
            )
            db.session.add(room_class)
            db.session.commit()
            flash('Room class created successfully.', 'success')
            return redirect(url_for('hospital.list_room_classes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating room class: {str(e)}', 'error')
    
    return render_template('hospital/room_classes/new.html', form=form)


@bp.route('/admin/room_classes/<string:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_room_class(id):
    room_class = RoomClass.query.get_or_404(id)
    form = RoomClassForm(obj=room_class)
    
    if form.validate_on_submit():
        try:
            room_class.name = form.name.data
            room_class.code = form.code.data
            room_class.description = form.description.data
            room_class.daily_rate = form.daily_rate.data if form.daily_rate.data else None
            room_class.is_active = form.is_active.data
            room_class.updated_by = current_user.id
            
            db.session.commit()
            flash('Room class updated successfully.', 'success')
            return redirect(url_for('hospital.list_room_classes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating room class: {str(e)}', 'error')
    
    return render_template('hospital/room_classes/edit.html', form=form, room_class=room_class)


@bp.route('/admin/room_classes/<string:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_room_class(id):
    room_class = RoomClass.query.get_or_404(id)
    
    try:
        db.session.delete(room_class)
        db.session.commit()
        flash('Room class deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting room class: {str(e)}', 'error')
    
    return redirect(url_for('hospital.list_room_classes'))
    return redirect(url_for('hospital.list_wards'))


# Ward-Room Class Assignment Routes
@bp.route('/admin/ward_room_class_assignments', methods=['GET'])
@roles_required('Admin')
def list_ward_room_class_assignments():
    assignments = WardRoomClassAssignment.query.all()
    return render_template('hospital/ward_room_class_assignments/list.html', assignments=assignments)


# Doctor Management Routes
@bp.route('/admin/ward_room_class_assignments/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_ward_room_class_assignment():
    form = WardRoomClassAssignmentForm()
    
    # Populate ward choices
    form.ward_id.choices = [(ward.id, ward.name) for ward in Ward.query.all()]
    
    # Populate room class choices
    form.room_class_id.choices = [(rc.id, rc.name) for rc in RoomClass.query.all()]
    
    if form.validate_on_submit():
        try:
            assignment = WardRoomClassAssignment(
                ward_id=form.ward_id.data,
                room_class_id=form.room_class_id.data,
                priority=form.priority.data,
                min_capacity=form.min_capacity.data,
                max_capacity=form.max_capacity.data if form.max_capacity.data else None,
                is_active=form.is_active.data,
                created_by=current_user.id,
                updated_by=current_user.id
            )
            db.session.add(assignment)
            db.session.commit()
            flash('Ward-room class assignment created successfully.', 'success')
            return redirect(url_for('hospital.list_ward_room_class_assignments'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating ward-room class assignment: {str(e)}', 'error')
    
    return render_template('hospital/ward_room_class_assignments/new.html', form=form)


@bp.route('/admin/ward_room_class_assignments/<string:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_ward_room_class_assignment(id):
    assignment = WardRoomClassAssignment.query.get_or_404(id)
    form = WardRoomClassAssignmentForm(obj=assignment)
    
    # Populate ward choices
    form.ward_id.choices = [(ward.id, ward.name) for ward in Ward.query.all()]
    
    # Populate room class choices
    form.room_class_id.choices = [(rc.id, rc.name) for rc in RoomClass.query.all()]
    
    if form.validate_on_submit():
        try:
            assignment.ward_id = form.ward_id.data
            assignment.room_class_id = form.room_class_id.data
            assignment.priority = form.priority.data
            assignment.min_capacity = form.min_capacity.data
            assignment.max_capacity = form.max_capacity.data if form.max_capacity.data else None
            assignment.is_active = form.is_active.data
            assignment.updated_by = current_user.id
            db.session.commit()
            flash('Ward-room class assignment updated successfully.', 'success')
            return redirect(url_for('hospital.list_ward_room_class_assignments'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating ward-room class assignment: {str(e)}', 'error')
    
    return render_template('hospital/ward_room_class_assignments/edit.html', form=form, assignment=assignment)


@bp.route('/admin/ward_room_class_assignments/<string:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_ward_room_class_assignment(id):
    assignment = WardRoomClassAssignment.query.get_or_404(id)
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        flash('Ward-room class assignment deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting ward-room class assignment: {str(e)}', 'error')
    
    return redirect(url_for('hospital.list_ward_room_class_assignments'))


@bp.route('/admin/doctors', methods=['GET'])
@roles_required('Admin')
def list_doctors():
    doctors = DoctorProfile.query.all()
    return render_template('hospital/doctors/list.html', doctors=doctors)


@bp.route('/admin/doctors/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_doctor():
    form = DoctorProfileForm()
    
    # Populate user choices
    form.user_id.choices = [(user.id, f"{user.first_name} {user.last_name}") for user in User.query.all()]
    
    # Populate hospital choices
    form.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]
    
    if form.validate_on_submit():
        try:
            doctor = DoctorProfile(
                user_id=form.user_id.data,
                hospital_id=form.hospital_id.data,
                specialization=form.specialization.data,
                license_number=form.license_number.data,
                education=form.education.data,
                experience_years=form.experience_years.data,
                bio=form.bio.data,
                is_active=form.is_active.data,
                created_by=current_user.id,
                updated_by=current_user.id
            )
            db.session.add(doctor)
            db.session.commit()
            flash('Doctor created successfully.', 'success')
            return redirect(url_for('hospital.list_doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating doctor: {str(e)}', 'error')
    
    return render_template('hospital/doctors/new.html', form=form)


@bp.route('/admin/doctors/<string:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_doctor(id):
    doctor = DoctorProfile.query.get_or_404(id)
    form = DoctorProfileForm(obj=doctor)
    
    # Populate user choices
    form.user_id.choices = [(user.id, f"{user.first_name} {user.last_name}") for user in User.query.all()]
    
    # Populate hospital choices
    form.hospital_id.choices = [(hospital.id, hospital.name) for hospital in Hospital.query.all()]
    
    if form.validate_on_submit():
        try:
            doctor.user_id = form.user_id.data
            doctor.hospital_id = form.hospital_id.data
            doctor.specialization = form.specialization.data
            doctor.license_number = form.license_number.data
            doctor.education = form.education.data
            doctor.experience_years = form.experience_years.data
            doctor.bio = form.bio.data
            doctor.is_active = form.is_active.data
            doctor.updated_by = current_user.id
            
            db.session.commit()
            flash('Doctor updated successfully.', 'success')
            return redirect(url_for('hospital.list_doctors'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating doctor: {str(e)}', 'error')
    
    return render_template('hospital/doctors/edit.html', form=form, doctor=doctor)


@bp.route('/admin/doctors/<string:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_doctor(id):
    doctor = DoctorProfile.query.get_or_404(id)
    
    try:
        db.session.delete(doctor)
        db.session.commit()
        flash('Doctor deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting doctor: {str(e)}', 'error')
    
    return redirect(url_for('hospital.list_doctors'))


# Doctor Schedule Management Routes
@bp.route('/admin/doctors/<string:doctor_id>/schedules', methods=['GET'])
@roles_required('Admin')
def list_doctor_schedules(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    schedules = DoctorSchedule.query.filter_by(doctor_id=doctor_id).all()
    return render_template('hospital/doctors/schedules/list.html', doctor=doctor, schedules=schedules)
@bp.route('/admin/doctors/<string:doctor_id>/schedules/new', methods=['GET', 'POST'])
@roles_required('Admin')
def create_doctor_schedule(doctor_id):
    doctor = DoctorProfile.query.get_or_404(doctor_id)
    form = DoctorScheduleForm()
    
    # Populate doctor choices (current doctor only)
    form.doctor_id.choices = [(doctor.id, f"{doctor.user.first_name} {doctor.user.last_name}")]
    form.doctor_id.data = doctor.id
    
    # Populate clinic choices
    form.clinic_id.choices = [(clinic.id, clinic.name) for clinic in Clinic.query.all()]
    
    if form.validate_on_submit():
        try:
            schedule = DoctorSchedule(
                doctor_id=form.doctor_id.data,
                clinic_id=form.clinic_id.data,
                day_of_week=form.day_of_week.data,
                start_time=form.start_time.data,
                end_time=form.end_time.data,
                slot_duration=form.slot_duration.data,
                max_patients=form.max_patients.data,
                is_active=form.is_active.data,
                created_by=current_user.id,
                updated_by=current_user.id
            )
            db.session.add(schedule)
            db.session.commit()
            flash('Schedule created successfully.', 'success')
            return redirect(url_for('hospital.list_doctor_schedules', doctor_id=doctor_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating schedule: {str(e)}', 'error')
    
    return render_template('hospital/doctors/schedules/new.html', form=form, doctor=doctor)

# Bed Management Routes
@bp.route('/admin/beds', methods=['GET'])
@roles_required('Admissions Clerk', 'Nurse')
def view_beds():
    try:
        # Fetch all beds with their relationships
        beds = Bed.query.all()
        
        # Fetch wards and room classes for filtering
        wards = Ward.query.all()
        room_classes = RoomClass.query.all()
        
        # Organize beds by ward and room class
        bed_data = {}
        for bed in beds:
            # Ensure bed has required relationships
            if not bed.ward_room or not bed.ward_room.ward or not bed.ward_room.room_class:
                continue
                
            ward_id = bed.ward_room.ward.id
            room_class_id = bed.ward_room.room_class.id
            
            # Initialize ward data if not exists
            if ward_id not in bed_data:
                bed_data[ward_id] = {
                    'ward': bed.ward_room.ward,
                    'room_classes': {}
                }
            
            # Initialize room class data if not exists
            if room_class_id not in bed_data[ward_id]['room_classes']:
                bed_data[ward_id]['room_classes'][room_class_id] = {
                    'room_class': bed.ward_room.room_class,
                    'rooms': []
                }
            
            # Check if room already exists in the list
            room_exists = False
            for room_data in bed_data[ward_id]['room_classes'][room_class_id]['rooms']:
                if room_data['ward_room'].id == bed.ward_room.id:
                    room_data['beds'].append(bed)
                    room_exists = True
                    break
            
            # If room doesn't exist, create new room entry
            if not room_exists:
                bed_data[ward_id]['room_classes'][room_class_id]['rooms'].append({
                    'ward_room': bed.ward_room,
                    'beds': [bed]
                })
        
        return render_template('hospital/beds/view.html', bed_data=bed_data, wards=wards, room_classes=room_classes)
    except Exception as e:
        flash(f'Error loading bed data: {str(e)}', 'error')
        return render_template('hospital/beds/view.html', bed_data={}, wards=[], room_classes=[])


# Bed Assignment Routes
@bp.route('/admin/beds/assign', methods=['GET', 'POST'])
@roles_required('Admissions Clerk', 'Nurse')
def assign_bed():
    from app.hospital.services import PatientPlacementService
    
    form = BedAssignmentForm()
    
    # Populate patient choices
    form.patient_id.choices = [(patient.id, f"{patient.first_name} {patient.last_name}") for patient in Patient.query.all()]
    
    # Populate bed choices (only available beds)
    form.bed_id.choices = [(bed.id, f"{bed.name} - {bed.ward_room.ward.name} - {bed.ward_room.name}") for bed in Bed.query.filter_by(is_occupied=False, is_active=True).all()]
    
    if form.validate_on_submit():
        try:
            # Check if bed is already occupied
            bed = Bed.query.get(form.bed_id.data)
            if bed.is_occupied:
                flash('This bed is already occupied.', 'error')
                return render_template('hospital/beds/assign.html', form=form)
            
            # Get the patient
            patient = Patient.query.get(form.patient_id.data)
            
            # Use PatientPlacementService to verify this is an optimal placement
            # In a real implementation, you might pass specific care level and specialty requirements
            optimal_ward, optimal_bed = PatientPlacementService.place_patient(patient)
            
            # Create admission record
            admission = Admission(
                patient_id=form.patient_id.data,
                bed_id=form.bed_id.data,
                admitted_by=current_user.id,
                status='Admitted'
            )
            
            # Update bed status to occupied
            bed.is_occupied = True
            bed.updated_by = current_user.id
            
            # Add to database
            db.session.add(admission)
            db.session.commit()
            
            flash('Patient assigned to bed successfully.', 'success')
            return redirect(url_for('hospital.view_beds'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error assigning patient to bed: {str(e)}', 'error')
    
    return render_template('hospital/beds/assign.html', form=form)


@bp.route('/admin/beds/<string:bed_id>/unassign', methods=['POST'])
@roles_required('Admissions Clerk', 'Nurse')
def unassign_bed(bed_id):
    try:
        # Find the active admission for this bed
        admission = Admission.query.filter_by(bed_id=bed_id, status='Admitted').first()
        if not admission:
            flash('No patient assigned to this bed.', 'error')
            return redirect(url_for('hospital.view_beds'))
        
        # Update admission status to discharged
        admission.status = 'Discharged'
        admission.discharge_date = db.func.current_timestamp()
        admission.updated_by = current_user.id
        
        # Update bed status to available
        bed = Bed.query.get(bed_id)
        bed.is_occupied = False
        bed.updated_by = current_user.id
        
        # Commit changes
        db.session.commit()
        
        flash('Patient unassigned from bed successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error unassigning patient from bed: {str(e)}', 'error')
    
    return redirect(url_for('hospital.view_beds'))


@bp.route('/admin/doctors/schedules/<string:id>/edit', methods=['GET', 'POST'])
@roles_required('Admin')
def edit_doctor_schedule(id):
    schedule = DoctorSchedule.query.get_or_404(id)
    form = DoctorScheduleForm(obj=schedule)
    
    # Populate doctor choices (current doctor only)
    form.doctor_id.choices = [(schedule.doctor.id, f"{schedule.doctor.user.first_name} {schedule.doctor.user.last_name}")]
    
    # Populate clinic choices
    form.clinic_id.choices = [(clinic.id, clinic.name) for clinic in Clinic.query.all()]
    
    if form.validate_on_submit():
        try:
            schedule.doctor_id = form.doctor_id.data
            schedule.clinic_id = form.clinic_id.data
            schedule.day_of_week = form.day_of_week.data
            schedule.start_time = form.start_time.data
            schedule.end_time = form.end_time.data
            schedule.slot_duration = form.slot_duration.data
            schedule.max_patients = form.max_patients.data
            schedule.is_active = form.is_active.data
            schedule.updated_by = current_user.id
            
            db.session.commit()
            flash('Schedule updated successfully.', 'success')
            return redirect(url_for('hospital.list_doctor_schedules', doctor_id=schedule.doctor_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating schedule: {str(e)}', 'error')
    
    return render_template('hospital/doctors/schedules/edit.html', form=form, schedule=schedule)


@bp.route('/admin/doctors/schedules/<string:id>/delete', methods=['POST'])
@roles_required('Admin')
def delete_doctor_schedule(id):
    schedule = DoctorSchedule.query.get_or_404(id)
    doctor_id = schedule.doctor_id
    
    try:
        db.session.delete(schedule)
        db.session.commit()
        flash('Schedule deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting schedule: {str(e)}', 'error')
    
    return redirect(url_for('hospital.list_doctor_schedules', doctor_id=doctor_id))


@bp.route('/nurse/ward_dashboard', methods=['GET'])
@roles_required('Nurse')
def nurse_ward_dashboard():
    try:
        # Fetch all wards
        wards = Ward.query.all()
        
        # Fetch occupied beds with patient information
        occupied_beds = Bed.query.filter_by(is_occupied=True).all()
        
        # Organize data by ward
        ward_data = {}
        for bed in occupied_beds:
            if bed.ward_room and bed.ward_room.ward:
                ward_id = bed.ward_room.ward.id
                ward_name = bed.ward_room.ward.name
                
                # Initialize ward data if not exists
                if ward_id not in ward_data:
                    ward_data[ward_id] = {
                        'ward_name': ward_name,
                        'rooms': {}
                    }
                
                # Get room information
                room_id = bed.ward_room.id
                room_name = bed.ward_room.name
                
                # Initialize room data if not exists
                if room_id not in ward_data[ward_id]['rooms']:
                    ward_data[ward_id]['rooms'][room_id] = {
                        'room_name': room_name,
                        'beds': []
                    }
                
                # Get patient information for occupied bed
                admission = Admission.query.filter_by(bed_id=bed.id, status='Admitted').first()
                patient_info = None
                if admission and admission.patient:
                    patient_info = {
                        'id': admission.patient.id,
                        'first_name': admission.patient.first_name,
                        'last_name': admission.patient.last_name,
                        'date_of_birth': admission.patient.date_of_birth,
                        'gender': admission.patient.gender,
                        'admission_date': admission.admission_date
                    }
                
                # Add bed information
                bed_info = {
                    'id': bed.id,
                    'name': bed.name,
                    'patient': patient_info
                }
                
                ward_data[ward_id]['rooms'][room_id]['beds'].append(bed_info)
        
        return render_template('hospital/nurse_ward_dashboard.html', ward_data=ward_data, wards=wards)
    except Exception as e:
        flash(f'Error loading ward dashboard: {str(e)}', 'error')
        return render_template('hospital/nurse_ward_dashboard.html', ward_data={}, wards=[])


# Patient Transfer Routes
@bp.route('/nurse/patient_transfer', methods=['GET', 'POST'])
@roles_required('Nurse')
def transfer_patient():
    form = TransferForm()
    # Get patient_id from query parameters if provided
    patient_id = request.args.get('patient_id')
    
    # Populate patient choices (only patients with active admissions)
    active_admissions = Admission.query.filter_by(status='Admitted').all()
    form.patient_id.choices = [(admission.patient.id, f"{admission.patient.first_name} {admission.patient.last_name}") for admission in active_admissions]
    
    # If patient_id is provided, set it as the default choice
    if patient_id:
        form.patient_id.data = patient_id
    
    # Populate current bed choices (only beds with active admissions)
    form.current_bed_id.choices = [(admission.bed.id, f"{admission.bed.name} - {admission.bed.ward_room.ward.name} - {admission.bed.ward_room.name}") for admission in active_admissions]
    
    # Populate new bed choices (only available beds)
    form.new_bed_id.choices = [(bed.id, f"{bed.name} - {bed.ward_room.ward.name} - {bed.ward_room.name}") for bed in Bed.query.filter_by(is_occupied=False, is_active=True).all()]
    
    if form.validate_on_submit():
        try:
            # Get the current admission record
            current_admission = Admission.query.filter_by(
                patient_id=form.patient_id.data,
                bed_id=form.current_bed_id.data,
                status='Admitted'
            ).first()
            
            if not current_admission:
                flash('No active admission found for this patient in the specified bed.', 'error')
                return render_template('hospital/patient_transfer.html', form=form)
            
            # Check if new bed is the same as current bed
            if form.current_bed_id.data == form.new_bed_id.data:
                flash('Cannot transfer to the same bed.', 'error')
                return render_template('hospital/patient_transfer.html', form=form)
            
            # Check if new bed is available
            new_bed = Bed.query.get(form.new_bed_id.data)
            if not new_bed or new_bed.is_occupied:
                flash('Selected bed is not available.', 'error')
                return render_template('hospital/patient_transfer.html', form=form)
            
            # Update current admission status to 'Transferred'
            current_admission.status = 'Transferred'
            current_admission.updated_by = current_user.id
            
            # Update current bed status to available
            current_bed = Bed.query.get(form.current_bed_id.data)
            current_bed.is_occupied = False
            current_bed.updated_by = current_user.id
            
            # Create new admission record for the transfer
            new_admission = Admission(
                patient_id=form.patient_id.data,
                bed_id=form.new_bed_id.data,
                admitted_by=current_user.id,
                status='Admitted'
            )
            
            # Update new bed status to occupied
            new_bed.is_occupied = True
            new_bed.updated_by = current_user.id
            
            # Add to database
            db.session.add(new_admission)
            db.session.commit()
            
            flash('Patient transferred successfully.', 'success')
            return redirect(url_for('hospital.nurse_ward_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error transferring patient: {str(e)}', 'error')
    
    return render_template('hospital/patient_transfer.html', form=form)


# Patient Discharge Routes
@bp.route('/nurse/patient_discharge', methods=['GET', 'POST'])
@roles_required('Nurse')
def discharge_patient():
    form = DischargeForm()
    
    # Get patient_id from query parameters if provided
    patient_id = request.args.get('patient_id')
    
    # Populate patient choices (only patients with active admissions)
    active_admissions = Admission.query.filter_by(status='Admitted').all()
    form.patient_id.choices = [(admission.patient.id, f"{admission.patient.first_name} {admission.patient.last_name}") for admission in active_admissions]
    
    # If patient_id is provided, set it as the default choice
    if patient_id:
        form.patient_id.data = patient_id
    
    # Populate bed choices (only beds with active admissions)
    form.bed_id.choices = [(admission.bed.id, f"{admission.bed.name} - {admission.bed.ward_room.ward.name} - {admission.bed.ward_room.name}") for admission in active_admissions]
    
    if form.validate_on_submit():
        try:
            # Get the current admission record
            current_admission = Admission.query.filter_by(
                patient_id=form.patient_id.data,
                bed_id=form.bed_id.data,
                status='Admitted'
            ).first()
            
            if not current_admission:
                flash('No active admission found for this patient in the specified bed.', 'error')
                return render_template('hospital/patient_discharge.html', form=form)
            
            # Update admission status to 'Discharged'
            current_admission.status = 'Discharged'
            current_admission.discharge_date = db.func.current_timestamp()
            current_admission.updated_by = current_user.id
            
            # Update bed status to available
            bed = Bed.query.get(form.bed_id.data)
            bed.is_occupied = False
            bed.updated_by = current_user.id
            
            # Commit changes
            db.session.commit()
            
            flash('Patient discharged successfully.', 'success')
            return redirect(url_for('hospital.nurse_ward_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error discharging patient: {str(e)}', 'error')
    
    return render_template('hospital/patient_discharge.html', form=form)