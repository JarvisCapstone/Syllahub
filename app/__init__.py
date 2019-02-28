from config import Config
from flask import Flask
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

    #Initalize app with 
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)



    # register blueprints with application
    # import blueprints here to avoid circular references
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app

from app import models
