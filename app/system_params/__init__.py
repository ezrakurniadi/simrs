from flask import Blueprint

bp = Blueprint('system_params', __name__)

from app.system_params import routes