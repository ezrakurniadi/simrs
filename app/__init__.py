from flask import Flask
from config import config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

# Create SQLAlchemy instance
db = SQLAlchemy()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize database
    db.init_app(app)
    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    # User loader function
    from app.auth.models import User
    from app.patients.models import PatientUser
    @login_manager.user_loader
    def load_user(id):
        # Try to load as regular User first
        user = User.query.get(id)
        if user:
            return user
        # If not found, try to load as PatientUser
        return PatientUser.query.get(id)

    # Register blueprints
    from app.auth import bp as auth_bp
    from app.patients import bp as patients_bp
    from app.appointments import bp as appointments_bp
    from app.admin import bp as admin_bp
    from app.api import bp as api_bp
    from app.clinical_notes import bp as clinical_notes_bp
    from app.lab import bp as lab_bp
    from app.system_params import bp as system_params_bp
    from app.hospital import bp as hospital_bp
    from app.patients.auth import bp as patient_auth_bp
    from app.doctor import bp as doctor_bp
    from app.nurse import bp as nurse_bp
    from app.receptionist import bp as receptionist_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(patients_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(clinical_notes_bp)
    app.register_blueprint(lab_bp)
    app.register_blueprint(system_params_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(patient_auth_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(nurse_bp)
    app.register_blueprint(receptionist_bp)

    return app