from flask import Blueprint

bp = Blueprint('syllabus', __name__)


from app.syllabus import routes
