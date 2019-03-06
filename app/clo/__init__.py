from flask import Blueprint

bp = Blueprint('clo', __name__)


from app.clo import routes
