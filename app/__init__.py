from config import Config
from flask import Flask, current_app
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

#Application Factory function
def create_app(config_class=Config):
    app = Flask(__name__)

    """ Default config is the variables in the Config class in config.py.
    Use a different argument for testing"""
    app.config.from_object(config_class)

    app.app_context().push()
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)


    # register blueprints with application
    # import blueprints here to avoid circular references
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.clo import bp as clo_bp
    app.register_blueprint(clo_bp, url_prefix='/clo')

    from app.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from app.instructor import bp as instructor_bp
    app.register_blueprint(instructor_bp, url_prefix='/instructor')

    from app.course import bp as course_bp
    app.register_blueprint(course_bp, url_prefix='/course')

    from app.syllabus import bp as syllabus_bp
    app.register_blueprint(syllabus_bp, url_prefix='/syllabus')

    return app 

from app import models
