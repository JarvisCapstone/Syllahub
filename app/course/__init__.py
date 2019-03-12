from flask import Blueprint

bp = Blueprint('course', __name__)


from app.course import routes
