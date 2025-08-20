from flask import jsonify, request
from app.api import bp
from app.system_params.models import IDType, PayorType, PayorDetail, Ethnicity, Language, Race
from app.patients.models import Nationality
from app.models import db

# API routes for system parameters
@bp.route('/id-types', methods=['GET'])
def get_id_types():
    id_types = IDType.query.filter_by(is_active=True).all()
    return jsonify([{'id': it.id, 'name': it.name} for it in id_types])

@bp.route('/payor-types', methods=['GET'])
def get_payor_types():
    payor_types = PayorType.query.filter_by(is_active=True).all()
    return jsonify([{'id': pt.id, 'name': pt.name} for pt in payor_types])

@bp.route('/payor-details/<int:payor_type_id>', methods=['GET'])
def get_payor_details(payor_type_id):
    payor_details = PayorDetail.query.filter_by(payor_type_id=payor_type_id, is_active=True).all()
    return jsonify([{'id': pd.id, 'name': pd.name} for pd in payor_details])

@bp.route('/ethnicities', methods=['GET'])
def get_ethnicities():
    search = request.args.get('search', '')
    print(f"API /ethnicities called with search: '{search}'")
    query = Ethnicity.query
    if search:
        query = query.filter(Ethnicity.name.ilike(f'%{search}%'))
    ethnicities = query.all()
    print(f"Found {len(ethnicities)} ethnicities")
    results = [{'id': e.name, 'text': e.name} for e in ethnicities]
    print(f"Returning results: {results[:5]}...")  # Print first 5 results
    return jsonify({
        'results': results
    })

@bp.route('/languages', methods=['GET'])
def get_languages():
    search = request.args.get('search', '')
    print(f"API /languages called with search: '{search}'")
    query = Language.query
    if search:
        query = query.filter(Language.name.ilike(f'%{search}%'))
    languages = query.all()
    print(f"Found {len(languages)} languages")
    results = [{'id': l.name, 'text': l.name} for l in languages]
    print(f"Returning results: {results[:5]}...")  # Print first 5 results
    return jsonify({
        'results': results
    })

@bp.route('/nationalities', methods=['GET'])
def get_nationalities():
    nationalities = Nationality.query.all()
    return jsonify([{'id': n.id, 'name': n.name} for n in nationalities])

@bp.route('/races', methods=['GET'])
def get_races():
    races = Race.query.all()
    return jsonify([{'id': r.name, 'text': r.name} for r in races])

# API routes for patients
@bp.route('/patients', methods=['GET'])
def get_patients():
    # TODO: Implement patient listing logic
    return jsonify({'patients': []})

@bp.route('/patients/<int:id>', methods=['GET'])
def get_patient(id):
    # TODO: Implement patient retrieval logic
    return jsonify({'patient': {}})

@bp.route('/patients', methods=['POST'])
def create_patient():
    # TODO: Implement patient creation logic
    return jsonify({'patient': {}}), 201

@bp.route('/patients/<int:id>', methods=['PUT'])
def update_patient(id):
    # TODO: Implement patient update logic
    return jsonify({'patient': {}})

@bp.route('/patients/<int:id>', methods=['DELETE'])
def delete_patient(id):
    # TODO: Implement patient deletion logic
    return jsonify({'message': 'Patient deleted'})

# API routes for appointments
@bp.route('/appointments', methods=['GET'])
def get_appointments():
    # TODO: Implement appointment listing logic
    return jsonify({'appointments': []})

@bp.route('/appointments/<int:id>', methods=['GET'])
def get_appointment(id):
    # TODO: Implement appointment retrieval logic
    return jsonify({'appointment': {}})

@bp.route('/appointments', methods=['POST'])
def create_appointment():
    # TODO: Implement appointment creation logic
    return jsonify({'appointment': {}}), 201

@bp.route('/appointments/<int:id>', methods=['PUT'])
def update_appointment(id):
    # TODO: Implement appointment update logic
    return jsonify({'appointment': {}})

@bp.route('/appointments/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    # TODO: Implement appointment deletion logic
    return jsonify({'message': 'Appointment deleted'})