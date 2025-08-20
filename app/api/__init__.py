from flask import Blueprint

# Create Blueprint for API v1
bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import routes