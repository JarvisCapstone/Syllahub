from flask import Blueprint

bp = Blueprint('instructor', __name__)


from app.instructor import routes
