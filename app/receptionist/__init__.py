from flask import Blueprint

bp = Blueprint('receptionist', __name__)

from app.receptionist import routes