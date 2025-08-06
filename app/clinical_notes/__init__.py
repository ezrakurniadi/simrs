from flask import Blueprint

bp = Blueprint('clinical_notes', __name__)

from app.clinical_notes import routes