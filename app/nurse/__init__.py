from flask import Blueprint

bp = Blueprint('nurse', __name__)

from app.nurse import routes