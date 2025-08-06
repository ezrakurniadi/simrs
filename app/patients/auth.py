from flask import Blueprint

bp = Blueprint('patient_auth', __name__)

from app.patients import auth_routes