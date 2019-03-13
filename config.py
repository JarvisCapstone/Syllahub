import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    print("os environ get", os.environ.get('DATABASE_URL'))
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://JarvisSyllahub:databaseforall@JarvisSyllahub.mysql.pythonanywhere-services.com/JarvisSyllahub$Syllahub"
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    #    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

