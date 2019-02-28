from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

#Application Factory function
def create_app(config_class=Config):
    app = Flask(__name__)

    """ Default config is the variables in the Config class in config.py. 
    Use a different argument for testing"""
    app.config.from_object(config_class)

    #Initalize app with 
    db.init_app(app)
    migrate.init_app(app, db)



    #Register all Blueprints
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    return app

from app import models
