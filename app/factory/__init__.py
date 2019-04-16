from flask import Blueprint

bp = Blueprint('factory', __name__)


from app.factory import routes
